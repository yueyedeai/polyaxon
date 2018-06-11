import logging

from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver

import auditor

from constants.jobs import JobLifeCycle
from db.models.notebooks import NotebookJob, NotebookJobStatus
from event_manager.events.notebook import (
    NOTEBOOK_FAILED,
    NOTEBOOK_NEW_STATUS,
    NOTEBOOK_STOPPED,
    NOTEBOOK_SUCCEEDED
)
from libs.decorators import ignore_raw, ignore_updates, ignore_updates_pre
from libs.repos.utils import assign_code_reference
from polyaxon.celery_api import app as celery_app
from polyaxon.settings import SchedulerCeleryTasks

logger = logging.getLogger('polyaxon.signals.notebooks')


@receiver(pre_save, sender=NotebookJob, dispatch_uid="notebook_job_pre_save")
@ignore_updates_pre
@ignore_raw
def notebook_job_pre_save(sender, **kwargs):
    assign_code_reference(kwargs['instance'])


@receiver(post_save, sender=NotebookJob, dispatch_uid="notebook_job_post_save")
@ignore_updates
@ignore_raw
def notebook_job_post_save(sender, **kwargs):
    instance = kwargs['instance']
    instance.set_status(status=JobLifeCycle.CREATED)


@receiver(post_save, sender=NotebookJobStatus, dispatch_uid="notebook_job_status_post_save")
@ignore_updates
@ignore_raw
def notebook_job_status_post_save(sender, **kwargs):
    instance = kwargs['instance']
    job = instance.job
    previous_status = job.last_status
    # Update job last_status
    job.status = instance
    job.save()
    auditor.record(event_type=NOTEBOOK_NEW_STATUS,
                   instance=job,
                   previous_status=previous_status,
                   target='project')
    if instance.status == JobLifeCycle.STOPPED:
        auditor.record(event_type=NOTEBOOK_STOPPED,
                       instance=job,
                       previous_status=previous_status,
                       target='project')

    if instance.status == JobLifeCycle.FAILED:
        auditor.record(event_type=NOTEBOOK_FAILED,
                       instance=job,
                       previous_status=previous_status,
                       target='project')

    if instance.status == JobLifeCycle.STOPPED:
        auditor.record(event_type=NOTEBOOK_SUCCEEDED,
                       instance=job,
                       previous_status=previous_status,
                       target='project')


@receiver(pre_delete, sender=NotebookJob, dispatch_uid="notebook_job_pre_delete")
@ignore_raw
def notebook_job_pre_delete(sender, **kwargs):
    job = kwargs['instance']

    celery_app.send_task(
        SchedulerCeleryTasks.PROJECTS_NOTEBOOK_STOP,
        kwargs={
            'project_name': job.project.unique_name,
            'project_uuid': job.project.uuid.hex,
            'notebook_job_name': job.unique_name,
            'notebook_job_uuid': job.uuid.hex,
            'update_status': False
        })
