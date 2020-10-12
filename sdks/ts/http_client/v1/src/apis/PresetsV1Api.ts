// Copyright 2018-2020 Polyaxon, Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

/* tslint:disable */
/* eslint-disable */
/**
 * Polyaxon SDKs and REST API specification.
 * Polyaxon SDKs and REST API specification.
 *
 * The version of the OpenAPI document: 1.1.9
 * Contact: contact@polyaxon.com
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */


import * as runtime from '../runtime';
import {
    RuntimeError,
    RuntimeErrorFromJSON,
    RuntimeErrorToJSON,
    V1ListPresetsResponse,
    V1ListPresetsResponseFromJSON,
    V1ListPresetsResponseToJSON,
    V1Preset,
    V1PresetFromJSON,
    V1PresetToJSON,
} from '../models';

export interface CreatePresetRequest {
    owner: string;
    body: V1Preset;
}

export interface DeletePresetRequest {
    owner: string;
    uuid: string;
}

export interface GetPresetRequest {
    owner: string;
    uuid: string;
}

export interface ListPresetNamesRequest {
    owner: string;
    offset?: number;
    limit?: number;
    sort?: string;
    query?: string;
}

export interface ListPresetsRequest {
    owner: string;
    offset?: number;
    limit?: number;
    sort?: string;
    query?: string;
}

export interface PatchPresetRequest {
    owner: string;
    presetUuid: string;
    body: V1Preset;
}

export interface UpdatePresetRequest {
    owner: string;
    presetUuid: string;
    body: V1Preset;
}

/**
 * 
 */
export class PresetsV1Api extends runtime.BaseAPI {

    /**
     * Create scheduling presets
     */
    async createPresetRaw(requestParameters: CreatePresetRequest): Promise<runtime.ApiResponse<V1Preset>> {
        if (requestParameters.owner === null || requestParameters.owner === undefined) {
            throw new runtime.RequiredError('owner','Required parameter requestParameters.owner was null or undefined when calling createPreset.');
        }

        if (requestParameters.body === null || requestParameters.body === undefined) {
            throw new runtime.RequiredError('body','Required parameter requestParameters.body was null or undefined when calling createPreset.');
        }

        const queryParameters: runtime.HTTPQuery = {};

        const headerParameters: runtime.HTTPHeaders = {};

        headerParameters['Content-Type'] = 'application/json';

        if (this.configuration && this.configuration.apiKey) {
            headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // ApiKey authentication
        }

        const response = await this.request({
            path: `/api/v1/orgs/{owner}/presets`.replace(`{${"owner"}}`, encodeURIComponent(String(requestParameters.owner))),
            method: 'POST',
            headers: headerParameters,
            query: queryParameters,
            body: V1PresetToJSON(requestParameters.body),
        });

        return new runtime.JSONApiResponse(response, (jsonValue) => V1PresetFromJSON(jsonValue));
    }

    /**
     * Create scheduling presets
     */
    async createPreset(requestParameters: CreatePresetRequest): Promise<V1Preset> {
        const response = await this.createPresetRaw(requestParameters);
        return await response.value();
    }

    /**
     * Delete scheduling preset
     */
    async deletePresetRaw(requestParameters: DeletePresetRequest): Promise<runtime.ApiResponse<void>> {
        if (requestParameters.owner === null || requestParameters.owner === undefined) {
            throw new runtime.RequiredError('owner','Required parameter requestParameters.owner was null or undefined when calling deletePreset.');
        }

        if (requestParameters.uuid === null || requestParameters.uuid === undefined) {
            throw new runtime.RequiredError('uuid','Required parameter requestParameters.uuid was null or undefined when calling deletePreset.');
        }

        const queryParameters: runtime.HTTPQuery = {};

        const headerParameters: runtime.HTTPHeaders = {};

        if (this.configuration && this.configuration.apiKey) {
            headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // ApiKey authentication
        }

        const response = await this.request({
            path: `/api/v1/orgs/{owner}/presets/{uuid}`.replace(`{${"owner"}}`, encodeURIComponent(String(requestParameters.owner))).replace(`{${"uuid"}}`, encodeURIComponent(String(requestParameters.uuid))),
            method: 'DELETE',
            headers: headerParameters,
            query: queryParameters,
        });

        return new runtime.VoidApiResponse(response);
    }

