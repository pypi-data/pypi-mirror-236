"""
Type annotations for osis service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_osis/type_defs/)

Usage::

    ```python
    from types_aiobotocore_osis.type_defs import ChangeProgressStageTypeDef

    data: ChangeProgressStageTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import (
    ChangeProgressStageStatusesType,
    ChangeProgressStatusesType,
    PipelineStatusType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired
if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "ChangeProgressStageTypeDef",
    "CloudWatchLogDestinationTypeDef",
    "TagTypeDef",
    "VpcOptionsTypeDef",
    "ResponseMetadataTypeDef",
    "DeletePipelineRequestRequestTypeDef",
    "GetPipelineBlueprintRequestRequestTypeDef",
    "PipelineBlueprintTypeDef",
    "GetPipelineChangeProgressRequestRequestTypeDef",
    "GetPipelineRequestRequestTypeDef",
    "PipelineBlueprintSummaryTypeDef",
    "ListPipelinesRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "PipelineStatusReasonTypeDef",
    "StartPipelineRequestRequestTypeDef",
    "StopPipelineRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "ValidatePipelineRequestRequestTypeDef",
    "ValidationMessageTypeDef",
    "ChangeProgressStatusTypeDef",
    "LogPublishingOptionsTypeDef",
    "TagResourceRequestRequestTypeDef",
    "VpcEndpointTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "GetPipelineBlueprintResponseTypeDef",
    "ListPipelineBlueprintsResponseTypeDef",
    "PipelineSummaryTypeDef",
    "ValidatePipelineResponseTypeDef",
    "GetPipelineChangeProgressResponseTypeDef",
    "CreatePipelineRequestRequestTypeDef",
    "UpdatePipelineRequestRequestTypeDef",
    "PipelineTypeDef",
    "ListPipelinesResponseTypeDef",
    "CreatePipelineResponseTypeDef",
    "GetPipelineResponseTypeDef",
    "StartPipelineResponseTypeDef",
    "StopPipelineResponseTypeDef",
    "UpdatePipelineResponseTypeDef",
)

ChangeProgressStageTypeDef = TypedDict(
    "ChangeProgressStageTypeDef",
    {
        "Name": NotRequired[str],
        "Status": NotRequired[ChangeProgressStageStatusesType],
        "Description": NotRequired[str],
        "LastUpdatedAt": NotRequired[datetime],
    },
)

CloudWatchLogDestinationTypeDef = TypedDict(
    "CloudWatchLogDestinationTypeDef",
    {
        "LogGroup": str,
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

VpcOptionsTypeDef = TypedDict(
    "VpcOptionsTypeDef",
    {
        "SubnetIds": Sequence[str],
        "SecurityGroupIds": NotRequired[Sequence[str]],
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

DeletePipelineRequestRequestTypeDef = TypedDict(
    "DeletePipelineRequestRequestTypeDef",
    {
        "PipelineName": str,
    },
)

GetPipelineBlueprintRequestRequestTypeDef = TypedDict(
    "GetPipelineBlueprintRequestRequestTypeDef",
    {
        "BlueprintName": str,
    },
)

PipelineBlueprintTypeDef = TypedDict(
    "PipelineBlueprintTypeDef",
    {
        "BlueprintName": NotRequired[str],
        "PipelineConfigurationBody": NotRequired[str],
    },
)

GetPipelineChangeProgressRequestRequestTypeDef = TypedDict(
    "GetPipelineChangeProgressRequestRequestTypeDef",
    {
        "PipelineName": str,
    },
)

GetPipelineRequestRequestTypeDef = TypedDict(
    "GetPipelineRequestRequestTypeDef",
    {
        "PipelineName": str,
    },
)

PipelineBlueprintSummaryTypeDef = TypedDict(
    "PipelineBlueprintSummaryTypeDef",
    {
        "BlueprintName": NotRequired[str],
    },
)

ListPipelinesRequestRequestTypeDef = TypedDict(
    "ListPipelinesRequestRequestTypeDef",
    {
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "Arn": str,
    },
)

PipelineStatusReasonTypeDef = TypedDict(
    "PipelineStatusReasonTypeDef",
    {
        "Description": NotRequired[str],
    },
)

StartPipelineRequestRequestTypeDef = TypedDict(
    "StartPipelineRequestRequestTypeDef",
    {
        "PipelineName": str,
    },
)

StopPipelineRequestRequestTypeDef = TypedDict(
    "StopPipelineRequestRequestTypeDef",
    {
        "PipelineName": str,
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "Arn": str,
        "TagKeys": Sequence[str],
    },
)

ValidatePipelineRequestRequestTypeDef = TypedDict(
    "ValidatePipelineRequestRequestTypeDef",
    {
        "PipelineConfigurationBody": str,
    },
)

ValidationMessageTypeDef = TypedDict(
    "ValidationMessageTypeDef",
    {
        "Message": NotRequired[str],
    },
)

ChangeProgressStatusTypeDef = TypedDict(
    "ChangeProgressStatusTypeDef",
    {
        "StartTime": NotRequired[datetime],
        "Status": NotRequired[ChangeProgressStatusesType],
        "TotalNumberOfStages": NotRequired[int],
        "ChangeProgressStages": NotRequired[List[ChangeProgressStageTypeDef]],
    },
)

LogPublishingOptionsTypeDef = TypedDict(
    "LogPublishingOptionsTypeDef",
    {
        "IsLoggingEnabled": NotRequired[bool],
        "CloudWatchLogDestination": NotRequired[CloudWatchLogDestinationTypeDef],
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "Arn": str,
        "Tags": Sequence[TagTypeDef],
    },
)

VpcEndpointTypeDef = TypedDict(
    "VpcEndpointTypeDef",
    {
        "VpcEndpointId": NotRequired[str],
        "VpcId": NotRequired[str],
        "VpcOptions": NotRequired[VpcOptionsTypeDef],
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetPipelineBlueprintResponseTypeDef = TypedDict(
    "GetPipelineBlueprintResponseTypeDef",
    {
        "Blueprint": PipelineBlueprintTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListPipelineBlueprintsResponseTypeDef = TypedDict(
    "ListPipelineBlueprintsResponseTypeDef",
    {
        "Blueprints": List[PipelineBlueprintSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PipelineSummaryTypeDef = TypedDict(
    "PipelineSummaryTypeDef",
    {
        "Status": NotRequired[PipelineStatusType],
        "StatusReason": NotRequired[PipelineStatusReasonTypeDef],
        "PipelineName": NotRequired[str],
        "PipelineArn": NotRequired[str],
        "MinUnits": NotRequired[int],
        "MaxUnits": NotRequired[int],
        "CreatedAt": NotRequired[datetime],
        "LastUpdatedAt": NotRequired[datetime],
    },
)

ValidatePipelineResponseTypeDef = TypedDict(
    "ValidatePipelineResponseTypeDef",
    {
        "isValid": bool,
        "Errors": List[ValidationMessageTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetPipelineChangeProgressResponseTypeDef = TypedDict(
    "GetPipelineChangeProgressResponseTypeDef",
    {
        "ChangeProgressStatuses": List[ChangeProgressStatusTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreatePipelineRequestRequestTypeDef = TypedDict(
    "CreatePipelineRequestRequestTypeDef",
    {
        "PipelineName": str,
        "MinUnits": int,
        "MaxUnits": int,
        "PipelineConfigurationBody": str,
        "LogPublishingOptions": NotRequired[LogPublishingOptionsTypeDef],
        "VpcOptions": NotRequired[VpcOptionsTypeDef],
        "Tags": NotRequired[Sequence[TagTypeDef]],
    },
)

UpdatePipelineRequestRequestTypeDef = TypedDict(
    "UpdatePipelineRequestRequestTypeDef",
    {
        "PipelineName": str,
        "MinUnits": NotRequired[int],
        "MaxUnits": NotRequired[int],
        "PipelineConfigurationBody": NotRequired[str],
        "LogPublishingOptions": NotRequired[LogPublishingOptionsTypeDef],
    },
)

PipelineTypeDef = TypedDict(
    "PipelineTypeDef",
    {
        "PipelineName": NotRequired[str],
        "PipelineArn": NotRequired[str],
        "MinUnits": NotRequired[int],
        "MaxUnits": NotRequired[int],
        "Status": NotRequired[PipelineStatusType],
        "StatusReason": NotRequired[PipelineStatusReasonTypeDef],
        "PipelineConfigurationBody": NotRequired[str],
        "CreatedAt": NotRequired[datetime],
        "LastUpdatedAt": NotRequired[datetime],
        "IngestEndpointUrls": NotRequired[List[str]],
        "LogPublishingOptions": NotRequired[LogPublishingOptionsTypeDef],
        "VpcEndpoints": NotRequired[List[VpcEndpointTypeDef]],
    },
)

ListPipelinesResponseTypeDef = TypedDict(
    "ListPipelinesResponseTypeDef",
    {
        "NextToken": str,
        "Pipelines": List[PipelineSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreatePipelineResponseTypeDef = TypedDict(
    "CreatePipelineResponseTypeDef",
    {
        "Pipeline": PipelineTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetPipelineResponseTypeDef = TypedDict(
    "GetPipelineResponseTypeDef",
    {
        "Pipeline": PipelineTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartPipelineResponseTypeDef = TypedDict(
    "StartPipelineResponseTypeDef",
    {
        "Pipeline": PipelineTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StopPipelineResponseTypeDef = TypedDict(
    "StopPipelineResponseTypeDef",
    {
        "Pipeline": PipelineTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdatePipelineResponseTypeDef = TypedDict(
    "UpdatePipelineResponseTypeDef",
    {
        "Pipeline": PipelineTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
