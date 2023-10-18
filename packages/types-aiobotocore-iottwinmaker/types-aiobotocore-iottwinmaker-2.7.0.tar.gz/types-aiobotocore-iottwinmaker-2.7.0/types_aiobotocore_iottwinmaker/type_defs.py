"""
Type annotations for iottwinmaker service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iottwinmaker/type_defs/)

Usage::

    ```python
    from types_aiobotocore_iottwinmaker.type_defs import ResponseMetadataTypeDef

    data: ResponseMetadataTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    ColumnTypeType,
    ComponentUpdateTypeType,
    ErrorCodeType,
    OrderByTimeType,
    OrderType,
    ParentEntityUpdateTypeType,
    PricingModeType,
    PricingTierType,
    PropertyGroupUpdateTypeType,
    PropertyUpdateTypeType,
    ScopeType,
    StateType,
    SyncJobStateType,
    SyncResourceStateType,
    SyncResourceTypeType,
    TypeType,
    UpdateReasonType,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 12):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired
if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "ResponseMetadataTypeDef",
    "BundleInformationTypeDef",
    "ColumnDescriptionTypeDef",
    "ComponentPropertyGroupRequestTypeDef",
    "ComponentPropertyGroupResponseTypeDef",
    "PropertyDefinitionRequestTypeDef",
    "PropertyGroupRequestTypeDef",
    "CreateSceneRequestRequestTypeDef",
    "CreateSyncJobRequestRequestTypeDef",
    "CreateWorkspaceRequestRequestTypeDef",
    "LambdaFunctionTypeDef",
    "RelationshipTypeDef",
    "RelationshipValueTypeDef",
    "DeleteComponentTypeRequestRequestTypeDef",
    "DeleteEntityRequestRequestTypeDef",
    "DeleteSceneRequestRequestTypeDef",
    "DeleteSyncJobRequestRequestTypeDef",
    "DeleteWorkspaceRequestRequestTypeDef",
    "EntityPropertyReferenceTypeDef",
    "ErrorDetailsTypeDef",
    "ExecuteQueryRequestRequestTypeDef",
    "RowTypeDef",
    "GetComponentTypeRequestRequestTypeDef",
    "PropertyDefinitionResponseTypeDef",
    "PropertyGroupResponseTypeDef",
    "GetEntityRequestRequestTypeDef",
    "InterpolationParametersTypeDef",
    "PropertyFilterTypeDef",
    "TimestampTypeDef",
    "GetSceneRequestRequestTypeDef",
    "SceneErrorTypeDef",
    "GetSyncJobRequestRequestTypeDef",
    "GetWorkspaceRequestRequestTypeDef",
    "ListComponentTypesFilterTypeDef",
    "ListEntitiesFilterTypeDef",
    "ListScenesRequestRequestTypeDef",
    "SceneSummaryTypeDef",
    "ListSyncJobsRequestRequestTypeDef",
    "SyncResourceFilterTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListWorkspacesRequestRequestTypeDef",
    "WorkspaceSummaryTypeDef",
    "OrderByTypeDef",
    "ParentEntityUpdateRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdatePricingPlanRequestRequestTypeDef",
    "UpdateSceneRequestRequestTypeDef",
    "UpdateWorkspaceRequestRequestTypeDef",
    "CreateComponentTypeResponseTypeDef",
    "CreateEntityResponseTypeDef",
    "CreateSceneResponseTypeDef",
    "CreateSyncJobResponseTypeDef",
    "CreateWorkspaceResponseTypeDef",
    "DeleteComponentTypeResponseTypeDef",
    "DeleteEntityResponseTypeDef",
    "DeleteSyncJobResponseTypeDef",
    "GetWorkspaceResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "UpdateComponentTypeResponseTypeDef",
    "UpdateEntityResponseTypeDef",
    "UpdateSceneResponseTypeDef",
    "UpdateWorkspaceResponseTypeDef",
    "PricingPlanTypeDef",
    "PropertyRequestTypeDef",
    "DataConnectorTypeDef",
    "DataTypeTypeDef",
    "DataValueTypeDef",
    "PropertyLatestValueTypeDef",
    "StatusTypeDef",
    "SyncJobStatusTypeDef",
    "SyncResourceStatusTypeDef",
    "ExecuteQueryResponseTypeDef",
    "PropertyResponseTypeDef",
    "GetPropertyValueHistoryRequestRequestTypeDef",
    "PropertyValueTypeDef",
    "GetSceneResponseTypeDef",
    "ListComponentTypesRequestRequestTypeDef",
    "ListEntitiesRequestRequestTypeDef",
    "ListScenesResponseTypeDef",
    "ListSyncResourcesRequestRequestTypeDef",
    "ListWorkspacesResponseTypeDef",
    "TabularConditionsTypeDef",
    "GetPricingPlanResponseTypeDef",
    "UpdatePricingPlanResponseTypeDef",
    "ComponentRequestTypeDef",
    "ComponentUpdateRequestTypeDef",
    "FunctionRequestTypeDef",
    "FunctionResponseTypeDef",
    "GetPropertyValueResponseTypeDef",
    "ComponentTypeSummaryTypeDef",
    "EntitySummaryTypeDef",
    "GetSyncJobResponseTypeDef",
    "SyncJobSummaryTypeDef",
    "SyncResourceSummaryTypeDef",
    "ComponentResponseTypeDef",
    "PropertyValueEntryTypeDef",
    "PropertyValueHistoryTypeDef",
    "GetPropertyValueRequestRequestTypeDef",
    "CreateEntityRequestRequestTypeDef",
    "UpdateEntityRequestRequestTypeDef",
    "CreateComponentTypeRequestRequestTypeDef",
    "UpdateComponentTypeRequestRequestTypeDef",
    "GetComponentTypeResponseTypeDef",
    "ListComponentTypesResponseTypeDef",
    "ListEntitiesResponseTypeDef",
    "ListSyncJobsResponseTypeDef",
    "ListSyncResourcesResponseTypeDef",
    "GetEntityResponseTypeDef",
    "BatchPutPropertyErrorTypeDef",
    "BatchPutPropertyValuesRequestRequestTypeDef",
    "GetPropertyValueHistoryResponseTypeDef",
    "BatchPutPropertyErrorEntryTypeDef",
    "BatchPutPropertyValuesResponseTypeDef",
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

BundleInformationTypeDef = TypedDict(
    "BundleInformationTypeDef",
    {
        "bundleNames": List[str],
        "pricingTier": NotRequired[PricingTierType],
    },
)

ColumnDescriptionTypeDef = TypedDict(
    "ColumnDescriptionTypeDef",
    {
        "name": NotRequired[str],
        "type": NotRequired[ColumnTypeType],
    },
)

ComponentPropertyGroupRequestTypeDef = TypedDict(
    "ComponentPropertyGroupRequestTypeDef",
    {
        "groupType": NotRequired[Literal["TABULAR"]],
        "propertyNames": NotRequired[Sequence[str]],
        "updateType": NotRequired[PropertyGroupUpdateTypeType],
    },
)

ComponentPropertyGroupResponseTypeDef = TypedDict(
    "ComponentPropertyGroupResponseTypeDef",
    {
        "groupType": Literal["TABULAR"],
        "propertyNames": List[str],
        "isInherited": bool,
    },
)

PropertyDefinitionRequestTypeDef = TypedDict(
    "PropertyDefinitionRequestTypeDef",
    {
        "dataType": NotRequired["DataTypeTypeDef"],
        "isRequiredInEntity": NotRequired[bool],
        "isExternalId": NotRequired[bool],
        "isStoredExternally": NotRequired[bool],
        "isTimeSeries": NotRequired[bool],
        "defaultValue": NotRequired["DataValueTypeDef"],
        "configuration": NotRequired[Mapping[str, str]],
        "displayName": NotRequired[str],
    },
)

PropertyGroupRequestTypeDef = TypedDict(
    "PropertyGroupRequestTypeDef",
    {
        "groupType": NotRequired[Literal["TABULAR"]],
        "propertyNames": NotRequired[Sequence[str]],
    },
)

CreateSceneRequestRequestTypeDef = TypedDict(
    "CreateSceneRequestRequestTypeDef",
    {
        "workspaceId": str,
        "sceneId": str,
        "contentLocation": str,
        "description": NotRequired[str],
        "capabilities": NotRequired[Sequence[str]],
        "tags": NotRequired[Mapping[str, str]],
        "sceneMetadata": NotRequired[Mapping[str, str]],
    },
)

CreateSyncJobRequestRequestTypeDef = TypedDict(
    "CreateSyncJobRequestRequestTypeDef",
    {
        "workspaceId": str,
        "syncSource": str,
        "syncRole": str,
        "tags": NotRequired[Mapping[str, str]],
    },
)

CreateWorkspaceRequestRequestTypeDef = TypedDict(
    "CreateWorkspaceRequestRequestTypeDef",
    {
        "workspaceId": str,
        "s3Location": str,
        "role": str,
        "description": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)

LambdaFunctionTypeDef = TypedDict(
    "LambdaFunctionTypeDef",
    {
        "arn": str,
    },
)

RelationshipTypeDef = TypedDict(
    "RelationshipTypeDef",
    {
        "targetComponentTypeId": NotRequired[str],
        "relationshipType": NotRequired[str],
    },
)

RelationshipValueTypeDef = TypedDict(
    "RelationshipValueTypeDef",
    {
        "targetEntityId": NotRequired[str],
        "targetComponentName": NotRequired[str],
    },
)

DeleteComponentTypeRequestRequestTypeDef = TypedDict(
    "DeleteComponentTypeRequestRequestTypeDef",
    {
        "workspaceId": str,
        "componentTypeId": str,
    },
)

DeleteEntityRequestRequestTypeDef = TypedDict(
    "DeleteEntityRequestRequestTypeDef",
    {
        "workspaceId": str,
        "entityId": str,
        "isRecursive": NotRequired[bool],
    },
)

DeleteSceneRequestRequestTypeDef = TypedDict(
    "DeleteSceneRequestRequestTypeDef",
    {
        "workspaceId": str,
        "sceneId": str,
    },
)

DeleteSyncJobRequestRequestTypeDef = TypedDict(
    "DeleteSyncJobRequestRequestTypeDef",
    {
        "workspaceId": str,
        "syncSource": str,
    },
)

DeleteWorkspaceRequestRequestTypeDef = TypedDict(
    "DeleteWorkspaceRequestRequestTypeDef",
    {
        "workspaceId": str,
    },
)

EntityPropertyReferenceTypeDef = TypedDict(
    "EntityPropertyReferenceTypeDef",
    {
        "propertyName": str,
        "componentName": NotRequired[str],
        "externalIdProperty": NotRequired[Mapping[str, str]],
        "entityId": NotRequired[str],
    },
)

ErrorDetailsTypeDef = TypedDict(
    "ErrorDetailsTypeDef",
    {
        "code": NotRequired[ErrorCodeType],
        "message": NotRequired[str],
    },
)

ExecuteQueryRequestRequestTypeDef = TypedDict(
    "ExecuteQueryRequestRequestTypeDef",
    {
        "workspaceId": str,
        "queryStatement": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

RowTypeDef = TypedDict(
    "RowTypeDef",
    {
        "rowData": NotRequired[List[Dict[str, Any]]],
    },
)

GetComponentTypeRequestRequestTypeDef = TypedDict(
    "GetComponentTypeRequestRequestTypeDef",
    {
        "workspaceId": str,
        "componentTypeId": str,
    },
)

PropertyDefinitionResponseTypeDef = TypedDict(
    "PropertyDefinitionResponseTypeDef",
    {
        "dataType": "DataTypeTypeDef",
        "isTimeSeries": bool,
        "isRequiredInEntity": bool,
        "isExternalId": bool,
        "isStoredExternally": bool,
        "isImported": bool,
        "isFinal": bool,
        "isInherited": bool,
        "defaultValue": NotRequired["DataValueTypeDef"],
        "configuration": NotRequired[Dict[str, str]],
        "displayName": NotRequired[str],
    },
)

PropertyGroupResponseTypeDef = TypedDict(
    "PropertyGroupResponseTypeDef",
    {
        "groupType": Literal["TABULAR"],
        "propertyNames": List[str],
        "isInherited": bool,
    },
)

GetEntityRequestRequestTypeDef = TypedDict(
    "GetEntityRequestRequestTypeDef",
    {
        "workspaceId": str,
        "entityId": str,
    },
)

InterpolationParametersTypeDef = TypedDict(
    "InterpolationParametersTypeDef",
    {
        "interpolationType": NotRequired[Literal["LINEAR"]],
        "intervalInSeconds": NotRequired[int],
    },
)

PropertyFilterTypeDef = TypedDict(
    "PropertyFilterTypeDef",
    {
        "propertyName": NotRequired[str],
        "operator": NotRequired[str],
        "value": NotRequired["DataValueTypeDef"],
    },
)

TimestampTypeDef = Union[datetime, str]
GetSceneRequestRequestTypeDef = TypedDict(
    "GetSceneRequestRequestTypeDef",
    {
        "workspaceId": str,
        "sceneId": str,
    },
)

SceneErrorTypeDef = TypedDict(
    "SceneErrorTypeDef",
    {
        "code": NotRequired[Literal["MATTERPORT_ERROR"]],
        "message": NotRequired[str],
    },
)

GetSyncJobRequestRequestTypeDef = TypedDict(
    "GetSyncJobRequestRequestTypeDef",
    {
        "syncSource": str,
        "workspaceId": NotRequired[str],
    },
)

GetWorkspaceRequestRequestTypeDef = TypedDict(
    "GetWorkspaceRequestRequestTypeDef",
    {
        "workspaceId": str,
    },
)

ListComponentTypesFilterTypeDef = TypedDict(
    "ListComponentTypesFilterTypeDef",
    {
        "extendsFrom": NotRequired[str],
        "namespace": NotRequired[str],
        "isAbstract": NotRequired[bool],
    },
)

ListEntitiesFilterTypeDef = TypedDict(
    "ListEntitiesFilterTypeDef",
    {
        "parentEntityId": NotRequired[str],
        "componentTypeId": NotRequired[str],
        "externalId": NotRequired[str],
    },
)

ListScenesRequestRequestTypeDef = TypedDict(
    "ListScenesRequestRequestTypeDef",
    {
        "workspaceId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

SceneSummaryTypeDef = TypedDict(
    "SceneSummaryTypeDef",
    {
        "sceneId": str,
        "contentLocation": str,
        "arn": str,
        "creationDateTime": datetime,
        "updateDateTime": datetime,
        "description": NotRequired[str],
    },
)

ListSyncJobsRequestRequestTypeDef = TypedDict(
    "ListSyncJobsRequestRequestTypeDef",
    {
        "workspaceId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

SyncResourceFilterTypeDef = TypedDict(
    "SyncResourceFilterTypeDef",
    {
        "state": NotRequired[SyncResourceStateType],
        "resourceType": NotRequired[SyncResourceTypeType],
        "resourceId": NotRequired[str],
        "externalId": NotRequired[str],
    },
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceARN": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

ListWorkspacesRequestRequestTypeDef = TypedDict(
    "ListWorkspacesRequestRequestTypeDef",
    {
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

WorkspaceSummaryTypeDef = TypedDict(
    "WorkspaceSummaryTypeDef",
    {
        "workspaceId": str,
        "arn": str,
        "creationDateTime": datetime,
        "updateDateTime": datetime,
        "description": NotRequired[str],
    },
)

OrderByTypeDef = TypedDict(
    "OrderByTypeDef",
    {
        "propertyName": str,
        "order": NotRequired[OrderType],
    },
)

ParentEntityUpdateRequestTypeDef = TypedDict(
    "ParentEntityUpdateRequestTypeDef",
    {
        "updateType": ParentEntityUpdateTypeType,
        "parentEntityId": NotRequired[str],
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceARN": str,
        "tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceARN": str,
        "tagKeys": Sequence[str],
    },
)

UpdatePricingPlanRequestRequestTypeDef = TypedDict(
    "UpdatePricingPlanRequestRequestTypeDef",
    {
        "pricingMode": PricingModeType,
        "bundleNames": NotRequired[Sequence[str]],
    },
)

UpdateSceneRequestRequestTypeDef = TypedDict(
    "UpdateSceneRequestRequestTypeDef",
    {
        "workspaceId": str,
        "sceneId": str,
        "contentLocation": NotRequired[str],
        "description": NotRequired[str],
        "capabilities": NotRequired[Sequence[str]],
        "sceneMetadata": NotRequired[Mapping[str, str]],
    },
)

UpdateWorkspaceRequestRequestTypeDef = TypedDict(
    "UpdateWorkspaceRequestRequestTypeDef",
    {
        "workspaceId": str,
        "description": NotRequired[str],
        "role": NotRequired[str],
    },
)

CreateComponentTypeResponseTypeDef = TypedDict(
    "CreateComponentTypeResponseTypeDef",
    {
        "arn": str,
        "creationDateTime": datetime,
        "state": StateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateEntityResponseTypeDef = TypedDict(
    "CreateEntityResponseTypeDef",
    {
        "entityId": str,
        "arn": str,
        "creationDateTime": datetime,
        "state": StateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateSceneResponseTypeDef = TypedDict(
    "CreateSceneResponseTypeDef",
    {
        "arn": str,
        "creationDateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateSyncJobResponseTypeDef = TypedDict(
    "CreateSyncJobResponseTypeDef",
    {
        "arn": str,
        "creationDateTime": datetime,
        "state": SyncJobStateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateWorkspaceResponseTypeDef = TypedDict(
    "CreateWorkspaceResponseTypeDef",
    {
        "arn": str,
        "creationDateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteComponentTypeResponseTypeDef = TypedDict(
    "DeleteComponentTypeResponseTypeDef",
    {
        "state": StateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteEntityResponseTypeDef = TypedDict(
    "DeleteEntityResponseTypeDef",
    {
        "state": StateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteSyncJobResponseTypeDef = TypedDict(
    "DeleteSyncJobResponseTypeDef",
    {
        "state": SyncJobStateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetWorkspaceResponseTypeDef = TypedDict(
    "GetWorkspaceResponseTypeDef",
    {
        "workspaceId": str,
        "arn": str,
        "description": str,
        "s3Location": str,
        "role": str,
        "creationDateTime": datetime,
        "updateDateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateComponentTypeResponseTypeDef = TypedDict(
    "UpdateComponentTypeResponseTypeDef",
    {
        "workspaceId": str,
        "arn": str,
        "componentTypeId": str,
        "state": StateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateEntityResponseTypeDef = TypedDict(
    "UpdateEntityResponseTypeDef",
    {
        "updateDateTime": datetime,
        "state": StateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateSceneResponseTypeDef = TypedDict(
    "UpdateSceneResponseTypeDef",
    {
        "updateDateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateWorkspaceResponseTypeDef = TypedDict(
    "UpdateWorkspaceResponseTypeDef",
    {
        "updateDateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PricingPlanTypeDef = TypedDict(
    "PricingPlanTypeDef",
    {
        "effectiveDateTime": datetime,
        "pricingMode": PricingModeType,
        "updateDateTime": datetime,
        "updateReason": UpdateReasonType,
        "billableEntityCount": NotRequired[int],
        "bundleInformation": NotRequired[BundleInformationTypeDef],
    },
)

PropertyRequestTypeDef = TypedDict(
    "PropertyRequestTypeDef",
    {
        "definition": NotRequired[PropertyDefinitionRequestTypeDef],
        "value": NotRequired["DataValueTypeDef"],
        "updateType": NotRequired[PropertyUpdateTypeType],
    },
)

DataConnectorTypeDef = TypedDict(
    "DataConnectorTypeDef",
    {
        "lambda": NotRequired[LambdaFunctionTypeDef],
        "isNative": NotRequired[bool],
    },
)

DataTypeTypeDef = TypedDict(
    "DataTypeTypeDef",
    {
        "type": TypeType,
        "nestedType": NotRequired[Dict[str, Any]],
        "allowedValues": NotRequired[Sequence["DataValueTypeDef"]],
        "unitOfMeasure": NotRequired[str],
        "relationship": NotRequired[RelationshipTypeDef],
    },
)

DataValueTypeDef = TypedDict(
    "DataValueTypeDef",
    {
        "booleanValue": NotRequired[bool],
        "doubleValue": NotRequired[float],
        "integerValue": NotRequired[int],
        "longValue": NotRequired[int],
        "stringValue": NotRequired[str],
        "listValue": NotRequired[Sequence[Dict[str, Any]]],
        "mapValue": NotRequired[Mapping[str, Dict[str, Any]]],
        "relationshipValue": NotRequired[RelationshipValueTypeDef],
        "expression": NotRequired[str],
    },
)

PropertyLatestValueTypeDef = TypedDict(
    "PropertyLatestValueTypeDef",
    {
        "propertyReference": EntityPropertyReferenceTypeDef,
        "propertyValue": NotRequired["DataValueTypeDef"],
    },
)

StatusTypeDef = TypedDict(
    "StatusTypeDef",
    {
        "state": NotRequired[StateType],
        "error": NotRequired[ErrorDetailsTypeDef],
    },
)

SyncJobStatusTypeDef = TypedDict(
    "SyncJobStatusTypeDef",
    {
        "state": NotRequired[SyncJobStateType],
        "error": NotRequired[ErrorDetailsTypeDef],
    },
)

SyncResourceStatusTypeDef = TypedDict(
    "SyncResourceStatusTypeDef",
    {
        "state": NotRequired[SyncResourceStateType],
        "error": NotRequired[ErrorDetailsTypeDef],
    },
)

ExecuteQueryResponseTypeDef = TypedDict(
    "ExecuteQueryResponseTypeDef",
    {
        "columnDescriptions": List[ColumnDescriptionTypeDef],
        "rows": List[RowTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PropertyResponseTypeDef = TypedDict(
    "PropertyResponseTypeDef",
    {
        "definition": NotRequired[PropertyDefinitionResponseTypeDef],
        "value": NotRequired["DataValueTypeDef"],
    },
)

GetPropertyValueHistoryRequestRequestTypeDef = TypedDict(
    "GetPropertyValueHistoryRequestRequestTypeDef",
    {
        "workspaceId": str,
        "selectedProperties": Sequence[str],
        "entityId": NotRequired[str],
        "componentName": NotRequired[str],
        "componentTypeId": NotRequired[str],
        "propertyFilters": NotRequired[Sequence[PropertyFilterTypeDef]],
        "startDateTime": NotRequired[TimestampTypeDef],
        "endDateTime": NotRequired[TimestampTypeDef],
        "interpolation": NotRequired[InterpolationParametersTypeDef],
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
        "orderByTime": NotRequired[OrderByTimeType],
        "startTime": NotRequired[str],
        "endTime": NotRequired[str],
    },
)

PropertyValueTypeDef = TypedDict(
    "PropertyValueTypeDef",
    {
        "value": "DataValueTypeDef",
        "timestamp": NotRequired[TimestampTypeDef],
        "time": NotRequired[str],
    },
)

GetSceneResponseTypeDef = TypedDict(
    "GetSceneResponseTypeDef",
    {
        "workspaceId": str,
        "sceneId": str,
        "contentLocation": str,
        "arn": str,
        "creationDateTime": datetime,
        "updateDateTime": datetime,
        "description": str,
        "capabilities": List[str],
        "sceneMetadata": Dict[str, str],
        "generatedSceneMetadata": Dict[str, str],
        "error": SceneErrorTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListComponentTypesRequestRequestTypeDef = TypedDict(
    "ListComponentTypesRequestRequestTypeDef",
    {
        "workspaceId": str,
        "filters": NotRequired[Sequence[ListComponentTypesFilterTypeDef]],
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)

ListEntitiesRequestRequestTypeDef = TypedDict(
    "ListEntitiesRequestRequestTypeDef",
    {
        "workspaceId": str,
        "filters": NotRequired[Sequence[ListEntitiesFilterTypeDef]],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

ListScenesResponseTypeDef = TypedDict(
    "ListScenesResponseTypeDef",
    {
        "sceneSummaries": List[SceneSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSyncResourcesRequestRequestTypeDef = TypedDict(
    "ListSyncResourcesRequestRequestTypeDef",
    {
        "workspaceId": str,
        "syncSource": str,
        "filters": NotRequired[Sequence[SyncResourceFilterTypeDef]],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

ListWorkspacesResponseTypeDef = TypedDict(
    "ListWorkspacesResponseTypeDef",
    {
        "workspaceSummaries": List[WorkspaceSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TabularConditionsTypeDef = TypedDict(
    "TabularConditionsTypeDef",
    {
        "orderBy": NotRequired[Sequence[OrderByTypeDef]],
        "propertyFilters": NotRequired[Sequence[PropertyFilterTypeDef]],
    },
)

GetPricingPlanResponseTypeDef = TypedDict(
    "GetPricingPlanResponseTypeDef",
    {
        "currentPricingPlan": PricingPlanTypeDef,
        "pendingPricingPlan": PricingPlanTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdatePricingPlanResponseTypeDef = TypedDict(
    "UpdatePricingPlanResponseTypeDef",
    {
        "currentPricingPlan": PricingPlanTypeDef,
        "pendingPricingPlan": PricingPlanTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ComponentRequestTypeDef = TypedDict(
    "ComponentRequestTypeDef",
    {
        "description": NotRequired[str],
        "componentTypeId": NotRequired[str],
        "properties": NotRequired[Mapping[str, PropertyRequestTypeDef]],
        "propertyGroups": NotRequired[Mapping[str, ComponentPropertyGroupRequestTypeDef]],
    },
)

ComponentUpdateRequestTypeDef = TypedDict(
    "ComponentUpdateRequestTypeDef",
    {
        "updateType": NotRequired[ComponentUpdateTypeType],
        "description": NotRequired[str],
        "componentTypeId": NotRequired[str],
        "propertyUpdates": NotRequired[Mapping[str, PropertyRequestTypeDef]],
        "propertyGroupUpdates": NotRequired[Mapping[str, ComponentPropertyGroupRequestTypeDef]],
    },
)

FunctionRequestTypeDef = TypedDict(
    "FunctionRequestTypeDef",
    {
        "requiredProperties": NotRequired[Sequence[str]],
        "scope": NotRequired[ScopeType],
        "implementedBy": NotRequired[DataConnectorTypeDef],
    },
)

FunctionResponseTypeDef = TypedDict(
    "FunctionResponseTypeDef",
    {
        "requiredProperties": NotRequired[List[str]],
        "scope": NotRequired[ScopeType],
        "implementedBy": NotRequired[DataConnectorTypeDef],
        "isInherited": NotRequired[bool],
    },
)

GetPropertyValueResponseTypeDef = TypedDict(
    "GetPropertyValueResponseTypeDef",
    {
        "propertyValues": Dict[str, PropertyLatestValueTypeDef],
        "nextToken": str,
        "tabularPropertyValues": List[List[Dict[str, "DataValueTypeDef"]]],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ComponentTypeSummaryTypeDef = TypedDict(
    "ComponentTypeSummaryTypeDef",
    {
        "arn": str,
        "componentTypeId": str,
        "creationDateTime": datetime,
        "updateDateTime": datetime,
        "description": NotRequired[str],
        "status": NotRequired[StatusTypeDef],
        "componentTypeName": NotRequired[str],
    },
)

EntitySummaryTypeDef = TypedDict(
    "EntitySummaryTypeDef",
    {
        "entityId": str,
        "entityName": str,
        "arn": str,
        "status": StatusTypeDef,
        "creationDateTime": datetime,
        "updateDateTime": datetime,
        "parentEntityId": NotRequired[str],
        "description": NotRequired[str],
        "hasChildEntities": NotRequired[bool],
    },
)

GetSyncJobResponseTypeDef = TypedDict(
    "GetSyncJobResponseTypeDef",
    {
        "arn": str,
        "workspaceId": str,
        "syncSource": str,
        "syncRole": str,
        "status": SyncJobStatusTypeDef,
        "creationDateTime": datetime,
        "updateDateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SyncJobSummaryTypeDef = TypedDict(
    "SyncJobSummaryTypeDef",
    {
        "arn": NotRequired[str],
        "workspaceId": NotRequired[str],
        "syncSource": NotRequired[str],
        "status": NotRequired[SyncJobStatusTypeDef],
        "creationDateTime": NotRequired[datetime],
        "updateDateTime": NotRequired[datetime],
    },
)

SyncResourceSummaryTypeDef = TypedDict(
    "SyncResourceSummaryTypeDef",
    {
        "resourceType": NotRequired[SyncResourceTypeType],
        "externalId": NotRequired[str],
        "resourceId": NotRequired[str],
        "status": NotRequired[SyncResourceStatusTypeDef],
        "updateDateTime": NotRequired[datetime],
    },
)

ComponentResponseTypeDef = TypedDict(
    "ComponentResponseTypeDef",
    {
        "componentName": NotRequired[str],
        "description": NotRequired[str],
        "componentTypeId": NotRequired[str],
        "status": NotRequired[StatusTypeDef],
        "definedIn": NotRequired[str],
        "properties": NotRequired[Dict[str, PropertyResponseTypeDef]],
        "propertyGroups": NotRequired[Dict[str, ComponentPropertyGroupResponseTypeDef]],
        "syncSource": NotRequired[str],
    },
)

PropertyValueEntryTypeDef = TypedDict(
    "PropertyValueEntryTypeDef",
    {
        "entityPropertyReference": EntityPropertyReferenceTypeDef,
        "propertyValues": NotRequired[Sequence[PropertyValueTypeDef]],
    },
)

PropertyValueHistoryTypeDef = TypedDict(
    "PropertyValueHistoryTypeDef",
    {
        "entityPropertyReference": EntityPropertyReferenceTypeDef,
        "values": NotRequired[List[PropertyValueTypeDef]],
    },
)

GetPropertyValueRequestRequestTypeDef = TypedDict(
    "GetPropertyValueRequestRequestTypeDef",
    {
        "selectedProperties": Sequence[str],
        "workspaceId": str,
        "componentName": NotRequired[str],
        "componentTypeId": NotRequired[str],
        "entityId": NotRequired[str],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "propertyGroupName": NotRequired[str],
        "tabularConditions": NotRequired[TabularConditionsTypeDef],
    },
)

CreateEntityRequestRequestTypeDef = TypedDict(
    "CreateEntityRequestRequestTypeDef",
    {
        "workspaceId": str,
        "entityName": str,
        "entityId": NotRequired[str],
        "description": NotRequired[str],
        "components": NotRequired[Mapping[str, ComponentRequestTypeDef]],
        "parentEntityId": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)

UpdateEntityRequestRequestTypeDef = TypedDict(
    "UpdateEntityRequestRequestTypeDef",
    {
        "workspaceId": str,
        "entityId": str,
        "entityName": NotRequired[str],
        "description": NotRequired[str],
        "componentUpdates": NotRequired[Mapping[str, ComponentUpdateRequestTypeDef]],
        "parentEntityUpdate": NotRequired[ParentEntityUpdateRequestTypeDef],
    },
)

CreateComponentTypeRequestRequestTypeDef = TypedDict(
    "CreateComponentTypeRequestRequestTypeDef",
    {
        "workspaceId": str,
        "componentTypeId": str,
        "isSingleton": NotRequired[bool],
        "description": NotRequired[str],
        "propertyDefinitions": NotRequired[Mapping[str, PropertyDefinitionRequestTypeDef]],
        "extendsFrom": NotRequired[Sequence[str]],
        "functions": NotRequired[Mapping[str, FunctionRequestTypeDef]],
        "tags": NotRequired[Mapping[str, str]],
        "propertyGroups": NotRequired[Mapping[str, PropertyGroupRequestTypeDef]],
        "componentTypeName": NotRequired[str],
    },
)

UpdateComponentTypeRequestRequestTypeDef = TypedDict(
    "UpdateComponentTypeRequestRequestTypeDef",
    {
        "workspaceId": str,
        "componentTypeId": str,
        "isSingleton": NotRequired[bool],
        "description": NotRequired[str],
        "propertyDefinitions": NotRequired[Mapping[str, PropertyDefinitionRequestTypeDef]],
        "extendsFrom": NotRequired[Sequence[str]],
        "functions": NotRequired[Mapping[str, FunctionRequestTypeDef]],
        "propertyGroups": NotRequired[Mapping[str, PropertyGroupRequestTypeDef]],
        "componentTypeName": NotRequired[str],
    },
)

GetComponentTypeResponseTypeDef = TypedDict(
    "GetComponentTypeResponseTypeDef",
    {
        "workspaceId": str,
        "isSingleton": bool,
        "componentTypeId": str,
        "description": str,
        "propertyDefinitions": Dict[str, PropertyDefinitionResponseTypeDef],
        "extendsFrom": List[str],
        "functions": Dict[str, FunctionResponseTypeDef],
        "creationDateTime": datetime,
        "updateDateTime": datetime,
        "arn": str,
        "isAbstract": bool,
        "isSchemaInitialized": bool,
        "status": StatusTypeDef,
        "propertyGroups": Dict[str, PropertyGroupResponseTypeDef],
        "syncSource": str,
        "componentTypeName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListComponentTypesResponseTypeDef = TypedDict(
    "ListComponentTypesResponseTypeDef",
    {
        "workspaceId": str,
        "componentTypeSummaries": List[ComponentTypeSummaryTypeDef],
        "nextToken": str,
        "maxResults": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListEntitiesResponseTypeDef = TypedDict(
    "ListEntitiesResponseTypeDef",
    {
        "entitySummaries": List[EntitySummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSyncJobsResponseTypeDef = TypedDict(
    "ListSyncJobsResponseTypeDef",
    {
        "syncJobSummaries": List[SyncJobSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSyncResourcesResponseTypeDef = TypedDict(
    "ListSyncResourcesResponseTypeDef",
    {
        "syncResources": List[SyncResourceSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetEntityResponseTypeDef = TypedDict(
    "GetEntityResponseTypeDef",
    {
        "entityId": str,
        "entityName": str,
        "arn": str,
        "status": StatusTypeDef,
        "workspaceId": str,
        "description": str,
        "components": Dict[str, ComponentResponseTypeDef],
        "parentEntityId": str,
        "hasChildEntities": bool,
        "creationDateTime": datetime,
        "updateDateTime": datetime,
        "syncSource": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchPutPropertyErrorTypeDef = TypedDict(
    "BatchPutPropertyErrorTypeDef",
    {
        "errorCode": str,
        "errorMessage": str,
        "entry": PropertyValueEntryTypeDef,
    },
)

BatchPutPropertyValuesRequestRequestTypeDef = TypedDict(
    "BatchPutPropertyValuesRequestRequestTypeDef",
    {
        "workspaceId": str,
        "entries": Sequence[PropertyValueEntryTypeDef],
    },
)

GetPropertyValueHistoryResponseTypeDef = TypedDict(
    "GetPropertyValueHistoryResponseTypeDef",
    {
        "propertyValues": List[PropertyValueHistoryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchPutPropertyErrorEntryTypeDef = TypedDict(
    "BatchPutPropertyErrorEntryTypeDef",
    {
        "errors": List[BatchPutPropertyErrorTypeDef],
    },
)

BatchPutPropertyValuesResponseTypeDef = TypedDict(
    "BatchPutPropertyValuesResponseTypeDef",
    {
        "errorEntries": List[BatchPutPropertyErrorEntryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
