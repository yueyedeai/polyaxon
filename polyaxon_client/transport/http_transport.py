# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import os
import requests
import tarfile

from clint.textui import progress
from clint.textui.progress import Bar
from hestia.list_utils import to_list
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

from polyaxon_client import settings
from polyaxon_client.exceptions import ERRORS_MAPPING, PolyaxonShouldExitError
from polyaxon_client.logger import logger


class HttpTransportMixin(object):
    """HTTP operations transport."""
    MAX_UPLOAD_SIZE = 1024 * 1024 * 150

    @property
    def session(self):
        if not hasattr(self, '_session'):
            self._session = requests.Session()
        return self._session

    @staticmethod
    def create_progress_callback(encoder):
        encoder_len = encoder.len
        progress_bar = Bar(expected_size=encoder_len, filled_char='=')

        def callback(monitor):
            progress_bar.show(monitor.bytes_read)

        return callback, progress_bar

    @staticmethod
    def format_sizeof(num, suffix='B'):
        """
        Print in human friendly format
        """
        for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
            if abs(num) < 1024.0:
                return "%3.1f%s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f%s%s" % (num, 'Yi', suffix)

    def request(self,
                method,
                url,
                params=None,
                data=None,
                files=None,
                json=None,  # noqa
                timeout=None,
                headers=None,
                session=None):
        """Send a request with the given data as json to the given URL.

        Args:
            method: HTTP method
            url: The url to send the request to.
            params: Dictionary of values to format url.
            data:
            files:
            json:
            timeout:
            headers: extra headers to add to the request.

        Returns:
            Request response if successful, Exception otherwise.

        Raises:
            PolyaxonHTTPError or one of its subclasses.
        """
        logger.debug("Starting request to url: %s with params: %s, data: %s",
                     url, params, data)

        request_headers = self._get_headers(headers=headers)
        timeout = timeout if timeout is not None else settings.LONG_REQUEST_TIMEOUT
        session = session or self.session

        try:
            response = session.request(method,
                                       url,
                                       params=params,
                                       data=data,
                                       json=json,
                                       headers=request_headers,
                                       files=files,
                                       timeout=timeout,
                                       verify=self.config.verify_ssl)
        except (requests.exceptions.RequestException,
                requests.exceptions.Timeout,
                requests.exceptions.HTTPError) as exception:
            try:
                logger.debug("Exception: %s", exception, exc_info=True)
            except TypeError:
                pass
            raise PolyaxonShouldExitError(
                "Error connecting to Polyaxon server on `{}`.\n"
                "An Error `{}` occurred.\n"
                "Check your host and ports configuration "
                "and your internet connection.".format(url, exception))

        logger.debug("Response Content: %s, Headers: %s", response.content, response.headers)
        self.check_response_status(response, url)
        return response

    def upload(self,
               url,
               files,
               files_size,
               params=None,
               json_data=None,
               timeout=None,
               headers=None,
               session=None):

        if files_size > self.MAX_UPLOAD_SIZE:
            raise PolyaxonShouldExitError(
                "Files too large to sync, please keep it under {}.\n"
                "If you have data files in the current directory, "
                "please add them directly to your data volume, or upload them "
                "separately using `polyaxon data` command and remove them from here.\n".format(
                    self.format_sizeof(self.MAX_UPLOAD_SIZE)))

        files = to_list(files)
        if json_data:
            files.append(('json', json.dumps(json_data)))

        multipart_encoder = MultipartEncoder(
            fields=files
        )
        request_headers = headers or {}
        request_headers.update({"Content-Type": multipart_encoder.content_type})

        # Attach progress bar
        progress_callback, progress_bar = self.create_progress_callback(multipart_encoder)
        multipart_encoder_monitor = MultipartEncoderMonitor(multipart_encoder, progress_callback)

        timeout = timeout if timeout is not None else settings.LONG_REQUEST_TIMEOUT

        try:
            response = self.put(url=url,
                                params=params,
                                data=multipart_encoder_monitor,
                                headers=request_headers,
                                timeout=timeout,
                                session=session)
        finally:
            # always make sure we clear the console
            progress_bar.done()

        return response

    def download(self, url, filename, headers=None, timeout=None, session=None):
        """
        Download the file from the given url at the current path
        """
        logger.debug("Downloading files from url: %s", url)

        request_headers = self._get_headers(headers=headers)
        timeout = timeout if timeout is not None else settings.LONG_REQUEST_TIMEOUT
        session = session or self.session

        try:
            response = session.get(url,
                                   headers=request_headers,
                                   timeout=timeout,
                                   stream=True)
            self.check_response_status(response, url)
            with open(filename, 'wb') as f:
                # chunk mode response doesn't have content-length so we are
                # using a custom header here
                content_length = response.headers.get('x-polyaxon-content-length')
                if not content_length:
                    content_length = response.headers.get('content-length')
                if content_length:
                    for chunk in progress.bar(response.iter_content(chunk_size=1024),
                                              expected_size=(int(content_length) / 1024) + 1):
                        if chunk:
                            f.write(chunk)
                else:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
            return filename
        except (requests.exceptions.ConnectionError,
                requests.exceptions.RequestException,
                requests.exceptions.Timeout,
                requests.exceptions.HTTPError) as exception:
            try:
                logger.debug("Exception: %s", exception)
            except TypeError:
                pass

            raise PolyaxonShouldExitError(
                "Error connecting to Polyaxon server on `{}`.\n"
                "An Error `{}` occurred.\n"
                "Check your host and ports configuration "
                "and your internet connection.".format(url, exception))

    def download_tar(self, url, untar=True, delete_tar=False):
        """
        Download and optionally untar the tar file from the given url
        """
        try:
            logger.info("Downloading the tar file to the current directory ...")
            filename = self.download(url=url, filename='output.tar')
            if filename and untar:
                logger.info("Untarring the contents of the file ...")
                tar = tarfile.open(filename)
                tar.extractall()
                tar.close()
            if delete_tar:
                logger.info("Cleaning up the tar file ...")
                os.remove(filename)
            return filename
        except ERRORS_MAPPING['base'] as e:
            logger.info("Download URL ERROR! %s", e.message)
            return False

    def check_response_status(self, response, endpoint):
        """Check if response is successful. Else raise Exception."""

        if 200 <= response.status_code < 300:
            return response

        try:
            logger.error(
                "Request to %s failed with status code %s. \n"
                "Reason: %s", endpoint, response.status_code, response.text)
        except TypeError:
            logger.error("Request to %s failed with status code", endpoint)

        exception = ERRORS_MAPPING.get(response.status_code, ERRORS_MAPPING['http'])
        raise exception(endpoint=endpoint,
                        response=response,
                        message=response.text,
                        status_code=response.status_code)

    def get(self,
            url,
            params=None,
            data=None,
            files=None,
            json_data=None,
            timeout=None,
            headers=None,
            session=None):
        """Call request with a get."""
        return self.request('GET',
                            url=url,
                            params=params,
                            data=data,
                            files=files,
                            json=json_data,
                            timeout=timeout,
                            headers=headers,
                            session=session)

    def post(self,
             url,
             params=None,
             data=None,
             files=None,
             json_data=None,
             timeout=None,
             headers=None,
             session=None):
        """Call request with a post."""
        return self.request('POST',
                            url=url,
                            params=params,
                            data=data,
                            files=files,
                            json=json_data,
                            timeout=timeout,
                            headers=headers,
                            session=session)

    def patch(self,
              url,
              params=None,
              data=None,
              files=None,
              json_data=None,
              timeout=None,
              headers=None,
              session=None):
        """Call request with a patch."""
        return self.request('PATCH',
                            url=url,
                            params=params,
                            data=data,
                            files=files,
                            json=json_data,
                            timeout=timeout,
                            headers=headers,
                            session=session)

    def delete(self,
               url,
               params=None,
               data=None,
               files=None,
               json_data=None,
               timeout=None,
               headers=None,
               session=None):
        """Call request with a delete."""
        return self.request('DELETE',
                            url=url,
                            params=params,
                            data=data,
                            files=files,
                            json=json_data,
                            timeout=timeout,
                            headers=headers,
                            session=session)

    def put(self,
            url,
            params=None,
            data=None,
            files=None,
            json_data=None,
            timeout=None,
            headers=None,
            session=None):
        """Call request with a put."""
        return self.request('PUT',
                            url=url,
                            params=params,
                            data=data,
                            files=files,
                            json=json_data,
                            timeout=timeout,
                            headers=headers,
                            session=session)