    /**
     * Delete scheduling preset
     */
    async deletePreset(requestParameters: DeletePresetRequest): Promise<void> {
        await this.deletePresetRaw(requestParameters);
    }

    /**
     * Get scheduling preset
     */
    async getPresetRaw(requestParameters: GetPresetRequest): Promise<runtime.ApiResponse<V1Preset>> {
        if (requestParameters.owner === null || requestParameters.owner === undefined) {
            throw new runtime.RequiredError('owner','Required parameter requestParameters.owner was null or undefined when calling getPreset.');
        }

        if (requestParameters.uuid === null || requestParameters.uuid === undefined) {
            throw new runtime.RequiredError('uuid','Required parameter requestParameters.uuid was null or undefined when calling getPreset.');
        }

        const queryParameters: runtime.HTTPQuery = {};

        const headerParameters: runtime.HTTPHeaders = {};

        if (this.configuration && this.configuration.apiKey) {
            headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // ApiKey authentication
        }

        const response = await this.request({
            path: `/api/v1/orgs/{owner}/presets/{uuid}`.replace(`{${"owner"}}`, encodeURIComponent(String(requestParameters.owner))).replace(`{${"uuid"}}`, encodeURIComponent(String(requestParameters.uuid))),
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        });

        return new runtime.JSONApiResponse(response, (jsonValue) => V1PresetFromJSON(jsonValue));
    }

    /**
     * Get scheduling preset
     */
    async getPreset(requestParameters: GetPresetRequest): Promise<V1Preset> {
        const response = await this.getPresetRaw(requestParameters);
        return await response.value();
    }

    /**
     * List scheduling presets names
     */
    async listPresetNamesRaw(requestParameters: ListPresetNamesRequest): Promise<runtime.ApiResponse<V1ListPresetsResponse>> {
        if (requestParameters.owner === null || requestParameters.owner === undefined) {
            throw new runtime.RequiredError('owner','Required parameter requestParameters.owner was null or undefined when calling listPresetNames.');
        }

        const queryParameters: runtime.HTTPQuery = {};

        if (requestParameters.offset !== undefined) {
            queryParameters['offset'] = requestParameters.offset;
        }

        if (requestParameters.limit !== undefined) {
            queryParameters['limit'] = requestParameters.limit;
        }

        if (requestParameters.sort !== undefined) {
            queryParameters['sort'] = requestParameters.sort;
        }

        if (requestParameters.query !== undefined) {
            queryParameters['query'] = requestParameters.query;
        }

        const headerParameters: runtime.HTTPHeaders = {};

        if (this.configuration && this.configuration.apiKey) {
            headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // ApiKey authentication
        }

        const response = await this.request({
            path: `/api/v1/orgs/{owner}/presets/names`.replace(`{${"owner"}}`, encodeURIComponent(String(requestParameters.owner))),
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        });

        return new runtime.JSONApiResponse(response, (jsonValue) => V1ListPresetsResponseFromJSON(jsonValue));
    }

    /**
     * List scheduling presets names
     */
    async listPresetNames(requestParameters: ListPresetNamesRequest): Promise<V1ListPresetsResponse> {
        const response = await this.listPresetNamesRaw(requestParameters);
        return await response.value();
    }

    /**
     * List scheduling presets
     */
    async listPresetsRaw(requestParameters: ListPresetsRequest): Promise<runtime.ApiResponse<V1ListPresetsResponse>> {
        if (requestParameters.owner === null || requestParameters.owner === undefined) {
            throw new runtime.RequiredError('owner','Required parameter requestParameters.owner was null or undefined when calling listPresets.');
        }

        const queryParameters: runtime.HTTPQuery = {};

        if (requestParameters.offset !== undefined) {
            queryParameters['offset'] = requestParameters.offset;
        }

        if (requestParameters.limit !== undefined) {
            queryParameters['limit'] = requestParameters.limit;
        }

        if (requestParameters.sort !== undefined) {
            queryParameters['sort'] = requestParameters.sort;
        }

        if (requestParameters.query !== undefined) {
            queryParameters['query'] = requestParameters.query;
        }

        const headerParameters: runtime.HTTPHeaders = {};

        if (this.configuration && this.configuration.apiKey) {
            headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // ApiKey authentication
        }

        const response = await this.request({
            path: `/api/v1/orgs/{owner}/presets`.replace(`{${"owner"}}`, encodeURIComponent(String(requestParameters.owner))),
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        });

        return new runtime.JSONApiResponse(response, (jsonValue) => V1ListPresetsResponseFromJSON(jsonValue));
    }

