"""
Type annotations for gamesparks service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_gamesparks/type_defs/)

Usage::

    ```python
    from types_aiobotocore_gamesparks.type_defs import BlobTypeDef

    data: BlobTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from aiobotocore.response import StreamingBody

from .literals import (
    DeploymentActionType,
    DeploymentStateType,
    GameStateType,
    GeneratedCodeJobStateType,
    OperationType,
    ResultCodeType,
    StageStateType,
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
    "BlobTypeDef",
    "ConnectionTypeDef",
    "CreateGameRequestRequestTypeDef",
    "GameDetailsTypeDef",
    "ResponseMetadataTypeDef",
    "CreateSnapshotRequestRequestTypeDef",
    "CreateStageRequestRequestTypeDef",
    "StageDetailsTypeDef",
    "DeleteGameRequestRequestTypeDef",
    "DeleteStageRequestRequestTypeDef",
    "DeploymentResultTypeDef",
    "DisconnectPlayerRequestRequestTypeDef",
    "ExportSnapshotRequestRequestTypeDef",
    "ExtensionDetailsTypeDef",
    "ExtensionVersionDetailsTypeDef",
    "SectionTypeDef",
    "GameSummaryTypeDef",
    "GeneratedCodeJobDetailsTypeDef",
    "GeneratorTypeDef",
    "GetExtensionRequestRequestTypeDef",
    "GetExtensionVersionRequestRequestTypeDef",
    "GetGameConfigurationRequestRequestTypeDef",
    "GetGameRequestRequestTypeDef",
    "GetGeneratedCodeJobRequestRequestTypeDef",
    "GetPlayerConnectionStatusRequestRequestTypeDef",
    "GetSnapshotRequestRequestTypeDef",
    "GetStageDeploymentRequestRequestTypeDef",
    "GetStageRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ListExtensionVersionsRequestRequestTypeDef",
    "ListExtensionsRequestRequestTypeDef",
    "ListGamesRequestRequestTypeDef",
    "ListGeneratedCodeJobsRequestRequestTypeDef",
    "ListSnapshotsRequestRequestTypeDef",
    "SnapshotSummaryTypeDef",
    "ListStageDeploymentsRequestRequestTypeDef",
    "ListStagesRequestRequestTypeDef",
    "StageSummaryTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "SectionModificationTypeDef",
    "StartStageDeploymentRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateGameRequestRequestTypeDef",
    "UpdateSnapshotRequestRequestTypeDef",
    "UpdateStageRequestRequestTypeDef",
    "ImportGameConfigurationSourceTypeDef",
    "CreateGameResultTypeDef",
    "DisconnectPlayerResultTypeDef",
    "ExportSnapshotResultTypeDef",
    "GetGameResultTypeDef",
    "GetPlayerConnectionStatusResultTypeDef",
    "ListTagsForResourceResultTypeDef",
    "StartGeneratedCodeJobResultTypeDef",
    "UpdateGameResultTypeDef",
    "CreateStageResultTypeDef",
    "GetStageResultTypeDef",
    "UpdateStageResultTypeDef",
    "StageDeploymentDetailsTypeDef",
    "StageDeploymentSummaryTypeDef",
    "GetExtensionResultTypeDef",
    "ListExtensionsResultTypeDef",
    "GetExtensionVersionResultTypeDef",
    "ListExtensionVersionsResultTypeDef",
    "GameConfigurationDetailsTypeDef",
    "SnapshotDetailsTypeDef",
    "ListGamesResultTypeDef",
    "GetGeneratedCodeJobResultTypeDef",
    "ListGeneratedCodeJobsResultTypeDef",
    "StartGeneratedCodeJobRequestRequestTypeDef",
    "ListExtensionVersionsRequestListExtensionVersionsPaginateTypeDef",
    "ListExtensionsRequestListExtensionsPaginateTypeDef",
    "ListGamesRequestListGamesPaginateTypeDef",
    "ListGeneratedCodeJobsRequestListGeneratedCodeJobsPaginateTypeDef",
    "ListSnapshotsRequestListSnapshotsPaginateTypeDef",
    "ListStageDeploymentsRequestListStageDeploymentsPaginateTypeDef",
    "ListStagesRequestListStagesPaginateTypeDef",
    "ListSnapshotsResultTypeDef",
    "ListStagesResultTypeDef",
    "UpdateGameConfigurationRequestRequestTypeDef",
    "ImportGameConfigurationRequestRequestTypeDef",
    "GetStageDeploymentResultTypeDef",
    "StartStageDeploymentResultTypeDef",
    "ListStageDeploymentsResultTypeDef",
    "GetGameConfigurationResultTypeDef",
    "ImportGameConfigurationResultTypeDef",
    "UpdateGameConfigurationResultTypeDef",
    "CreateSnapshotResultTypeDef",
    "GetSnapshotResultTypeDef",
    "UpdateSnapshotResultTypeDef",
)

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]
ConnectionTypeDef = TypedDict(
    "ConnectionTypeDef",
    {
        "Created": NotRequired[datetime],
        "Id": NotRequired[str],
    },
)

CreateGameRequestRequestTypeDef = TypedDict(
    "CreateGameRequestRequestTypeDef",
    {
        "GameName": str,
        "ClientToken": NotRequired[str],
        "Description": NotRequired[str],
        "Tags": NotRequired[Mapping[str, str]],
    },
)

GameDetailsTypeDef = TypedDict(
    "GameDetailsTypeDef",
    {
        "Arn": NotRequired[str],
        "Created": NotRequired[datetime],
        "Description": NotRequired[str],
        "EnableTerminationProtection": NotRequired[bool],
        "LastUpdated": NotRequired[datetime],
        "Name": NotRequired[str],
        "State": NotRequired[GameStateType],
        "Tags": NotRequired[Dict[str, str]],
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

CreateSnapshotRequestRequestTypeDef = TypedDict(
    "CreateSnapshotRequestRequestTypeDef",
    {
        "GameName": str,
        "Description": NotRequired[str],
    },
)

CreateStageRequestRequestTypeDef = TypedDict(
    "CreateStageRequestRequestTypeDef",
    {
        "GameName": str,
        "Role": str,
        "StageName": str,
        "ClientToken": NotRequired[str],
        "Description": NotRequired[str],
        "Tags": NotRequired[Mapping[str, str]],
    },
)

StageDetailsTypeDef = TypedDict(
    "StageDetailsTypeDef",
    {
        "Arn": NotRequired[str],
        "Created": NotRequired[datetime],
        "Description": NotRequired[str],
        "GameKey": NotRequired[str],
        "LastUpdated": NotRequired[datetime],
        "LogGroup": NotRequired[str],
        "Name": NotRequired[str],
        "Role": NotRequired[str],
        "State": NotRequired[StageStateType],
        "Tags": NotRequired[Dict[str, str]],
    },
)

DeleteGameRequestRequestTypeDef = TypedDict(
    "DeleteGameRequestRequestTypeDef",
    {
        "GameName": str,
    },
)

DeleteStageRequestRequestTypeDef = TypedDict(
    "DeleteStageRequestRequestTypeDef",
    {
        "GameName": str,
        "StageName": str,
    },
)

DeploymentResultTypeDef = TypedDict(
    "DeploymentResultTypeDef",
    {
        "Message": NotRequired[str],
        "ResultCode": NotRequired[ResultCodeType],
    },
)

DisconnectPlayerRequestRequestTypeDef = TypedDict(
    "DisconnectPlayerRequestRequestTypeDef",
    {
        "GameName": str,
        "PlayerId": str,
        "StageName": str,
    },
)

ExportSnapshotRequestRequestTypeDef = TypedDict(
    "ExportSnapshotRequestRequestTypeDef",
    {
        "GameName": str,
        "SnapshotId": str,
    },
)

ExtensionDetailsTypeDef = TypedDict(
    "ExtensionDetailsTypeDef",
    {
        "Description": NotRequired[str],
        "Name": NotRequired[str],
        "Namespace": NotRequired[str],
    },
)

ExtensionVersionDetailsTypeDef = TypedDict(
    "ExtensionVersionDetailsTypeDef",
    {
        "Name": NotRequired[str],
        "Namespace": NotRequired[str],
        "Schema": NotRequired[str],
        "Version": NotRequired[str],
    },
)

SectionTypeDef = TypedDict(
    "SectionTypeDef",
    {
        "Attributes": NotRequired[Dict[str, Any]],
        "Name": NotRequired[str],
        "Size": NotRequired[int],
    },
)

GameSummaryTypeDef = TypedDict(
    "GameSummaryTypeDef",
    {
        "Description": NotRequired[str],
        "Name": NotRequired[str],
        "State": NotRequired[GameStateType],
        "Tags": NotRequired[Dict[str, str]],
    },
)

GeneratedCodeJobDetailsTypeDef = TypedDict(
    "GeneratedCodeJobDetailsTypeDef",
    {
        "Description": NotRequired[str],
        "ExpirationTime": NotRequired[datetime],
        "GeneratedCodeJobId": NotRequired[str],
        "S3Url": NotRequired[str],
        "Status": NotRequired[GeneratedCodeJobStateType],
    },
)

GeneratorTypeDef = TypedDict(
    "GeneratorTypeDef",
    {
        "GameSdkVersion": NotRequired[str],
        "Language": NotRequired[str],
        "TargetPlatform": NotRequired[str],
    },
)

GetExtensionRequestRequestTypeDef = TypedDict(
    "GetExtensionRequestRequestTypeDef",
    {
        "Name": str,
        "Namespace": str,
    },
)

GetExtensionVersionRequestRequestTypeDef = TypedDict(
    "GetExtensionVersionRequestRequestTypeDef",
    {
        "ExtensionVersion": str,
        "Name": str,
        "Namespace": str,
    },
)

GetGameConfigurationRequestRequestTypeDef = TypedDict(
    "GetGameConfigurationRequestRequestTypeDef",
    {
        "GameName": str,
        "Sections": NotRequired[Sequence[str]],
    },
)

GetGameRequestRequestTypeDef = TypedDict(
    "GetGameRequestRequestTypeDef",
    {
        "GameName": str,
    },
)

GetGeneratedCodeJobRequestRequestTypeDef = TypedDict(
    "GetGeneratedCodeJobRequestRequestTypeDef",
    {
        "GameName": str,
        "JobId": str,
        "SnapshotId": str,
    },
)

GetPlayerConnectionStatusRequestRequestTypeDef = TypedDict(
    "GetPlayerConnectionStatusRequestRequestTypeDef",
    {
        "GameName": str,
        "PlayerId": str,
        "StageName": str,
    },
)

GetSnapshotRequestRequestTypeDef = TypedDict(
    "GetSnapshotRequestRequestTypeDef",
    {
        "GameName": str,
        "SnapshotId": str,
        "Sections": NotRequired[Sequence[str]],
    },
)

GetStageDeploymentRequestRequestTypeDef = TypedDict(
    "GetStageDeploymentRequestRequestTypeDef",
    {
        "GameName": str,
        "StageName": str,
        "DeploymentId": NotRequired[str],
    },
)

GetStageRequestRequestTypeDef = TypedDict(
    "GetStageRequestRequestTypeDef",
    {
        "GameName": str,
        "StageName": str,
    },
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": NotRequired[int],
        "PageSize": NotRequired[int],
        "StartingToken": NotRequired[str],
    },
)

ListExtensionVersionsRequestRequestTypeDef = TypedDict(
    "ListExtensionVersionsRequestRequestTypeDef",
    {
        "Name": str,
        "Namespace": str,
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

ListExtensionsRequestRequestTypeDef = TypedDict(
    "ListExtensionsRequestRequestTypeDef",
    {
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

ListGamesRequestRequestTypeDef = TypedDict(
    "ListGamesRequestRequestTypeDef",
    {
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

ListGeneratedCodeJobsRequestRequestTypeDef = TypedDict(
    "ListGeneratedCodeJobsRequestRequestTypeDef",
    {
        "GameName": str,
        "SnapshotId": str,
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

ListSnapshotsRequestRequestTypeDef = TypedDict(
    "ListSnapshotsRequestRequestTypeDef",
    {
        "GameName": str,
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

SnapshotSummaryTypeDef = TypedDict(
    "SnapshotSummaryTypeDef",
    {
        "Created": NotRequired[datetime],
        "Description": NotRequired[str],
        "Id": NotRequired[str],
        "LastUpdated": NotRequired[datetime],
    },
)

ListStageDeploymentsRequestRequestTypeDef = TypedDict(
    "ListStageDeploymentsRequestRequestTypeDef",
    {
        "GameName": str,
        "StageName": str,
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

ListStagesRequestRequestTypeDef = TypedDict(
    "ListStagesRequestRequestTypeDef",
    {
        "GameName": str,
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

StageSummaryTypeDef = TypedDict(
    "StageSummaryTypeDef",
    {
        "Description": NotRequired[str],
        "GameKey": NotRequired[str],
        "Name": NotRequired[str],
        "State": NotRequired[StageStateType],
        "Tags": NotRequired[Dict[str, str]],
    },
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

SectionModificationTypeDef = TypedDict(
    "SectionModificationTypeDef",
    {
        "Operation": OperationType,
        "Path": str,
        "Section": str,
        "Value": NotRequired[Mapping[str, Any]],
    },
)

StartStageDeploymentRequestRequestTypeDef = TypedDict(
    "StartStageDeploymentRequestRequestTypeDef",
    {
        "GameName": str,
        "SnapshotId": str,
        "StageName": str,
        "ClientToken": NotRequired[str],
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "tagKeys": Sequence[str],
    },
)

UpdateGameRequestRequestTypeDef = TypedDict(
    "UpdateGameRequestRequestTypeDef",
    {
        "GameName": str,
        "Description": NotRequired[str],
    },
)

UpdateSnapshotRequestRequestTypeDef = TypedDict(
    "UpdateSnapshotRequestRequestTypeDef",
    {
        "GameName": str,
        "SnapshotId": str,
        "Description": NotRequired[str],
    },
)

UpdateStageRequestRequestTypeDef = TypedDict(
    "UpdateStageRequestRequestTypeDef",
    {
        "GameName": str,
        "StageName": str,
        "Description": NotRequired[str],
        "Role": NotRequired[str],
    },
)

ImportGameConfigurationSourceTypeDef = TypedDict(
    "ImportGameConfigurationSourceTypeDef",
    {
        "File": BlobTypeDef,
    },
)

CreateGameResultTypeDef = TypedDict(
    "CreateGameResultTypeDef",
    {
        "Game": GameDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DisconnectPlayerResultTypeDef = TypedDict(
    "DisconnectPlayerResultTypeDef",
    {
        "DisconnectFailures": List[str],
        "DisconnectSuccesses": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ExportSnapshotResultTypeDef = TypedDict(
    "ExportSnapshotResultTypeDef",
    {
        "S3Url": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetGameResultTypeDef = TypedDict(
    "GetGameResultTypeDef",
    {
        "Game": GameDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetPlayerConnectionStatusResultTypeDef = TypedDict(
    "GetPlayerConnectionStatusResultTypeDef",
    {
        "Connections": List[ConnectionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResultTypeDef = TypedDict(
    "ListTagsForResourceResultTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartGeneratedCodeJobResultTypeDef = TypedDict(
    "StartGeneratedCodeJobResultTypeDef",
    {
        "GeneratedCodeJobId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateGameResultTypeDef = TypedDict(
    "UpdateGameResultTypeDef",
    {
        "Game": GameDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateStageResultTypeDef = TypedDict(
    "CreateStageResultTypeDef",
    {
        "Stage": StageDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetStageResultTypeDef = TypedDict(
    "GetStageResultTypeDef",
    {
        "Stage": StageDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateStageResultTypeDef = TypedDict(
    "UpdateStageResultTypeDef",
    {
        "Stage": StageDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StageDeploymentDetailsTypeDef = TypedDict(
    "StageDeploymentDetailsTypeDef",
    {
        "Created": NotRequired[datetime],
        "DeploymentAction": NotRequired[DeploymentActionType],
        "DeploymentId": NotRequired[str],
        "DeploymentResult": NotRequired[DeploymentResultTypeDef],
        "DeploymentState": NotRequired[DeploymentStateType],
        "LastUpdated": NotRequired[datetime],
        "SnapshotId": NotRequired[str],
    },
)

StageDeploymentSummaryTypeDef = TypedDict(
    "StageDeploymentSummaryTypeDef",
    {
        "DeploymentAction": NotRequired[DeploymentActionType],
        "DeploymentId": NotRequired[str],
        "DeploymentResult": NotRequired[DeploymentResultTypeDef],
        "DeploymentState": NotRequired[DeploymentStateType],
        "LastUpdated": NotRequired[datetime],
        "SnapshotId": NotRequired[str],
    },
)

GetExtensionResultTypeDef = TypedDict(
    "GetExtensionResultTypeDef",
    {
        "Extension": ExtensionDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListExtensionsResultTypeDef = TypedDict(
    "ListExtensionsResultTypeDef",
    {
        "Extensions": List[ExtensionDetailsTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetExtensionVersionResultTypeDef = TypedDict(
    "GetExtensionVersionResultTypeDef",
    {
        "ExtensionVersion": ExtensionVersionDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListExtensionVersionsResultTypeDef = TypedDict(
    "ListExtensionVersionsResultTypeDef",
    {
        "ExtensionVersions": List[ExtensionVersionDetailsTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GameConfigurationDetailsTypeDef = TypedDict(
    "GameConfigurationDetailsTypeDef",
    {
        "Created": NotRequired[datetime],
        "LastUpdated": NotRequired[datetime],
        "Sections": NotRequired[Dict[str, SectionTypeDef]],
    },
)

SnapshotDetailsTypeDef = TypedDict(
    "SnapshotDetailsTypeDef",
    {
        "Created": NotRequired[datetime],
        "Description": NotRequired[str],
        "Id": NotRequired[str],
        "LastUpdated": NotRequired[datetime],
        "Sections": NotRequired[Dict[str, SectionTypeDef]],
    },
)

ListGamesResultTypeDef = TypedDict(
    "ListGamesResultTypeDef",
    {
        "Games": List[GameSummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetGeneratedCodeJobResultTypeDef = TypedDict(
    "GetGeneratedCodeJobResultTypeDef",
    {
        "GeneratedCodeJob": GeneratedCodeJobDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListGeneratedCodeJobsResultTypeDef = TypedDict(
    "ListGeneratedCodeJobsResultTypeDef",
    {
        "GeneratedCodeJobs": List[GeneratedCodeJobDetailsTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartGeneratedCodeJobRequestRequestTypeDef = TypedDict(
    "StartGeneratedCodeJobRequestRequestTypeDef",
    {
        "GameName": str,
        "Generator": GeneratorTypeDef,
        "SnapshotId": str,
    },
)

ListExtensionVersionsRequestListExtensionVersionsPaginateTypeDef = TypedDict(
    "ListExtensionVersionsRequestListExtensionVersionsPaginateTypeDef",
    {
        "Name": str,
        "Namespace": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListExtensionsRequestListExtensionsPaginateTypeDef = TypedDict(
    "ListExtensionsRequestListExtensionsPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListGamesRequestListGamesPaginateTypeDef = TypedDict(
    "ListGamesRequestListGamesPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListGeneratedCodeJobsRequestListGeneratedCodeJobsPaginateTypeDef = TypedDict(
    "ListGeneratedCodeJobsRequestListGeneratedCodeJobsPaginateTypeDef",
    {
        "GameName": str,
        "SnapshotId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListSnapshotsRequestListSnapshotsPaginateTypeDef = TypedDict(
    "ListSnapshotsRequestListSnapshotsPaginateTypeDef",
    {
        "GameName": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListStageDeploymentsRequestListStageDeploymentsPaginateTypeDef = TypedDict(
    "ListStageDeploymentsRequestListStageDeploymentsPaginateTypeDef",
    {
        "GameName": str,
        "StageName": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListStagesRequestListStagesPaginateTypeDef = TypedDict(
    "ListStagesRequestListStagesPaginateTypeDef",
    {
        "GameName": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListSnapshotsResultTypeDef = TypedDict(
    "ListSnapshotsResultTypeDef",
    {
        "NextToken": str,
        "Snapshots": List[SnapshotSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListStagesResultTypeDef = TypedDict(
    "ListStagesResultTypeDef",
    {
        "NextToken": str,
        "Stages": List[StageSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateGameConfigurationRequestRequestTypeDef = TypedDict(
    "UpdateGameConfigurationRequestRequestTypeDef",
    {
        "GameName": str,
        "Modifications": Sequence[SectionModificationTypeDef],
    },
)

ImportGameConfigurationRequestRequestTypeDef = TypedDict(
    "ImportGameConfigurationRequestRequestTypeDef",
    {
        "GameName": str,
        "ImportSource": ImportGameConfigurationSourceTypeDef,
    },
)

GetStageDeploymentResultTypeDef = TypedDict(
    "GetStageDeploymentResultTypeDef",
    {
        "StageDeployment": StageDeploymentDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartStageDeploymentResultTypeDef = TypedDict(
    "StartStageDeploymentResultTypeDef",
    {
        "StageDeployment": StageDeploymentDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListStageDeploymentsResultTypeDef = TypedDict(
    "ListStageDeploymentsResultTypeDef",
    {
        "NextToken": str,
        "StageDeployments": List[StageDeploymentSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetGameConfigurationResultTypeDef = TypedDict(
    "GetGameConfigurationResultTypeDef",
    {
        "GameConfiguration": GameConfigurationDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ImportGameConfigurationResultTypeDef = TypedDict(
    "ImportGameConfigurationResultTypeDef",
    {
        "GameConfiguration": GameConfigurationDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateGameConfigurationResultTypeDef = TypedDict(
    "UpdateGameConfigurationResultTypeDef",
    {
        "GameConfiguration": GameConfigurationDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateSnapshotResultTypeDef = TypedDict(
    "CreateSnapshotResultTypeDef",
    {
        "Snapshot": SnapshotDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSnapshotResultTypeDef = TypedDict(
    "GetSnapshotResultTypeDef",
    {
        "Snapshot": SnapshotDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateSnapshotResultTypeDef = TypedDict(
    "UpdateSnapshotResultTypeDef",
    {
        "Snapshot": SnapshotDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
