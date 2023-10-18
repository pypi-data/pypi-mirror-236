"""
Type annotations for fis service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/type_defs/)

Usage::

    ```python
    from types_aiobotocore_fis.type_defs import ActionParameterTypeDef

    data: ActionParameterTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import ExperimentActionStatusType, ExperimentStatusType

if sys.version_info >= (3, 12):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired
if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "ActionParameterTypeDef",
    "ActionTargetTypeDef",
    "CreateExperimentTemplateActionInputTypeDef",
    "ExperimentTemplateCloudWatchLogsLogConfigurationInputTypeDef",
    "ExperimentTemplateS3LogConfigurationInputTypeDef",
    "CreateExperimentTemplateStopConditionInputTypeDef",
    "ResponseMetadataTypeDef",
    "ExperimentTemplateTargetInputFilterTypeDef",
    "DeleteExperimentTemplateRequestRequestTypeDef",
    "ExperimentActionStateTypeDef",
    "ExperimentCloudWatchLogsLogConfigurationTypeDef",
    "ExperimentS3LogConfigurationTypeDef",
    "ExperimentStateTypeDef",
    "ExperimentStopConditionTypeDef",
    "ExperimentTargetFilterTypeDef",
    "ExperimentTemplateActionTypeDef",
    "ExperimentTemplateCloudWatchLogsLogConfigurationTypeDef",
    "ExperimentTemplateS3LogConfigurationTypeDef",
    "ExperimentTemplateStopConditionTypeDef",
    "ExperimentTemplateSummaryTypeDef",
    "ExperimentTemplateTargetFilterTypeDef",
    "GetActionRequestRequestTypeDef",
    "GetExperimentRequestRequestTypeDef",
    "GetExperimentTemplateRequestRequestTypeDef",
    "GetTargetResourceTypeRequestRequestTypeDef",
    "ListActionsRequestRequestTypeDef",
    "ListExperimentTemplatesRequestRequestTypeDef",
    "ListExperimentsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTargetResourceTypesRequestRequestTypeDef",
    "TargetResourceTypeSummaryTypeDef",
    "StartExperimentRequestRequestTypeDef",
    "StopExperimentRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TargetResourceTypeParameterTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateExperimentTemplateActionInputItemTypeDef",
    "UpdateExperimentTemplateStopConditionInputTypeDef",
    "ActionSummaryTypeDef",
    "ActionTypeDef",
    "CreateExperimentTemplateLogConfigurationInputTypeDef",
    "UpdateExperimentTemplateLogConfigurationInputTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "CreateExperimentTemplateTargetInputTypeDef",
    "UpdateExperimentTemplateTargetInputTypeDef",
    "ExperimentActionTypeDef",
    "ExperimentLogConfigurationTypeDef",
    "ExperimentSummaryTypeDef",
    "ExperimentTargetTypeDef",
    "ExperimentTemplateLogConfigurationTypeDef",
    "ListExperimentTemplatesResponseTypeDef",
    "ExperimentTemplateTargetTypeDef",
    "ListTargetResourceTypesResponseTypeDef",
    "TargetResourceTypeTypeDef",
    "ListActionsResponseTypeDef",
    "GetActionResponseTypeDef",
    "CreateExperimentTemplateRequestRequestTypeDef",
    "UpdateExperimentTemplateRequestRequestTypeDef",
    "ListExperimentsResponseTypeDef",
    "ExperimentTypeDef",
    "ExperimentTemplateTypeDef",
    "GetTargetResourceTypeResponseTypeDef",
    "GetExperimentResponseTypeDef",
    "StartExperimentResponseTypeDef",
    "StopExperimentResponseTypeDef",
    "CreateExperimentTemplateResponseTypeDef",
    "DeleteExperimentTemplateResponseTypeDef",
    "GetExperimentTemplateResponseTypeDef",
    "UpdateExperimentTemplateResponseTypeDef",
)

ActionParameterTypeDef = TypedDict(
    "ActionParameterTypeDef",
    {
        "description": NotRequired[str],
        "required": NotRequired[bool],
    },
)

ActionTargetTypeDef = TypedDict(
    "ActionTargetTypeDef",
    {
        "resourceType": NotRequired[str],
    },
)

CreateExperimentTemplateActionInputTypeDef = TypedDict(
    "CreateExperimentTemplateActionInputTypeDef",
    {
        "actionId": str,
        "description": NotRequired[str],
        "parameters": NotRequired[Mapping[str, str]],
        "targets": NotRequired[Mapping[str, str]],
        "startAfter": NotRequired[Sequence[str]],
    },
)

ExperimentTemplateCloudWatchLogsLogConfigurationInputTypeDef = TypedDict(
    "ExperimentTemplateCloudWatchLogsLogConfigurationInputTypeDef",
    {
        "logGroupArn": str,
    },
)

ExperimentTemplateS3LogConfigurationInputTypeDef = TypedDict(
    "ExperimentTemplateS3LogConfigurationInputTypeDef",
    {
        "bucketName": str,
        "prefix": NotRequired[str],
    },
)

CreateExperimentTemplateStopConditionInputTypeDef = TypedDict(
    "CreateExperimentTemplateStopConditionInputTypeDef",
    {
        "source": str,
        "value": NotRequired[str],
    },
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

ExperimentTemplateTargetInputFilterTypeDef = TypedDict(
    "ExperimentTemplateTargetInputFilterTypeDef",
    {
        "path": str,
        "values": Sequence[str],
    },
)

DeleteExperimentTemplateRequestRequestTypeDef = TypedDict(
    "DeleteExperimentTemplateRequestRequestTypeDef",
    {
        "id": str,
    },
)

ExperimentActionStateTypeDef = TypedDict(
    "ExperimentActionStateTypeDef",
    {
        "status": NotRequired[ExperimentActionStatusType],
        "reason": NotRequired[str],
    },
)

ExperimentCloudWatchLogsLogConfigurationTypeDef = TypedDict(
    "ExperimentCloudWatchLogsLogConfigurationTypeDef",
    {
        "logGroupArn": NotRequired[str],
    },
)

ExperimentS3LogConfigurationTypeDef = TypedDict(
    "ExperimentS3LogConfigurationTypeDef",
    {
        "bucketName": NotRequired[str],
        "prefix": NotRequired[str],
    },
)

ExperimentStateTypeDef = TypedDict(
    "ExperimentStateTypeDef",
    {
        "status": NotRequired[ExperimentStatusType],
        "reason": NotRequired[str],
    },
)

ExperimentStopConditionTypeDef = TypedDict(
    "ExperimentStopConditionTypeDef",
    {
        "source": NotRequired[str],
        "value": NotRequired[str],
    },
)

ExperimentTargetFilterTypeDef = TypedDict(
    "ExperimentTargetFilterTypeDef",
    {
        "path": NotRequired[str],
        "values": NotRequired[List[str]],
    },
)

ExperimentTemplateActionTypeDef = TypedDict(
    "ExperimentTemplateActionTypeDef",
    {
        "actionId": NotRequired[str],
        "description": NotRequired[str],
        "parameters": NotRequired[Dict[str, str]],
        "targets": NotRequired[Dict[str, str]],
        "startAfter": NotRequired[List[str]],
    },
)

ExperimentTemplateCloudWatchLogsLogConfigurationTypeDef = TypedDict(
    "ExperimentTemplateCloudWatchLogsLogConfigurationTypeDef",
    {
        "logGroupArn": NotRequired[str],
    },
)

ExperimentTemplateS3LogConfigurationTypeDef = TypedDict(
    "ExperimentTemplateS3LogConfigurationTypeDef",
    {
        "bucketName": NotRequired[str],
        "prefix": NotRequired[str],
    },
)

ExperimentTemplateStopConditionTypeDef = TypedDict(
    "ExperimentTemplateStopConditionTypeDef",
    {
        "source": NotRequired[str],
        "value": NotRequired[str],
    },
)

ExperimentTemplateSummaryTypeDef = TypedDict(
    "ExperimentTemplateSummaryTypeDef",
    {
        "id": NotRequired[str],
        "description": NotRequired[str],
        "creationTime": NotRequired[datetime],
        "lastUpdateTime": NotRequired[datetime],
        "tags": NotRequired[Dict[str, str]],
    },
)

ExperimentTemplateTargetFilterTypeDef = TypedDict(
    "ExperimentTemplateTargetFilterTypeDef",
    {
        "path": NotRequired[str],
        "values": NotRequired[List[str]],
    },
)

GetActionRequestRequestTypeDef = TypedDict(
    "GetActionRequestRequestTypeDef",
    {
        "id": str,
    },
)

GetExperimentRequestRequestTypeDef = TypedDict(
    "GetExperimentRequestRequestTypeDef",
    {
        "id": str,
    },
)

GetExperimentTemplateRequestRequestTypeDef = TypedDict(
    "GetExperimentTemplateRequestRequestTypeDef",
    {
        "id": str,
    },
)

GetTargetResourceTypeRequestRequestTypeDef = TypedDict(
    "GetTargetResourceTypeRequestRequestTypeDef",
    {
        "resourceType": str,
    },
)

ListActionsRequestRequestTypeDef = TypedDict(
    "ListActionsRequestRequestTypeDef",
    {
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

ListExperimentTemplatesRequestRequestTypeDef = TypedDict(
    "ListExperimentTemplatesRequestRequestTypeDef",
    {
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

ListExperimentsRequestRequestTypeDef = TypedDict(
    "ListExperimentsRequestRequestTypeDef",
    {
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

ListTargetResourceTypesRequestRequestTypeDef = TypedDict(
    "ListTargetResourceTypesRequestRequestTypeDef",
    {
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

TargetResourceTypeSummaryTypeDef = TypedDict(
    "TargetResourceTypeSummaryTypeDef",
    {
        "resourceType": NotRequired[str],
        "description": NotRequired[str],
    },
)

StartExperimentRequestRequestTypeDef = TypedDict(
    "StartExperimentRequestRequestTypeDef",
    {
        "clientToken": str,
        "experimentTemplateId": str,
        "tags": NotRequired[Mapping[str, str]],
    },
)

StopExperimentRequestRequestTypeDef = TypedDict(
    "StopExperimentRequestRequestTypeDef",
    {
        "id": str,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)

TargetResourceTypeParameterTypeDef = TypedDict(
    "TargetResourceTypeParameterTypeDef",
    {
        "description": NotRequired[str],
        "required": NotRequired[bool],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": NotRequired[Sequence[str]],
    },
)

UpdateExperimentTemplateActionInputItemTypeDef = TypedDict(
    "UpdateExperimentTemplateActionInputItemTypeDef",
    {
        "actionId": NotRequired[str],
        "description": NotRequired[str],
        "parameters": NotRequired[Mapping[str, str]],
        "targets": NotRequired[Mapping[str, str]],
        "startAfter": NotRequired[Sequence[str]],
    },
)

UpdateExperimentTemplateStopConditionInputTypeDef = TypedDict(
    "UpdateExperimentTemplateStopConditionInputTypeDef",
    {
        "source": str,
        "value": NotRequired[str],
    },
)

ActionSummaryTypeDef = TypedDict(
    "ActionSummaryTypeDef",
    {
        "id": NotRequired[str],
        "description": NotRequired[str],
        "targets": NotRequired[Dict[str, ActionTargetTypeDef]],
        "tags": NotRequired[Dict[str, str]],
    },
)

ActionTypeDef = TypedDict(
    "ActionTypeDef",
    {
        "id": NotRequired[str],
        "description": NotRequired[str],
        "parameters": NotRequired[Dict[str, ActionParameterTypeDef]],
        "targets": NotRequired[Dict[str, ActionTargetTypeDef]],
        "tags": NotRequired[Dict[str, str]],
    },
)

CreateExperimentTemplateLogConfigurationInputTypeDef = TypedDict(
    "CreateExperimentTemplateLogConfigurationInputTypeDef",
    {
        "logSchemaVersion": int,
        "cloudWatchLogsConfiguration": NotRequired[
            ExperimentTemplateCloudWatchLogsLogConfigurationInputTypeDef
        ],
        "s3Configuration": NotRequired[ExperimentTemplateS3LogConfigurationInputTypeDef],
    },
)

UpdateExperimentTemplateLogConfigurationInputTypeDef = TypedDict(
    "UpdateExperimentTemplateLogConfigurationInputTypeDef",
    {
        "cloudWatchLogsConfiguration": NotRequired[
            ExperimentTemplateCloudWatchLogsLogConfigurationInputTypeDef
        ],
        "s3Configuration": NotRequired[ExperimentTemplateS3LogConfigurationInputTypeDef],
        "logSchemaVersion": NotRequired[int],
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateExperimentTemplateTargetInputTypeDef = TypedDict(
    "CreateExperimentTemplateTargetInputTypeDef",
    {
        "resourceType": str,
        "selectionMode": str,
        "resourceArns": NotRequired[Sequence[str]],
        "resourceTags": NotRequired[Mapping[str, str]],
        "filters": NotRequired[Sequence[ExperimentTemplateTargetInputFilterTypeDef]],
        "parameters": NotRequired[Mapping[str, str]],
    },
)

UpdateExperimentTemplateTargetInputTypeDef = TypedDict(
    "UpdateExperimentTemplateTargetInputTypeDef",
    {
        "resourceType": str,
        "selectionMode": str,
        "resourceArns": NotRequired[Sequence[str]],
        "resourceTags": NotRequired[Mapping[str, str]],
        "filters": NotRequired[Sequence[ExperimentTemplateTargetInputFilterTypeDef]],
        "parameters": NotRequired[Mapping[str, str]],
    },
)

ExperimentActionTypeDef = TypedDict(
    "ExperimentActionTypeDef",
    {
        "actionId": NotRequired[str],
        "description": NotRequired[str],
        "parameters": NotRequired[Dict[str, str]],
        "targets": NotRequired[Dict[str, str]],
        "startAfter": NotRequired[List[str]],
        "state": NotRequired[ExperimentActionStateTypeDef],
        "startTime": NotRequired[datetime],
        "endTime": NotRequired[datetime],
    },
)

ExperimentLogConfigurationTypeDef = TypedDict(
    "ExperimentLogConfigurationTypeDef",
    {
        "cloudWatchLogsConfiguration": NotRequired[ExperimentCloudWatchLogsLogConfigurationTypeDef],
        "s3Configuration": NotRequired[ExperimentS3LogConfigurationTypeDef],
        "logSchemaVersion": NotRequired[int],
    },
)

ExperimentSummaryTypeDef = TypedDict(
    "ExperimentSummaryTypeDef",
    {
        "id": NotRequired[str],
        "experimentTemplateId": NotRequired[str],
        "state": NotRequired[ExperimentStateTypeDef],
        "creationTime": NotRequired[datetime],
        "tags": NotRequired[Dict[str, str]],
    },
)

ExperimentTargetTypeDef = TypedDict(
    "ExperimentTargetTypeDef",
    {
        "resourceType": NotRequired[str],
        "resourceArns": NotRequired[List[str]],
        "resourceTags": NotRequired[Dict[str, str]],
        "filters": NotRequired[List[ExperimentTargetFilterTypeDef]],
        "selectionMode": NotRequired[str],
        "parameters": NotRequired[Dict[str, str]],
    },
)

ExperimentTemplateLogConfigurationTypeDef = TypedDict(
    "ExperimentTemplateLogConfigurationTypeDef",
    {
        "cloudWatchLogsConfiguration": NotRequired[
            ExperimentTemplateCloudWatchLogsLogConfigurationTypeDef
        ],
        "s3Configuration": NotRequired[ExperimentTemplateS3LogConfigurationTypeDef],
        "logSchemaVersion": NotRequired[int],
    },
)

ListExperimentTemplatesResponseTypeDef = TypedDict(
    "ListExperimentTemplatesResponseTypeDef",
    {
        "experimentTemplates": List[ExperimentTemplateSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ExperimentTemplateTargetTypeDef = TypedDict(
    "ExperimentTemplateTargetTypeDef",
    {
        "resourceType": NotRequired[str],
        "resourceArns": NotRequired[List[str]],
        "resourceTags": NotRequired[Dict[str, str]],
        "filters": NotRequired[List[ExperimentTemplateTargetFilterTypeDef]],
        "selectionMode": NotRequired[str],
        "parameters": NotRequired[Dict[str, str]],
    },
)

ListTargetResourceTypesResponseTypeDef = TypedDict(
    "ListTargetResourceTypesResponseTypeDef",
    {
        "targetResourceTypes": List[TargetResourceTypeSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TargetResourceTypeTypeDef = TypedDict(
    "TargetResourceTypeTypeDef",
    {
        "resourceType": NotRequired[str],
        "description": NotRequired[str],
        "parameters": NotRequired[Dict[str, TargetResourceTypeParameterTypeDef]],
    },
)

ListActionsResponseTypeDef = TypedDict(
    "ListActionsResponseTypeDef",
    {
        "actions": List[ActionSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetActionResponseTypeDef = TypedDict(
    "GetActionResponseTypeDef",
    {
        "action": ActionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateExperimentTemplateRequestRequestTypeDef = TypedDict(
    "CreateExperimentTemplateRequestRequestTypeDef",
    {
        "clientToken": str,
        "description": str,
        "stopConditions": Sequence[CreateExperimentTemplateStopConditionInputTypeDef],
        "actions": Mapping[str, CreateExperimentTemplateActionInputTypeDef],
        "roleArn": str,
        "targets": NotRequired[Mapping[str, CreateExperimentTemplateTargetInputTypeDef]],
        "tags": NotRequired[Mapping[str, str]],
        "logConfiguration": NotRequired[CreateExperimentTemplateLogConfigurationInputTypeDef],
    },
)

UpdateExperimentTemplateRequestRequestTypeDef = TypedDict(
    "UpdateExperimentTemplateRequestRequestTypeDef",
    {
        "id": str,
        "description": NotRequired[str],
        "stopConditions": NotRequired[Sequence[UpdateExperimentTemplateStopConditionInputTypeDef]],
        "targets": NotRequired[Mapping[str, UpdateExperimentTemplateTargetInputTypeDef]],
        "actions": NotRequired[Mapping[str, UpdateExperimentTemplateActionInputItemTypeDef]],
        "roleArn": NotRequired[str],
        "logConfiguration": NotRequired[UpdateExperimentTemplateLogConfigurationInputTypeDef],
    },
)

ListExperimentsResponseTypeDef = TypedDict(
    "ListExperimentsResponseTypeDef",
    {
        "experiments": List[ExperimentSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ExperimentTypeDef = TypedDict(
    "ExperimentTypeDef",
    {
        "id": NotRequired[str],
        "experimentTemplateId": NotRequired[str],
        "roleArn": NotRequired[str],
        "state": NotRequired[ExperimentStateTypeDef],
        "targets": NotRequired[Dict[str, ExperimentTargetTypeDef]],
        "actions": NotRequired[Dict[str, ExperimentActionTypeDef]],
        "stopConditions": NotRequired[List[ExperimentStopConditionTypeDef]],
        "creationTime": NotRequired[datetime],
        "startTime": NotRequired[datetime],
        "endTime": NotRequired[datetime],
        "tags": NotRequired[Dict[str, str]],
        "logConfiguration": NotRequired[ExperimentLogConfigurationTypeDef],
    },
)

ExperimentTemplateTypeDef = TypedDict(
    "ExperimentTemplateTypeDef",
    {
        "id": NotRequired[str],
        "description": NotRequired[str],
        "targets": NotRequired[Dict[str, ExperimentTemplateTargetTypeDef]],
        "actions": NotRequired[Dict[str, ExperimentTemplateActionTypeDef]],
        "stopConditions": NotRequired[List[ExperimentTemplateStopConditionTypeDef]],
        "creationTime": NotRequired[datetime],
        "lastUpdateTime": NotRequired[datetime],
        "roleArn": NotRequired[str],
        "tags": NotRequired[Dict[str, str]],
        "logConfiguration": NotRequired[ExperimentTemplateLogConfigurationTypeDef],
    },
)

GetTargetResourceTypeResponseTypeDef = TypedDict(
    "GetTargetResourceTypeResponseTypeDef",
    {
        "targetResourceType": TargetResourceTypeTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetExperimentResponseTypeDef = TypedDict(
    "GetExperimentResponseTypeDef",
    {
        "experiment": ExperimentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartExperimentResponseTypeDef = TypedDict(
    "StartExperimentResponseTypeDef",
    {
        "experiment": ExperimentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StopExperimentResponseTypeDef = TypedDict(
    "StopExperimentResponseTypeDef",
    {
        "experiment": ExperimentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateExperimentTemplateResponseTypeDef = TypedDict(
    "CreateExperimentTemplateResponseTypeDef",
    {
        "experimentTemplate": ExperimentTemplateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteExperimentTemplateResponseTypeDef = TypedDict(
    "DeleteExperimentTemplateResponseTypeDef",
    {
        "experimentTemplate": ExperimentTemplateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetExperimentTemplateResponseTypeDef = TypedDict(
    "GetExperimentTemplateResponseTypeDef",
    {
        "experimentTemplate": ExperimentTemplateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateExperimentTemplateResponseTypeDef = TypedDict(
    "UpdateExperimentTemplateResponseTypeDef",
    {
        "experimentTemplate": ExperimentTemplateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