    /**
     * List scheduling presets
     */
    async listPresets(requestParameters: ListPresetsRequest): Promise<V1ListPresetsResponse> {
        const response = await this.listPresetsRaw(requestParameters);
        return await response.value();
    }

    /**
     * Patch scheduling preset
     */
    async patchPresetRaw(requestParameters: PatchPresetRequest): Promise<runtime.ApiResponse<V1Preset>> {
        if (requestParameters.owner === null || requestParameters.owner === undefined) {
            throw new runtime.RequiredError('owner','Required parameter requestParameters.owner was null or undefined when calling patchPreset.');
        }

        if (requestParameters.presetUuid === null || requestParameters.presetUuid === undefined) {
            throw new runtime.RequiredError('presetUuid','Required parameter requestParameters.presetUuid was null or undefined when calling patchPreset.');
        }

        if (requestParameters.body === null || requestParameters.body === undefined) {
            throw new runtime.RequiredError('body','Required parameter requestParameters.body was null or undefined when calling patchPreset.');
        }

        const queryParameters: runtime.HTTPQuery = {};

        const headerParameters: runtime.HTTPHeaders = {};

        headerParameters['Content-Type'] = 'application/json';

        if (this.configuration && this.configuration.apiKey) {
            headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // ApiKey authentication
        }

        const response = await this.request({
            path: `/api/v1/orgs/{owner}/presets/{preset.uuid}`.replace(`{${"owner"}}`, encodeURIComponent(String(requestParameters.owner))).replace(`{${"preset.uuid"}}`, encodeURIComponent(String(requestParameters.presetUuid))),
            method: 'PATCH',
            headers: headerParameters,
            query: queryParameters,
            body: V1PresetToJSON(requestParameters.body),
        });

        return new runtime.JSONApiResponse(response, (jsonValue) => V1PresetFromJSON(jsonValue));
    }

    /**
     * Patch scheduling preset
     */
    async patchPreset(requestParameters: PatchPresetRequest): Promise<V1Preset> {
        const response = await this.patchPresetRaw(requestParameters);
        return await response.value();
    }

    /**
     * Update scheduling preset
     */
    async updatePresetRaw(requestParameters: UpdatePresetRequest): Promise<runtime.ApiResponse<V1Preset>> {
        if (requestParameters.owner === null || requestParameters.owner === undefined) {
            throw new runtime.RequiredError('owner','Required parameter requestParameters.owner was null or undefined when calling updatePreset.');
        }

        if (requestParameters.presetUuid === null || requestParameters.presetUuid === undefined) {
            throw new runtime.RequiredError('presetUuid','Required parameter requestParameters.presetUuid was null or undefined when calling updatePreset.');
        }

        if (requestParameters.body === null || requestParameters.body === undefined) {
            throw new runtime.RequiredError('body','Required parameter requestParameters.body was null or undefined when calling updatePreset.');
        }

        const queryParameters: runtime.HTTPQuery = {};

        const headerParameters: runtime.HTTPHeaders = {};

        headerParameters['Content-Type'] = 'application/json';

        if (this.configuration && this.configuration.apiKey) {
            headerParameters["Authorization"] = this.configuration.apiKey("Authorization"); // ApiKey authentication
        }

        const response = await this.request({
            path: `/api/v1/orgs/{owner}/presets/{preset.uuid}`.replace(`{${"owner"}}`, encodeURIComponent(String(requestParameters.owner))).replace(`{${"preset.uuid"}}`, encodeURIComponent(String(requestParameters.presetUuid))),
            method: 'PUT',
            headers: headerParameters,
            query: queryParameters,
            body: V1PresetToJSON(requestParameters.body),
        });

        return new runtime.JSONApiResponse(response, (jsonValue) => V1PresetFromJSON(jsonValue));
    }

    /**
     * Update scheduling preset
     */
    async updatePreset(requestParameters: UpdatePresetRequest): Promise<V1Preset> {
        const response = await this.updatePresetRaw(requestParameters);
        return await response.value();
    }

}