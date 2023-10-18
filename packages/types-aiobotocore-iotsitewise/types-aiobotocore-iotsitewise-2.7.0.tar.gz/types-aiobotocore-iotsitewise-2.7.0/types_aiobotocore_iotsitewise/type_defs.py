"""
Type annotations for iotsitewise service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsitewise/type_defs/)

Usage::

    ```python
    from types_aiobotocore_iotsitewise.type_defs import AggregatesTypeDef

    data: AggregatesTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from aiobotocore.response import StreamingBody

from .literals import (
    AggregateTypeType,
    AssetModelStateType,
    AssetStateType,
    AuthModeType,
    BatchEntryCompletionStatusType,
    BatchGetAssetPropertyAggregatesErrorCodeType,
    BatchGetAssetPropertyValueErrorCodeType,
    BatchGetAssetPropertyValueHistoryErrorCodeType,
    BatchPutAssetPropertyValueErrorCodeType,
    CapabilitySyncStatusType,
    ColumnNameType,
    ComputeLocationType,
    ConfigurationStateType,
    DetailedErrorCodeType,
    DisassociatedDataStorageStateType,
    EncryptionTypeType,
    ErrorCodeType,
    ForwardingConfigStateType,
    IdentityTypeType,
    JobStatusType,
    ListAssetModelPropertiesFilterType,
    ListAssetPropertiesFilterType,
    ListAssetsFilterType,
    ListBulkImportJobsFilterType,
    ListTimeSeriesTypeType,
    LoggingLevelType,
    MonitorErrorCodeType,
    PermissionType,
    PortalStateType,
    PropertyDataTypeType,
    PropertyNotificationStateType,
    QualityType,
    ResourceTypeType,
    StorageTypeType,
    TimeOrderingType,
    TraversalDirectionType,
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
    "AggregatesTypeDef",
    "AlarmsTypeDef",
    "AssetErrorDetailsTypeDef",
    "AssetHierarchyInfoTypeDef",
    "AssetHierarchyTypeDef",
    "AssetModelHierarchyDefinitionTypeDef",
    "AssetModelHierarchyTypeDef",
    "PropertyNotificationTypeDef",
    "TimeInNanosTypeDef",
    "VariantTypeDef",
    "AssociateAssetsRequestRequestTypeDef",
    "AssociateTimeSeriesToAssetPropertyRequestRequestTypeDef",
    "AttributeTypeDef",
    "BatchAssociateProjectAssetsRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "BatchDisassociateProjectAssetsRequestRequestTypeDef",
    "TimestampTypeDef",
    "BatchGetAssetPropertyAggregatesErrorEntryTypeDef",
    "BatchGetAssetPropertyAggregatesErrorInfoTypeDef",
    "BatchGetAssetPropertyValueEntryTypeDef",
    "BatchGetAssetPropertyValueErrorEntryTypeDef",
    "BatchGetAssetPropertyValueErrorInfoTypeDef",
    "BatchGetAssetPropertyValueHistoryErrorEntryTypeDef",
    "BatchGetAssetPropertyValueHistoryErrorInfoTypeDef",
    "BlobTypeDef",
    "ConfigurationErrorDetailsTypeDef",
    "CreateAssetRequestRequestTypeDef",
    "ErrorReportLocationTypeDef",
    "FileTypeDef",
    "CreateDashboardRequestRequestTypeDef",
    "CreateProjectRequestRequestTypeDef",
    "CsvTypeDef",
    "CustomerManagedS3StorageTypeDef",
    "DashboardSummaryTypeDef",
    "DeleteAccessPolicyRequestRequestTypeDef",
    "DeleteAssetModelRequestRequestTypeDef",
    "DeleteAssetRequestRequestTypeDef",
    "DeleteDashboardRequestRequestTypeDef",
    "DeleteGatewayRequestRequestTypeDef",
    "DeletePortalRequestRequestTypeDef",
    "DeleteProjectRequestRequestTypeDef",
    "DeleteTimeSeriesRequestRequestTypeDef",
    "DescribeAccessPolicyRequestRequestTypeDef",
    "WaiterConfigTypeDef",
    "DescribeAssetModelRequestRequestTypeDef",
    "DescribeAssetPropertyRequestRequestTypeDef",
    "DescribeAssetRequestRequestTypeDef",
    "DescribeBulkImportJobRequestRequestTypeDef",
    "DescribeDashboardRequestRequestTypeDef",
    "DescribeGatewayCapabilityConfigurationRequestRequestTypeDef",
    "DescribeGatewayRequestRequestTypeDef",
    "GatewayCapabilitySummaryTypeDef",
    "LoggingOptionsTypeDef",
    "DescribePortalRequestRequestTypeDef",
    "ImageLocationTypeDef",
    "DescribeProjectRequestRequestTypeDef",
    "RetentionPeriodTypeDef",
    "DescribeTimeSeriesRequestRequestTypeDef",
    "DetailedErrorTypeDef",
    "DisassociateAssetsRequestRequestTypeDef",
    "DisassociateTimeSeriesFromAssetPropertyRequestRequestTypeDef",
    "VariableValueTypeDef",
    "ForwardingConfigTypeDef",
    "GreengrassTypeDef",
    "GreengrassV2TypeDef",
    "PaginatorConfigTypeDef",
    "GetAssetPropertyValueRequestRequestTypeDef",
    "GetInterpolatedAssetPropertyValuesRequestRequestTypeDef",
    "GroupIdentityTypeDef",
    "IAMRoleIdentityTypeDef",
    "IAMUserIdentityTypeDef",
    "UserIdentityTypeDef",
    "JobSummaryTypeDef",
    "ListAccessPoliciesRequestRequestTypeDef",
    "ListAssetModelPropertiesRequestRequestTypeDef",
    "ListAssetModelsRequestRequestTypeDef",
    "ListAssetPropertiesRequestRequestTypeDef",
    "ListAssetRelationshipsRequestRequestTypeDef",
    "ListAssetsRequestRequestTypeDef",
    "ListAssociatedAssetsRequestRequestTypeDef",
    "ListBulkImportJobsRequestRequestTypeDef",
    "ListDashboardsRequestRequestTypeDef",
    "ListGatewaysRequestRequestTypeDef",
    "ListPortalsRequestRequestTypeDef",
    "ListProjectAssetsRequestRequestTypeDef",
    "ListProjectsRequestRequestTypeDef",
    "ProjectSummaryTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTimeSeriesRequestRequestTypeDef",
    "TimeSeriesSummaryTypeDef",
    "MetricProcessingConfigTypeDef",
    "TumblingWindowTypeDef",
    "MonitorErrorDetailsTypeDef",
    "PortalResourceTypeDef",
    "ProjectResourceTypeDef",
    "PutDefaultEncryptionConfigurationRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAssetPropertyRequestRequestTypeDef",
    "UpdateAssetRequestRequestTypeDef",
    "UpdateDashboardRequestRequestTypeDef",
    "UpdateGatewayCapabilityConfigurationRequestRequestTypeDef",
    "UpdateGatewayRequestRequestTypeDef",
    "UpdateProjectRequestRequestTypeDef",
    "AggregatedValueTypeDef",
    "AssetRelationshipSummaryTypeDef",
    "AssetPropertySummaryTypeDef",
    "AssetPropertyTypeDef",
    "BatchPutAssetPropertyErrorTypeDef",
    "AssetPropertyValueTypeDef",
    "InterpolatedAssetPropertyValueTypeDef",
    "BatchAssociateProjectAssetsResponseTypeDef",
    "BatchDisassociateProjectAssetsResponseTypeDef",
    "CreateAccessPolicyResponseTypeDef",
    "CreateBulkImportJobResponseTypeDef",
    "CreateDashboardResponseTypeDef",
    "CreateGatewayResponseTypeDef",
    "CreateProjectResponseTypeDef",
    "DescribeDashboardResponseTypeDef",
    "DescribeGatewayCapabilityConfigurationResponseTypeDef",
    "DescribeProjectResponseTypeDef",
    "DescribeTimeSeriesResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ListProjectAssetsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "UpdateGatewayCapabilityConfigurationResponseTypeDef",
    "BatchGetAssetPropertyAggregatesEntryTypeDef",
    "BatchGetAssetPropertyValueHistoryEntryTypeDef",
    "GetAssetPropertyAggregatesRequestRequestTypeDef",
    "GetAssetPropertyValueHistoryRequestRequestTypeDef",
    "BatchGetAssetPropertyAggregatesSkippedEntryTypeDef",
    "BatchGetAssetPropertyValueRequestRequestTypeDef",
    "BatchGetAssetPropertyValueSkippedEntryTypeDef",
    "BatchGetAssetPropertyValueHistorySkippedEntryTypeDef",
    "ImageFileTypeDef",
    "ConfigurationStatusTypeDef",
    "FileFormatTypeDef",
    "MultiLayerStorageTypeDef",
    "ListDashboardsResponseTypeDef",
    "DescribeAssetModelRequestAssetModelActiveWaitTypeDef",
    "DescribeAssetModelRequestAssetModelNotExistsWaitTypeDef",
    "DescribeAssetRequestAssetActiveWaitTypeDef",
    "DescribeAssetRequestAssetNotExistsWaitTypeDef",
    "DescribePortalRequestPortalActiveWaitTypeDef",
    "DescribePortalRequestPortalNotExistsWaitTypeDef",
    "DescribeLoggingOptionsResponseTypeDef",
    "PutLoggingOptionsRequestRequestTypeDef",
    "ErrorDetailsTypeDef",
    "ExpressionVariableTypeDef",
    "MeasurementProcessingConfigTypeDef",
    "TransformProcessingConfigTypeDef",
    "GatewayPlatformTypeDef",
    "GetAssetPropertyAggregatesRequestGetAssetPropertyAggregatesPaginateTypeDef",
    "GetAssetPropertyValueHistoryRequestGetAssetPropertyValueHistoryPaginateTypeDef",
    "GetInterpolatedAssetPropertyValuesRequestGetInterpolatedAssetPropertyValuesPaginateTypeDef",
    "ListAccessPoliciesRequestListAccessPoliciesPaginateTypeDef",
    "ListAssetModelPropertiesRequestListAssetModelPropertiesPaginateTypeDef",
    "ListAssetModelsRequestListAssetModelsPaginateTypeDef",
    "ListAssetPropertiesRequestListAssetPropertiesPaginateTypeDef",
    "ListAssetRelationshipsRequestListAssetRelationshipsPaginateTypeDef",
    "ListAssetsRequestListAssetsPaginateTypeDef",
    "ListAssociatedAssetsRequestListAssociatedAssetsPaginateTypeDef",
    "ListBulkImportJobsRequestListBulkImportJobsPaginateTypeDef",
    "ListDashboardsRequestListDashboardsPaginateTypeDef",
    "ListGatewaysRequestListGatewaysPaginateTypeDef",
    "ListPortalsRequestListPortalsPaginateTypeDef",
    "ListProjectAssetsRequestListProjectAssetsPaginateTypeDef",
    "ListProjectsRequestListProjectsPaginateTypeDef",
    "ListTimeSeriesRequestListTimeSeriesPaginateTypeDef",
    "IdentityTypeDef",
    "ListBulkImportJobsResponseTypeDef",
    "ListProjectsResponseTypeDef",
    "ListTimeSeriesResponseTypeDef",
    "MetricWindowTypeDef",
    "PortalStatusTypeDef",
    "ResourceTypeDef",
    "BatchGetAssetPropertyAggregatesSuccessEntryTypeDef",
    "GetAssetPropertyAggregatesResponseTypeDef",
    "ListAssetRelationshipsResponseTypeDef",
    "ListAssetPropertiesResponseTypeDef",
    "AssetCompositeModelTypeDef",
    "BatchPutAssetPropertyErrorEntryTypeDef",
    "BatchGetAssetPropertyValueHistorySuccessEntryTypeDef",
    "BatchGetAssetPropertyValueSuccessEntryTypeDef",
    "GetAssetPropertyValueHistoryResponseTypeDef",
    "GetAssetPropertyValueResponseTypeDef",
    "PutAssetPropertyValueEntryTypeDef",
    "GetInterpolatedAssetPropertyValuesResponseTypeDef",
    "BatchGetAssetPropertyAggregatesRequestRequestTypeDef",
    "BatchGetAssetPropertyValueHistoryRequestRequestTypeDef",
    "CreatePortalRequestRequestTypeDef",
    "ImageTypeDef",
    "DescribeDefaultEncryptionConfigurationResponseTypeDef",
    "PutDefaultEncryptionConfigurationResponseTypeDef",
    "JobConfigurationTypeDef",
    "DescribeStorageConfigurationResponseTypeDef",
    "PutStorageConfigurationRequestRequestTypeDef",
    "PutStorageConfigurationResponseTypeDef",
    "AssetModelStatusTypeDef",
    "AssetStatusTypeDef",
    "MeasurementTypeDef",
    "TransformPaginatorTypeDef",
    "TransformTypeDef",
    "CreateGatewayRequestRequestTypeDef",
    "DescribeGatewayResponseTypeDef",
    "GatewaySummaryTypeDef",
    "MetricPaginatorTypeDef",
    "MetricTypeDef",
    "CreatePortalResponseTypeDef",
    "DeletePortalResponseTypeDef",
    "DescribePortalResponseTypeDef",
    "PortalSummaryTypeDef",
    "UpdatePortalResponseTypeDef",
    "AccessPolicySummaryTypeDef",
    "CreateAccessPolicyRequestRequestTypeDef",
    "DescribeAccessPolicyResponseTypeDef",
    "UpdateAccessPolicyRequestRequestTypeDef",
    "BatchGetAssetPropertyAggregatesResponseTypeDef",
    "BatchPutAssetPropertyValueResponseTypeDef",
    "BatchGetAssetPropertyValueHistoryResponseTypeDef",
    "BatchGetAssetPropertyValueResponseTypeDef",
    "BatchPutAssetPropertyValueRequestRequestTypeDef",
    "UpdatePortalRequestRequestTypeDef",
    "CreateBulkImportJobRequestRequestTypeDef",
    "DescribeBulkImportJobResponseTypeDef",
    "AssetModelSummaryTypeDef",
    "CreateAssetModelResponseTypeDef",
    "DeleteAssetModelResponseTypeDef",
    "UpdateAssetModelResponseTypeDef",
    "AssetSummaryTypeDef",
    "AssociatedAssetsSummaryTypeDef",
    "CreateAssetResponseTypeDef",
    "DeleteAssetResponseTypeDef",
    "DescribeAssetResponseTypeDef",
    "UpdateAssetResponseTypeDef",
    "ListGatewaysResponseTypeDef",
    "PropertyTypePaginatorTypeDef",
    "PropertyTypeTypeDef",
    "ListPortalsResponseTypeDef",
    "ListAccessPoliciesResponseTypeDef",
    "ListAssetModelsResponseTypeDef",
    "ListAssetsResponseTypeDef",
    "ListAssociatedAssetsResponseTypeDef",
    "AssetModelPropertySummaryPaginatorTypeDef",
    "AssetModelPropertyDefinitionTypeDef",
    "AssetModelPropertySummaryTypeDef",
    "AssetModelPropertyTypeDef",
    "PropertyTypeDef",
    "ListAssetModelPropertiesResponsePaginatorTypeDef",
    "AssetModelCompositeModelDefinitionTypeDef",
    "ListAssetModelPropertiesResponseTypeDef",
    "AssetModelCompositeModelTypeDef",
    "CompositeModelPropertyTypeDef",
    "CreateAssetModelRequestRequestTypeDef",
    "DescribeAssetModelResponseTypeDef",
    "UpdateAssetModelRequestRequestTypeDef",
    "DescribeAssetPropertyResponseTypeDef",
)

AggregatesTypeDef = TypedDict(
    "AggregatesTypeDef",
    {
        "average": NotRequired[float],
        "count": NotRequired[float],
        "maximum": NotRequired[float],
        "minimum": NotRequired[float],
        "sum": NotRequired[float],
        "standardDeviation": NotRequired[float],
    },
)

AlarmsTypeDef = TypedDict(
    "AlarmsTypeDef",
    {
        "alarmRoleArn": str,
        "notificationLambdaArn": NotRequired[str],
    },
)

AssetErrorDetailsTypeDef = TypedDict(
    "AssetErrorDetailsTypeDef",
    {
        "assetId": str,
        "code": Literal["INTERNAL_FAILURE"],
        "message": str,
    },
)

AssetHierarchyInfoTypeDef = TypedDict(
    "AssetHierarchyInfoTypeDef",
    {
        "parentAssetId": NotRequired[str],
        "childAssetId": NotRequired[str],
    },
)

AssetHierarchyTypeDef = TypedDict(
    "AssetHierarchyTypeDef",
    {
        "name": str,
        "id": NotRequired[str],
    },
)

AssetModelHierarchyDefinitionTypeDef = TypedDict(
    "AssetModelHierarchyDefinitionTypeDef",
    {
        "name": str,
        "childAssetModelId": str,
    },
)

AssetModelHierarchyTypeDef = TypedDict(
    "AssetModelHierarchyTypeDef",
    {
        "name": str,
        "childAssetModelId": str,
        "id": NotRequired[str],
    },
)

PropertyNotificationTypeDef = TypedDict(
    "PropertyNotificationTypeDef",
    {
        "topic": str,
        "state": PropertyNotificationStateType,
    },
)

TimeInNanosTypeDef = TypedDict(
    "TimeInNanosTypeDef",
    {
        "timeInSeconds": int,
        "offsetInNanos": NotRequired[int],
    },
)

VariantTypeDef = TypedDict(
    "VariantTypeDef",
    {
        "stringValue": NotRequired[str],
        "integerValue": NotRequired[int],
        "doubleValue": NotRequired[float],
        "booleanValue": NotRequired[bool],
    },
)

AssociateAssetsRequestRequestTypeDef = TypedDict(
    "AssociateAssetsRequestRequestTypeDef",
    {
        "assetId": str,
        "hierarchyId": str,
        "childAssetId": str,
        "clientToken": NotRequired[str],
    },
)

AssociateTimeSeriesToAssetPropertyRequestRequestTypeDef = TypedDict(
    "AssociateTimeSeriesToAssetPropertyRequestRequestTypeDef",
    {
        "alias": str,
        "assetId": str,
        "propertyId": str,
        "clientToken": NotRequired[str],
    },
)

AttributeTypeDef = TypedDict(
    "AttributeTypeDef",
    {
        "defaultValue": NotRequired[str],
    },
)

BatchAssociateProjectAssetsRequestRequestTypeDef = TypedDict(
    "BatchAssociateProjectAssetsRequestRequestTypeDef",
    {
        "projectId": str,
        "assetIds": Sequence[str],
        "clientToken": NotRequired[str],
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

BatchDisassociateProjectAssetsRequestRequestTypeDef = TypedDict(
    "BatchDisassociateProjectAssetsRequestRequestTypeDef",
    {
        "projectId": str,
        "assetIds": Sequence[str],
        "clientToken": NotRequired[str],
    },
)

TimestampTypeDef = Union[datetime, str]
BatchGetAssetPropertyAggregatesErrorEntryTypeDef = TypedDict(
    "BatchGetAssetPropertyAggregatesErrorEntryTypeDef",
    {
        "errorCode": BatchGetAssetPropertyAggregatesErrorCodeType,
        "errorMessage": str,
        "entryId": str,
    },
)

BatchGetAssetPropertyAggregatesErrorInfoTypeDef = TypedDict(
    "BatchGetAssetPropertyAggregatesErrorInfoTypeDef",
    {
        "errorCode": BatchGetAssetPropertyAggregatesErrorCodeType,
        "errorTimestamp": datetime,
    },
)

BatchGetAssetPropertyValueEntryTypeDef = TypedDict(
    "BatchGetAssetPropertyValueEntryTypeDef",
    {
        "entryId": str,
        "assetId": NotRequired[str],
        "propertyId": NotRequired[str],
        "propertyAlias": NotRequired[str],
    },
)

BatchGetAssetPropertyValueErrorEntryTypeDef = TypedDict(
    "BatchGetAssetPropertyValueErrorEntryTypeDef",
    {
        "errorCode": BatchGetAssetPropertyValueErrorCodeType,
        "errorMessage": str,
        "entryId": str,
    },
)

BatchGetAssetPropertyValueErrorInfoTypeDef = TypedDict(
    "BatchGetAssetPropertyValueErrorInfoTypeDef",
    {
        "errorCode": BatchGetAssetPropertyValueErrorCodeType,
        "errorTimestamp": datetime,
    },
)

BatchGetAssetPropertyValueHistoryErrorEntryTypeDef = TypedDict(
    "BatchGetAssetPropertyValueHistoryErrorEntryTypeDef",
    {
        "errorCode": BatchGetAssetPropertyValueHistoryErrorCodeType,
        "errorMessage": str,
        "entryId": str,
    },
)

BatchGetAssetPropertyValueHistoryErrorInfoTypeDef = TypedDict(
    "BatchGetAssetPropertyValueHistoryErrorInfoTypeDef",
    {
        "errorCode": BatchGetAssetPropertyValueHistoryErrorCodeType,
        "errorTimestamp": datetime,
    },
)

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]
ConfigurationErrorDetailsTypeDef = TypedDict(
    "ConfigurationErrorDetailsTypeDef",
    {
        "code": ErrorCodeType,
        "message": str,
    },
)

CreateAssetRequestRequestTypeDef = TypedDict(
    "CreateAssetRequestRequestTypeDef",
    {
        "assetName": str,
        "assetModelId": str,
        "clientToken": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
        "assetDescription": NotRequired[str],
    },
)

ErrorReportLocationTypeDef = TypedDict(
    "ErrorReportLocationTypeDef",
    {
        "bucket": str,
        "prefix": str,
    },
)

FileTypeDef = TypedDict(
    "FileTypeDef",
    {
        "bucket": str,
        "key": str,
        "versionId": NotRequired[str],
    },
)

CreateDashboardRequestRequestTypeDef = TypedDict(
    "CreateDashboardRequestRequestTypeDef",
    {
        "projectId": str,
        "dashboardName": str,
        "dashboardDefinition": str,
        "dashboardDescription": NotRequired[str],
        "clientToken": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)

CreateProjectRequestRequestTypeDef = TypedDict(
    "CreateProjectRequestRequestTypeDef",
    {
        "portalId": str,
        "projectName": str,
        "projectDescription": NotRequired[str],
        "clientToken": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)

CsvTypeDef = TypedDict(
    "CsvTypeDef",
    {
        "columnNames": NotRequired[Sequence[ColumnNameType]],
    },
)

CustomerManagedS3StorageTypeDef = TypedDict(
    "CustomerManagedS3StorageTypeDef",
    {
        "s3ResourceArn": str,
        "roleArn": str,
    },
)

DashboardSummaryTypeDef = TypedDict(
    "DashboardSummaryTypeDef",
    {
        "id": str,
        "name": str,
        "description": NotRequired[str],
        "creationDate": NotRequired[datetime],
        "lastUpdateDate": NotRequired[datetime],
    },
)

DeleteAccessPolicyRequestRequestTypeDef = TypedDict(
    "DeleteAccessPolicyRequestRequestTypeDef",
    {
        "accessPolicyId": str,
        "clientToken": NotRequired[str],
    },
)

DeleteAssetModelRequestRequestTypeDef = TypedDict(
    "DeleteAssetModelRequestRequestTypeDef",
    {
        "assetModelId": str,
        "clientToken": NotRequired[str],
    },
)

DeleteAssetRequestRequestTypeDef = TypedDict(
    "DeleteAssetRequestRequestTypeDef",
    {
        "assetId": str,
        "clientToken": NotRequired[str],
    },
)

DeleteDashboardRequestRequestTypeDef = TypedDict(
    "DeleteDashboardRequestRequestTypeDef",
    {
        "dashboardId": str,
        "clientToken": NotRequired[str],
    },
)

DeleteGatewayRequestRequestTypeDef = TypedDict(
    "DeleteGatewayRequestRequestTypeDef",
    {
        "gatewayId": str,
    },
)

DeletePortalRequestRequestTypeDef = TypedDict(
    "DeletePortalRequestRequestTypeDef",
    {
        "portalId": str,
        "clientToken": NotRequired[str],
    },
)

DeleteProjectRequestRequestTypeDef = TypedDict(
    "DeleteProjectRequestRequestTypeDef",
    {
        "projectId": str,
        "clientToken": NotRequired[str],
    },
)

DeleteTimeSeriesRequestRequestTypeDef = TypedDict(
    "DeleteTimeSeriesRequestRequestTypeDef",
    {
        "alias": NotRequired[str],
        "assetId": NotRequired[str],
        "propertyId": NotRequired[str],
        "clientToken": NotRequired[str],
    },
)

DescribeAccessPolicyRequestRequestTypeDef = TypedDict(
    "DescribeAccessPolicyRequestRequestTypeDef",
    {
        "accessPolicyId": str,
    },
)

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": NotRequired[int],
        "MaxAttempts": NotRequired[int],
    },
)

DescribeAssetModelRequestRequestTypeDef = TypedDict(
    "DescribeAssetModelRequestRequestTypeDef",
    {
        "assetModelId": str,
        "excludeProperties": NotRequired[bool],
    },
)

DescribeAssetPropertyRequestRequestTypeDef = TypedDict(
    "DescribeAssetPropertyRequestRequestTypeDef",
    {
        "assetId": str,
        "propertyId": str,
    },
)

DescribeAssetRequestRequestTypeDef = TypedDict(
    "DescribeAssetRequestRequestTypeDef",
    {
        "assetId": str,
        "excludeProperties": NotRequired[bool],
    },
)

DescribeBulkImportJobRequestRequestTypeDef = TypedDict(
    "DescribeBulkImportJobRequestRequestTypeDef",
    {
        "jobId": str,
    },
)

DescribeDashboardRequestRequestTypeDef = TypedDict(
    "DescribeDashboardRequestRequestTypeDef",
    {
        "dashboardId": str,
    },
)

DescribeGatewayCapabilityConfigurationRequestRequestTypeDef = TypedDict(
    "DescribeGatewayCapabilityConfigurationRequestRequestTypeDef",
    {
        "gatewayId": str,
        "capabilityNamespace": str,
    },
)

DescribeGatewayRequestRequestTypeDef = TypedDict(
    "DescribeGatewayRequestRequestTypeDef",
    {
        "gatewayId": str,
    },
)

GatewayCapabilitySummaryTypeDef = TypedDict(
    "GatewayCapabilitySummaryTypeDef",
    {
        "capabilityNamespace": str,
        "capabilitySyncStatus": CapabilitySyncStatusType,
    },
)

LoggingOptionsTypeDef = TypedDict(
    "LoggingOptionsTypeDef",
    {
        "level": LoggingLevelType,
    },
)

DescribePortalRequestRequestTypeDef = TypedDict(
    "DescribePortalRequestRequestTypeDef",
    {
        "portalId": str,
    },
)

ImageLocationTypeDef = TypedDict(
    "ImageLocationTypeDef",
    {
        "id": str,
        "url": str,
    },
)

DescribeProjectRequestRequestTypeDef = TypedDict(
    "DescribeProjectRequestRequestTypeDef",
    {
        "projectId": str,
    },
)

RetentionPeriodTypeDef = TypedDict(
    "RetentionPeriodTypeDef",
    {
        "numberOfDays": NotRequired[int],
        "unlimited": NotRequired[bool],
    },
)

DescribeTimeSeriesRequestRequestTypeDef = TypedDict(
    "DescribeTimeSeriesRequestRequestTypeDef",
    {
        "alias": NotRequired[str],
        "assetId": NotRequired[str],
        "propertyId": NotRequired[str],
    },
)

DetailedErrorTypeDef = TypedDict(
    "DetailedErrorTypeDef",
    {
        "code": DetailedErrorCodeType,
        "message": str,
    },
)

DisassociateAssetsRequestRequestTypeDef = TypedDict(
    "DisassociateAssetsRequestRequestTypeDef",
    {
        "assetId": str,
        "hierarchyId": str,
        "childAssetId": str,
        "clientToken": NotRequired[str],
    },
)

DisassociateTimeSeriesFromAssetPropertyRequestRequestTypeDef = TypedDict(
    "DisassociateTimeSeriesFromAssetPropertyRequestRequestTypeDef",
    {
        "alias": str,
        "assetId": str,
        "propertyId": str,
        "clientToken": NotRequired[str],
    },
)

VariableValueTypeDef = TypedDict(
    "VariableValueTypeDef",
    {
        "propertyId": str,
        "hierarchyId": NotRequired[str],
    },
)

ForwardingConfigTypeDef = TypedDict(
    "ForwardingConfigTypeDef",
    {
        "state": ForwardingConfigStateType,
    },
)

GreengrassTypeDef = TypedDict(
    "GreengrassTypeDef",
    {
        "groupArn": str,
    },
)

GreengrassV2TypeDef = TypedDict(
    "GreengrassV2TypeDef",
    {
        "coreDeviceThingName": str,
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

GetAssetPropertyValueRequestRequestTypeDef = TypedDict(
    "GetAssetPropertyValueRequestRequestTypeDef",
    {
        "assetId": NotRequired[str],
        "propertyId": NotRequired[str],
        "propertyAlias": NotRequired[str],
    },
)

GetInterpolatedAssetPropertyValuesRequestRequestTypeDef = TypedDict(
    "GetInterpolatedAssetPropertyValuesRequestRequestTypeDef",
    {
        "startTimeInSeconds": int,
        "endTimeInSeconds": int,
        "quality": QualityType,
        "intervalInSeconds": int,
        "type": str,
        "assetId": NotRequired[str],
        "propertyId": NotRequired[str],
        "propertyAlias": NotRequired[str],
        "startTimeOffsetInNanos": NotRequired[int],
        "endTimeOffsetInNanos": NotRequired[int],
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
        "intervalWindowInSeconds": NotRequired[int],
    },
)

GroupIdentityTypeDef = TypedDict(
    "GroupIdentityTypeDef",
    {
        "id": str,
    },
)

IAMRoleIdentityTypeDef = TypedDict(
    "IAMRoleIdentityTypeDef",
    {
        "arn": str,
    },
)

IAMUserIdentityTypeDef = TypedDict(
    "IAMUserIdentityTypeDef",
    {
        "arn": str,
    },
)

UserIdentityTypeDef = TypedDict(
    "UserIdentityTypeDef",
    {
        "id": str,
    },
)

JobSummaryTypeDef = TypedDict(
    "JobSummaryTypeDef",
    {
        "id": str,
        "name": str,
        "status": JobStatusType,
    },
)

ListAccessPoliciesRequestRequestTypeDef = TypedDict(
    "ListAccessPoliciesRequestRequestTypeDef",
    {
        "identityType": NotRequired[IdentityTypeType],
        "identityId": NotRequired[str],
        "resourceType": NotRequired[ResourceTypeType],
        "resourceId": NotRequired[str],
        "iamArn": NotRequired[str],
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)

ListAssetModelPropertiesRequestRequestTypeDef = TypedDict(
    "ListAssetModelPropertiesRequestRequestTypeDef",
    {
        "assetModelId": str,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
        "filter": NotRequired[ListAssetModelPropertiesFilterType],
    },
)

ListAssetModelsRequestRequestTypeDef = TypedDict(
    "ListAssetModelsRequestRequestTypeDef",
    {
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)

ListAssetPropertiesRequestRequestTypeDef = TypedDict(
    "ListAssetPropertiesRequestRequestTypeDef",
    {
        "assetId": str,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
        "filter": NotRequired[ListAssetPropertiesFilterType],
    },
)

ListAssetRelationshipsRequestRequestTypeDef = TypedDict(
    "ListAssetRelationshipsRequestRequestTypeDef",
    {
        "assetId": str,
        "traversalType": Literal["PATH_TO_ROOT"],
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)

ListAssetsRequestRequestTypeDef = TypedDict(
    "ListAssetsRequestRequestTypeDef",
    {
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
        "assetModelId": NotRequired[str],
        "filter": NotRequired[ListAssetsFilterType],
    },
)

ListAssociatedAssetsRequestRequestTypeDef = TypedDict(
    "ListAssociatedAssetsRequestRequestTypeDef",
    {
        "assetId": str,
        "hierarchyId": NotRequired[str],
        "traversalDirection": NotRequired[TraversalDirectionType],
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)

ListBulkImportJobsRequestRequestTypeDef = TypedDict(
    "ListBulkImportJobsRequestRequestTypeDef",
    {
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
        "filter": NotRequired[ListBulkImportJobsFilterType],
    },
)

ListDashboardsRequestRequestTypeDef = TypedDict(
    "ListDashboardsRequestRequestTypeDef",
    {
        "projectId": str,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)

ListGatewaysRequestRequestTypeDef = TypedDict(
    "ListGatewaysRequestRequestTypeDef",
    {
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)

ListPortalsRequestRequestTypeDef = TypedDict(
    "ListPortalsRequestRequestTypeDef",
    {
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)

ListProjectAssetsRequestRequestTypeDef = TypedDict(
    "ListProjectAssetsRequestRequestTypeDef",
    {
        "projectId": str,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)

ListProjectsRequestRequestTypeDef = TypedDict(
    "ListProjectsRequestRequestTypeDef",
    {
        "portalId": str,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)

ProjectSummaryTypeDef = TypedDict(
    "ProjectSummaryTypeDef",
    {
        "id": str,
        "name": str,
        "description": NotRequired[str],
        "creationDate": NotRequired[datetime],
        "lastUpdateDate": NotRequired[datetime],
    },
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

ListTimeSeriesRequestRequestTypeDef = TypedDict(
    "ListTimeSeriesRequestRequestTypeDef",
    {
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
        "assetId": NotRequired[str],
        "aliasPrefix": NotRequired[str],
        "timeSeriesType": NotRequired[ListTimeSeriesTypeType],
    },
)

TimeSeriesSummaryTypeDef = TypedDict(
    "TimeSeriesSummaryTypeDef",
    {
        "timeSeriesId": str,
        "dataType": PropertyDataTypeType,
        "timeSeriesCreationDate": datetime,
        "timeSeriesLastUpdateDate": datetime,
        "timeSeriesArn": str,
        "assetId": NotRequired[str],
        "propertyId": NotRequired[str],
        "alias": NotRequired[str],
        "dataTypeSpec": NotRequired[str],
    },
)

MetricProcessingConfigTypeDef = TypedDict(
    "MetricProcessingConfigTypeDef",
    {
        "computeLocation": ComputeLocationType,
    },
)

TumblingWindowTypeDef = TypedDict(
    "TumblingWindowTypeDef",
    {
        "interval": str,
        "offset": NotRequired[str],
    },
)

MonitorErrorDetailsTypeDef = TypedDict(
    "MonitorErrorDetailsTypeDef",
    {
        "code": NotRequired[MonitorErrorCodeType],
        "message": NotRequired[str],
    },
)

PortalResourceTypeDef = TypedDict(
    "PortalResourceTypeDef",
    {
        "id": str,
    },
)

ProjectResourceTypeDef = TypedDict(
    "ProjectResourceTypeDef",
    {
        "id": str,
    },
)

PutDefaultEncryptionConfigurationRequestRequestTypeDef = TypedDict(
    "PutDefaultEncryptionConfigurationRequestRequestTypeDef",
    {
        "encryptionType": EncryptionTypeType,
        "kmsKeyId": NotRequired[str],
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

UpdateAssetPropertyRequestRequestTypeDef = TypedDict(
    "UpdateAssetPropertyRequestRequestTypeDef",
    {
        "assetId": str,
        "propertyId": str,
        "propertyAlias": NotRequired[str],
        "propertyNotificationState": NotRequired[PropertyNotificationStateType],
        "clientToken": NotRequired[str],
        "propertyUnit": NotRequired[str],
    },
)

UpdateAssetRequestRequestTypeDef = TypedDict(
    "UpdateAssetRequestRequestTypeDef",
    {
        "assetId": str,
        "assetName": str,
        "clientToken": NotRequired[str],
        "assetDescription": NotRequired[str],
    },
)

UpdateDashboardRequestRequestTypeDef = TypedDict(
    "UpdateDashboardRequestRequestTypeDef",
    {
        "dashboardId": str,
        "dashboardName": str,
        "dashboardDefinition": str,
        "dashboardDescription": NotRequired[str],
        "clientToken": NotRequired[str],
    },
)

UpdateGatewayCapabilityConfigurationRequestRequestTypeDef = TypedDict(
    "UpdateGatewayCapabilityConfigurationRequestRequestTypeDef",
    {
        "gatewayId": str,
        "capabilityNamespace": str,
        "capabilityConfiguration": str,
    },
)

UpdateGatewayRequestRequestTypeDef = TypedDict(
    "UpdateGatewayRequestRequestTypeDef",
    {
        "gatewayId": str,
        "gatewayName": str,
    },
)

UpdateProjectRequestRequestTypeDef = TypedDict(
    "UpdateProjectRequestRequestTypeDef",
    {
        "projectId": str,
        "projectName": str,
        "projectDescription": NotRequired[str],
        "clientToken": NotRequired[str],
    },
)

AggregatedValueTypeDef = TypedDict(
    "AggregatedValueTypeDef",
    {
        "timestamp": datetime,
        "value": AggregatesTypeDef,
        "quality": NotRequired[QualityType],
    },
)

AssetRelationshipSummaryTypeDef = TypedDict(
    "AssetRelationshipSummaryTypeDef",
    {
        "relationshipType": Literal["HIERARCHY"],
        "hierarchyInfo": NotRequired[AssetHierarchyInfoTypeDef],
    },
)

AssetPropertySummaryTypeDef = TypedDict(
    "AssetPropertySummaryTypeDef",
    {
        "id": NotRequired[str],
        "alias": NotRequired[str],
        "unit": NotRequired[str],
        "notification": NotRequired[PropertyNotificationTypeDef],
        "assetCompositeModelId": NotRequired[str],
    },
)

AssetPropertyTypeDef = TypedDict(
    "AssetPropertyTypeDef",
    {
        "id": str,
        "name": str,
        "dataType": PropertyDataTypeType,
        "alias": NotRequired[str],
        "notification": NotRequired[PropertyNotificationTypeDef],
        "dataTypeSpec": NotRequired[str],
        "unit": NotRequired[str],
    },
)

BatchPutAssetPropertyErrorTypeDef = TypedDict(
    "BatchPutAssetPropertyErrorTypeDef",
    {
        "errorCode": BatchPutAssetPropertyValueErrorCodeType,
        "errorMessage": str,
        "timestamps": List[TimeInNanosTypeDef],
    },
)

AssetPropertyValueTypeDef = TypedDict(
    "AssetPropertyValueTypeDef",
    {
        "value": VariantTypeDef,
        "timestamp": TimeInNanosTypeDef,
        "quality": NotRequired[QualityType],
    },
)

InterpolatedAssetPropertyValueTypeDef = TypedDict(
    "InterpolatedAssetPropertyValueTypeDef",
    {
        "timestamp": TimeInNanosTypeDef,
        "value": VariantTypeDef,
    },
)

BatchAssociateProjectAssetsResponseTypeDef = TypedDict(
    "BatchAssociateProjectAssetsResponseTypeDef",
    {
        "errors": List[AssetErrorDetailsTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchDisassociateProjectAssetsResponseTypeDef = TypedDict(
    "BatchDisassociateProjectAssetsResponseTypeDef",
    {
        "errors": List[AssetErrorDetailsTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAccessPolicyResponseTypeDef = TypedDict(
    "CreateAccessPolicyResponseTypeDef",
    {
        "accessPolicyId": str,
        "accessPolicyArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateBulkImportJobResponseTypeDef = TypedDict(
    "CreateBulkImportJobResponseTypeDef",
    {
        "jobId": str,
        "jobName": str,
        "jobStatus": JobStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDashboardResponseTypeDef = TypedDict(
    "CreateDashboardResponseTypeDef",
    {
        "dashboardId": str,
        "dashboardArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateGatewayResponseTypeDef = TypedDict(
    "CreateGatewayResponseTypeDef",
    {
        "gatewayId": str,
        "gatewayArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateProjectResponseTypeDef = TypedDict(
    "CreateProjectResponseTypeDef",
    {
        "projectId": str,
        "projectArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDashboardResponseTypeDef = TypedDict(
    "DescribeDashboardResponseTypeDef",
    {
        "dashboardId": str,
        "dashboardArn": str,
        "dashboardName": str,
        "projectId": str,
        "dashboardDescription": str,
        "dashboardDefinition": str,
        "dashboardCreationDate": datetime,
        "dashboardLastUpdateDate": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeGatewayCapabilityConfigurationResponseTypeDef = TypedDict(
    "DescribeGatewayCapabilityConfigurationResponseTypeDef",
    {
        "gatewayId": str,
        "capabilityNamespace": str,
        "capabilityConfiguration": str,
        "capabilitySyncStatus": CapabilitySyncStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeProjectResponseTypeDef = TypedDict(
    "DescribeProjectResponseTypeDef",
    {
        "projectId": str,
        "projectArn": str,
        "projectName": str,
        "portalId": str,
        "projectDescription": str,
        "projectCreationDate": datetime,
        "projectLastUpdateDate": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeTimeSeriesResponseTypeDef = TypedDict(
    "DescribeTimeSeriesResponseTypeDef",
    {
        "assetId": str,
        "propertyId": str,
        "alias": str,
        "timeSeriesId": str,
        "dataType": PropertyDataTypeType,
        "dataTypeSpec": str,
        "timeSeriesCreationDate": datetime,
        "timeSeriesLastUpdateDate": datetime,
        "timeSeriesArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListProjectAssetsResponseTypeDef = TypedDict(
    "ListProjectAssetsResponseTypeDef",
    {
        "assetIds": List[str],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateGatewayCapabilityConfigurationResponseTypeDef = TypedDict(
    "UpdateGatewayCapabilityConfigurationResponseTypeDef",
    {
        "capabilityNamespace": str,
        "capabilitySyncStatus": CapabilitySyncStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchGetAssetPropertyAggregatesEntryTypeDef = TypedDict(
    "BatchGetAssetPropertyAggregatesEntryTypeDef",
    {
        "entryId": str,
        "aggregateTypes": Sequence[AggregateTypeType],
        "resolution": str,
        "startDate": TimestampTypeDef,
        "endDate": TimestampTypeDef,
        "assetId": NotRequired[str],
        "propertyId": NotRequired[str],
        "propertyAlias": NotRequired[str],
        "qualities": NotRequired[Sequence[QualityType]],
        "timeOrdering": NotRequired[TimeOrderingType],
    },
)

BatchGetAssetPropertyValueHistoryEntryTypeDef = TypedDict(
    "BatchGetAssetPropertyValueHistoryEntryTypeDef",
    {
        "entryId": str,
        "assetId": NotRequired[str],
        "propertyId": NotRequired[str],
        "propertyAlias": NotRequired[str],
        "startDate": NotRequired[TimestampTypeDef],
        "endDate": NotRequired[TimestampTypeDef],
        "qualities": NotRequired[Sequence[QualityType]],
        "timeOrdering": NotRequired[TimeOrderingType],
    },
)

GetAssetPropertyAggregatesRequestRequestTypeDef = TypedDict(
    "GetAssetPropertyAggregatesRequestRequestTypeDef",
    {
        "aggregateTypes": Sequence[AggregateTypeType],
        "resolution": str,
        "startDate": TimestampTypeDef,
        "endDate": TimestampTypeDef,
        "assetId": NotRequired[str],
        "propertyId": NotRequired[str],
        "propertyAlias": NotRequired[str],
        "qualities": NotRequired[Sequence[QualityType]],
        "timeOrdering": NotRequired[TimeOrderingType],
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)

GetAssetPropertyValueHistoryRequestRequestTypeDef = TypedDict(
    "GetAssetPropertyValueHistoryRequestRequestTypeDef",
    {
        "assetId": NotRequired[str],
        "propertyId": NotRequired[str],
        "propertyAlias": NotRequired[str],
        "startDate": NotRequired[TimestampTypeDef],
        "endDate": NotRequired[TimestampTypeDef],
        "qualities": NotRequired[Sequence[QualityType]],
        "timeOrdering": NotRequired[TimeOrderingType],
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)

BatchGetAssetPropertyAggregatesSkippedEntryTypeDef = TypedDict(
    "BatchGetAssetPropertyAggregatesSkippedEntryTypeDef",
    {
        "entryId": str,
        "completionStatus": BatchEntryCompletionStatusType,
        "errorInfo": NotRequired[BatchGetAssetPropertyAggregatesErrorInfoTypeDef],
    },
)

BatchGetAssetPropertyValueRequestRequestTypeDef = TypedDict(
    "BatchGetAssetPropertyValueRequestRequestTypeDef",
    {
        "entries": Sequence[BatchGetAssetPropertyValueEntryTypeDef],
        "nextToken": NotRequired[str],
    },
)

BatchGetAssetPropertyValueSkippedEntryTypeDef = TypedDict(
    "BatchGetAssetPropertyValueSkippedEntryTypeDef",
    {
        "entryId": str,
        "completionStatus": BatchEntryCompletionStatusType,
        "errorInfo": NotRequired[BatchGetAssetPropertyValueErrorInfoTypeDef],
    },
)

BatchGetAssetPropertyValueHistorySkippedEntryTypeDef = TypedDict(
    "BatchGetAssetPropertyValueHistorySkippedEntryTypeDef",
    {
        "entryId": str,
        "completionStatus": BatchEntryCompletionStatusType,
        "errorInfo": NotRequired[BatchGetAssetPropertyValueHistoryErrorInfoTypeDef],
    },
)

ImageFileTypeDef = TypedDict(
    "ImageFileTypeDef",
    {
        "data": BlobTypeDef,
        "type": Literal["PNG"],
    },
)

ConfigurationStatusTypeDef = TypedDict(
    "ConfigurationStatusTypeDef",
    {
        "state": ConfigurationStateType,
        "error": NotRequired[ConfigurationErrorDetailsTypeDef],
    },
)

FileFormatTypeDef = TypedDict(
    "FileFormatTypeDef",
    {
        "csv": NotRequired[CsvTypeDef],
    },
)

MultiLayerStorageTypeDef = TypedDict(
    "MultiLayerStorageTypeDef",
    {
        "customerManagedS3Storage": CustomerManagedS3StorageTypeDef,
    },
)

ListDashboardsResponseTypeDef = TypedDict(
    "ListDashboardsResponseTypeDef",
    {
        "dashboardSummaries": List[DashboardSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAssetModelRequestAssetModelActiveWaitTypeDef = TypedDict(
    "DescribeAssetModelRequestAssetModelActiveWaitTypeDef",
    {
        "assetModelId": str,
        "excludeProperties": NotRequired[bool],
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)

DescribeAssetModelRequestAssetModelNotExistsWaitTypeDef = TypedDict(
    "DescribeAssetModelRequestAssetModelNotExistsWaitTypeDef",
    {
        "assetModelId": str,
        "excludeProperties": NotRequired[bool],
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)

DescribeAssetRequestAssetActiveWaitTypeDef = TypedDict(
    "DescribeAssetRequestAssetActiveWaitTypeDef",
    {
        "assetId": str,
        "excludeProperties": NotRequired[bool],
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)

DescribeAssetRequestAssetNotExistsWaitTypeDef = TypedDict(
    "DescribeAssetRequestAssetNotExistsWaitTypeDef",
    {
        "assetId": str,
        "excludeProperties": NotRequired[bool],
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)

DescribePortalRequestPortalActiveWaitTypeDef = TypedDict(
    "DescribePortalRequestPortalActiveWaitTypeDef",
    {
        "portalId": str,
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)

DescribePortalRequestPortalNotExistsWaitTypeDef = TypedDict(
    "DescribePortalRequestPortalNotExistsWaitTypeDef",
    {
        "portalId": str,
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)

DescribeLoggingOptionsResponseTypeDef = TypedDict(
    "DescribeLoggingOptionsResponseTypeDef",
    {
        "loggingOptions": LoggingOptionsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutLoggingOptionsRequestRequestTypeDef = TypedDict(
    "PutLoggingOptionsRequestRequestTypeDef",
    {
        "loggingOptions": LoggingOptionsTypeDef,
    },
)

ErrorDetailsTypeDef = TypedDict(
    "ErrorDetailsTypeDef",
    {
        "code": ErrorCodeType,
        "message": str,
        "details": NotRequired[List[DetailedErrorTypeDef]],
    },
)

ExpressionVariableTypeDef = TypedDict(
    "ExpressionVariableTypeDef",
    {
        "name": str,
        "value": VariableValueTypeDef,
    },
)

MeasurementProcessingConfigTypeDef = TypedDict(
    "MeasurementProcessingConfigTypeDef",
    {
        "forwardingConfig": ForwardingConfigTypeDef,
    },
)

TransformProcessingConfigTypeDef = TypedDict(
    "TransformProcessingConfigTypeDef",
    {
        "computeLocation": ComputeLocationType,
        "forwardingConfig": NotRequired[ForwardingConfigTypeDef],
    },
)

GatewayPlatformTypeDef = TypedDict(
    "GatewayPlatformTypeDef",
    {
        "greengrass": NotRequired[GreengrassTypeDef],
        "greengrassV2": NotRequired[GreengrassV2TypeDef],
    },
)

GetAssetPropertyAggregatesRequestGetAssetPropertyAggregatesPaginateTypeDef = TypedDict(
    "GetAssetPropertyAggregatesRequestGetAssetPropertyAggregatesPaginateTypeDef",
    {
        "aggregateTypes": Sequence[AggregateTypeType],
        "resolution": str,
        "startDate": TimestampTypeDef,
        "endDate": TimestampTypeDef,
        "assetId": NotRequired[str],
        "propertyId": NotRequired[str],
        "propertyAlias": NotRequired[str],
        "qualities": NotRequired[Sequence[QualityType]],
        "timeOrdering": NotRequired[TimeOrderingType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

GetAssetPropertyValueHistoryRequestGetAssetPropertyValueHistoryPaginateTypeDef = TypedDict(
    "GetAssetPropertyValueHistoryRequestGetAssetPropertyValueHistoryPaginateTypeDef",
    {
        "assetId": NotRequired[str],
        "propertyId": NotRequired[str],
        "propertyAlias": NotRequired[str],
        "startDate": NotRequired[TimestampTypeDef],
        "endDate": NotRequired[TimestampTypeDef],
        "qualities": NotRequired[Sequence[QualityType]],
        "timeOrdering": NotRequired[TimeOrderingType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

GetInterpolatedAssetPropertyValuesRequestGetInterpolatedAssetPropertyValuesPaginateTypeDef = TypedDict(
    "GetInterpolatedAssetPropertyValuesRequestGetInterpolatedAssetPropertyValuesPaginateTypeDef",
    {
        "startTimeInSeconds": int,
        "endTimeInSeconds": int,
        "quality": QualityType,
        "intervalInSeconds": int,
        "type": str,
        "assetId": NotRequired[str],
        "propertyId": NotRequired[str],
        "propertyAlias": NotRequired[str],
        "startTimeOffsetInNanos": NotRequired[int],
        "endTimeOffsetInNanos": NotRequired[int],
        "intervalWindowInSeconds": NotRequired[int],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListAccessPoliciesRequestListAccessPoliciesPaginateTypeDef = TypedDict(
    "ListAccessPoliciesRequestListAccessPoliciesPaginateTypeDef",
    {
        "identityType": NotRequired[IdentityTypeType],
        "identityId": NotRequired[str],
        "resourceType": NotRequired[ResourceTypeType],
        "resourceId": NotRequired[str],
        "iamArn": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListAssetModelPropertiesRequestListAssetModelPropertiesPaginateTypeDef = TypedDict(
    "ListAssetModelPropertiesRequestListAssetModelPropertiesPaginateTypeDef",
    {
        "assetModelId": str,
        "filter": NotRequired[ListAssetModelPropertiesFilterType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListAssetModelsRequestListAssetModelsPaginateTypeDef = TypedDict(
    "ListAssetModelsRequestListAssetModelsPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListAssetPropertiesRequestListAssetPropertiesPaginateTypeDef = TypedDict(
    "ListAssetPropertiesRequestListAssetPropertiesPaginateTypeDef",
    {
        "assetId": str,
        "filter": NotRequired[ListAssetPropertiesFilterType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListAssetRelationshipsRequestListAssetRelationshipsPaginateTypeDef = TypedDict(
    "ListAssetRelationshipsRequestListAssetRelationshipsPaginateTypeDef",
    {
        "assetId": str,
        "traversalType": Literal["PATH_TO_ROOT"],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListAssetsRequestListAssetsPaginateTypeDef = TypedDict(
    "ListAssetsRequestListAssetsPaginateTypeDef",
    {
        "assetModelId": NotRequired[str],
        "filter": NotRequired[ListAssetsFilterType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListAssociatedAssetsRequestListAssociatedAssetsPaginateTypeDef = TypedDict(
    "ListAssociatedAssetsRequestListAssociatedAssetsPaginateTypeDef",
    {
        "assetId": str,
        "hierarchyId": NotRequired[str],
        "traversalDirection": NotRequired[TraversalDirectionType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListBulkImportJobsRequestListBulkImportJobsPaginateTypeDef = TypedDict(
    "ListBulkImportJobsRequestListBulkImportJobsPaginateTypeDef",
    {
        "filter": NotRequired[ListBulkImportJobsFilterType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListDashboardsRequestListDashboardsPaginateTypeDef = TypedDict(
    "ListDashboardsRequestListDashboardsPaginateTypeDef",
    {
        "projectId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListGatewaysRequestListGatewaysPaginateTypeDef = TypedDict(
    "ListGatewaysRequestListGatewaysPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListPortalsRequestListPortalsPaginateTypeDef = TypedDict(
    "ListPortalsRequestListPortalsPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListProjectAssetsRequestListProjectAssetsPaginateTypeDef = TypedDict(
    "ListProjectAssetsRequestListProjectAssetsPaginateTypeDef",
    {
        "projectId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListProjectsRequestListProjectsPaginateTypeDef = TypedDict(
    "ListProjectsRequestListProjectsPaginateTypeDef",
    {
        "portalId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListTimeSeriesRequestListTimeSeriesPaginateTypeDef = TypedDict(
    "ListTimeSeriesRequestListTimeSeriesPaginateTypeDef",
    {
        "assetId": NotRequired[str],
        "aliasPrefix": NotRequired[str],
        "timeSeriesType": NotRequired[ListTimeSeriesTypeType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

IdentityTypeDef = TypedDict(
    "IdentityTypeDef",
    {
        "user": NotRequired[UserIdentityTypeDef],
        "group": NotRequired[GroupIdentityTypeDef],
        "iamUser": NotRequired[IAMUserIdentityTypeDef],
        "iamRole": NotRequired[IAMRoleIdentityTypeDef],
    },
)

ListBulkImportJobsResponseTypeDef = TypedDict(
    "ListBulkImportJobsResponseTypeDef",
    {
        "jobSummaries": List[JobSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListProjectsResponseTypeDef = TypedDict(
    "ListProjectsResponseTypeDef",
    {
        "projectSummaries": List[ProjectSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTimeSeriesResponseTypeDef = TypedDict(
    "ListTimeSeriesResponseTypeDef",
    {
        "TimeSeriesSummaries": List[TimeSeriesSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

MetricWindowTypeDef = TypedDict(
    "MetricWindowTypeDef",
    {
        "tumbling": NotRequired[TumblingWindowTypeDef],
    },
)

PortalStatusTypeDef = TypedDict(
    "PortalStatusTypeDef",
    {
        "state": PortalStateType,
        "error": NotRequired[MonitorErrorDetailsTypeDef],
    },
)

ResourceTypeDef = TypedDict(
    "ResourceTypeDef",
    {
        "portal": NotRequired[PortalResourceTypeDef],
        "project": NotRequired[ProjectResourceTypeDef],
    },
)

BatchGetAssetPropertyAggregatesSuccessEntryTypeDef = TypedDict(
    "BatchGetAssetPropertyAggregatesSuccessEntryTypeDef",
    {
        "entryId": str,
        "aggregatedValues": List[AggregatedValueTypeDef],
    },
)

GetAssetPropertyAggregatesResponseTypeDef = TypedDict(
    "GetAssetPropertyAggregatesResponseTypeDef",
    {
        "aggregatedValues": List[AggregatedValueTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAssetRelationshipsResponseTypeDef = TypedDict(
    "ListAssetRelationshipsResponseTypeDef",
    {
        "assetRelationshipSummaries": List[AssetRelationshipSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAssetPropertiesResponseTypeDef = TypedDict(
    "ListAssetPropertiesResponseTypeDef",
    {
        "assetPropertySummaries": List[AssetPropertySummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssetCompositeModelTypeDef = TypedDict(
    "AssetCompositeModelTypeDef",
    {
        "name": str,
        "type": str,
        "properties": List[AssetPropertyTypeDef],
        "description": NotRequired[str],
        "id": NotRequired[str],
    },
)

BatchPutAssetPropertyErrorEntryTypeDef = TypedDict(
    "BatchPutAssetPropertyErrorEntryTypeDef",
    {
        "entryId": str,
        "errors": List[BatchPutAssetPropertyErrorTypeDef],
    },
)

BatchGetAssetPropertyValueHistorySuccessEntryTypeDef = TypedDict(
    "BatchGetAssetPropertyValueHistorySuccessEntryTypeDef",
    {
        "entryId": str,
        "assetPropertyValueHistory": List[AssetPropertyValueTypeDef],
    },
)

BatchGetAssetPropertyValueSuccessEntryTypeDef = TypedDict(
    "BatchGetAssetPropertyValueSuccessEntryTypeDef",
    {
        "entryId": str,
        "assetPropertyValue": NotRequired[AssetPropertyValueTypeDef],
    },
)

GetAssetPropertyValueHistoryResponseTypeDef = TypedDict(
    "GetAssetPropertyValueHistoryResponseTypeDef",
    {
        "assetPropertyValueHistory": List[AssetPropertyValueTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAssetPropertyValueResponseTypeDef = TypedDict(
    "GetAssetPropertyValueResponseTypeDef",
    {
        "propertyValue": AssetPropertyValueTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutAssetPropertyValueEntryTypeDef = TypedDict(
    "PutAssetPropertyValueEntryTypeDef",
    {
        "entryId": str,
        "propertyValues": Sequence[AssetPropertyValueTypeDef],
        "assetId": NotRequired[str],
        "propertyId": NotRequired[str],
        "propertyAlias": NotRequired[str],
    },
)

GetInterpolatedAssetPropertyValuesResponseTypeDef = TypedDict(
    "GetInterpolatedAssetPropertyValuesResponseTypeDef",
    {
        "interpolatedAssetPropertyValues": List[InterpolatedAssetPropertyValueTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchGetAssetPropertyAggregatesRequestRequestTypeDef = TypedDict(
    "BatchGetAssetPropertyAggregatesRequestRequestTypeDef",
    {
        "entries": Sequence[BatchGetAssetPropertyAggregatesEntryTypeDef],
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)

BatchGetAssetPropertyValueHistoryRequestRequestTypeDef = TypedDict(
    "BatchGetAssetPropertyValueHistoryRequestRequestTypeDef",
    {
        "entries": Sequence[BatchGetAssetPropertyValueHistoryEntryTypeDef],
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)

CreatePortalRequestRequestTypeDef = TypedDict(
    "CreatePortalRequestRequestTypeDef",
    {
        "portalName": str,
        "portalContactEmail": str,
        "roleArn": str,
        "portalDescription": NotRequired[str],
        "clientToken": NotRequired[str],
        "portalLogoImageFile": NotRequired[ImageFileTypeDef],
        "tags": NotRequired[Mapping[str, str]],
        "portalAuthMode": NotRequired[AuthModeType],
        "notificationSenderEmail": NotRequired[str],
        "alarms": NotRequired[AlarmsTypeDef],
    },
)

ImageTypeDef = TypedDict(
    "ImageTypeDef",
    {
        "id": NotRequired[str],
        "file": NotRequired[ImageFileTypeDef],
    },
)

DescribeDefaultEncryptionConfigurationResponseTypeDef = TypedDict(
    "DescribeDefaultEncryptionConfigurationResponseTypeDef",
    {
        "encryptionType": EncryptionTypeType,
        "kmsKeyArn": str,
        "configurationStatus": ConfigurationStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutDefaultEncryptionConfigurationResponseTypeDef = TypedDict(
    "PutDefaultEncryptionConfigurationResponseTypeDef",
    {
        "encryptionType": EncryptionTypeType,
        "kmsKeyArn": str,
        "configurationStatus": ConfigurationStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

JobConfigurationTypeDef = TypedDict(
    "JobConfigurationTypeDef",
    {
        "fileFormat": FileFormatTypeDef,
    },
)

DescribeStorageConfigurationResponseTypeDef = TypedDict(
    "DescribeStorageConfigurationResponseTypeDef",
    {
        "storageType": StorageTypeType,
        "multiLayerStorage": MultiLayerStorageTypeDef,
        "disassociatedDataStorage": DisassociatedDataStorageStateType,
        "retentionPeriod": RetentionPeriodTypeDef,
        "configurationStatus": ConfigurationStatusTypeDef,
        "lastUpdateDate": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutStorageConfigurationRequestRequestTypeDef = TypedDict(
    "PutStorageConfigurationRequestRequestTypeDef",
    {
        "storageType": StorageTypeType,
        "multiLayerStorage": NotRequired[MultiLayerStorageTypeDef],
        "disassociatedDataStorage": NotRequired[DisassociatedDataStorageStateType],
        "retentionPeriod": NotRequired[RetentionPeriodTypeDef],
    },
)

PutStorageConfigurationResponseTypeDef = TypedDict(
    "PutStorageConfigurationResponseTypeDef",
    {
        "storageType": StorageTypeType,
        "multiLayerStorage": MultiLayerStorageTypeDef,
        "disassociatedDataStorage": DisassociatedDataStorageStateType,
        "retentionPeriod": RetentionPeriodTypeDef,
        "configurationStatus": ConfigurationStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssetModelStatusTypeDef = TypedDict(
    "AssetModelStatusTypeDef",
    {
        "state": AssetModelStateType,
        "error": NotRequired[ErrorDetailsTypeDef],
    },
)

AssetStatusTypeDef = TypedDict(
    "AssetStatusTypeDef",
    {
        "state": AssetStateType,
        "error": NotRequired[ErrorDetailsTypeDef],
    },
)

MeasurementTypeDef = TypedDict(
    "MeasurementTypeDef",
    {
        "processingConfig": NotRequired[MeasurementProcessingConfigTypeDef],
    },
)

TransformPaginatorTypeDef = TypedDict(
    "TransformPaginatorTypeDef",
    {
        "expression": str,
        "variables": List[ExpressionVariableTypeDef],
        "processingConfig": NotRequired[TransformProcessingConfigTypeDef],
    },
)

TransformTypeDef = TypedDict(
    "TransformTypeDef",
    {
        "expression": str,
        "variables": Sequence[ExpressionVariableTypeDef],
        "processingConfig": NotRequired[TransformProcessingConfigTypeDef],
    },
)

CreateGatewayRequestRequestTypeDef = TypedDict(
    "CreateGatewayRequestRequestTypeDef",
    {
        "gatewayName": str,
        "gatewayPlatform": GatewayPlatformTypeDef,
        "tags": NotRequired[Mapping[str, str]],
    },
)

DescribeGatewayResponseTypeDef = TypedDict(
    "DescribeGatewayResponseTypeDef",
    {
        "gatewayId": str,
        "gatewayName": str,
        "gatewayArn": str,
        "gatewayPlatform": GatewayPlatformTypeDef,
        "gatewayCapabilitySummaries": List[GatewayCapabilitySummaryTypeDef],
        "creationDate": datetime,
        "lastUpdateDate": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GatewaySummaryTypeDef = TypedDict(
    "GatewaySummaryTypeDef",
    {
        "gatewayId": str,
        "gatewayName": str,
        "creationDate": datetime,
        "lastUpdateDate": datetime,
        "gatewayPlatform": NotRequired[GatewayPlatformTypeDef],
        "gatewayCapabilitySummaries": NotRequired[List[GatewayCapabilitySummaryTypeDef]],
    },
)

MetricPaginatorTypeDef = TypedDict(
    "MetricPaginatorTypeDef",
    {
        "expression": str,
        "variables": List[ExpressionVariableTypeDef],
        "window": MetricWindowTypeDef,
        "processingConfig": NotRequired[MetricProcessingConfigTypeDef],
    },
)

MetricTypeDef = TypedDict(
    "MetricTypeDef",
    {
        "expression": str,
        "variables": Sequence[ExpressionVariableTypeDef],
        "window": MetricWindowTypeDef,
        "processingConfig": NotRequired[MetricProcessingConfigTypeDef],
    },
)

CreatePortalResponseTypeDef = TypedDict(
    "CreatePortalResponseTypeDef",
    {
        "portalId": str,
        "portalArn": str,
        "portalStartUrl": str,
        "portalStatus": PortalStatusTypeDef,
        "ssoApplicationId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeletePortalResponseTypeDef = TypedDict(
    "DeletePortalResponseTypeDef",
    {
        "portalStatus": PortalStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribePortalResponseTypeDef = TypedDict(
    "DescribePortalResponseTypeDef",
    {
        "portalId": str,
        "portalArn": str,
        "portalName": str,
        "portalDescription": str,
        "portalClientId": str,
        "portalStartUrl": str,
        "portalContactEmail": str,
        "portalStatus": PortalStatusTypeDef,
        "portalCreationDate": datetime,
        "portalLastUpdateDate": datetime,
        "portalLogoImageLocation": ImageLocationTypeDef,
        "roleArn": str,
        "portalAuthMode": AuthModeType,
        "notificationSenderEmail": str,
        "alarms": AlarmsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PortalSummaryTypeDef = TypedDict(
    "PortalSummaryTypeDef",
    {
        "id": str,
        "name": str,
        "startUrl": str,
        "status": PortalStatusTypeDef,
        "description": NotRequired[str],
        "creationDate": NotRequired[datetime],
        "lastUpdateDate": NotRequired[datetime],
        "roleArn": NotRequired[str],
    },
)

UpdatePortalResponseTypeDef = TypedDict(
    "UpdatePortalResponseTypeDef",
    {
        "portalStatus": PortalStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AccessPolicySummaryTypeDef = TypedDict(
    "AccessPolicySummaryTypeDef",
    {
        "id": str,
        "identity": IdentityTypeDef,
        "resource": ResourceTypeDef,
        "permission": PermissionType,
        "creationDate": NotRequired[datetime],
        "lastUpdateDate": NotRequired[datetime],
    },
)

CreateAccessPolicyRequestRequestTypeDef = TypedDict(
    "CreateAccessPolicyRequestRequestTypeDef",
    {
        "accessPolicyIdentity": IdentityTypeDef,
        "accessPolicyResource": ResourceTypeDef,
        "accessPolicyPermission": PermissionType,
        "clientToken": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)

DescribeAccessPolicyResponseTypeDef = TypedDict(
    "DescribeAccessPolicyResponseTypeDef",
    {
        "accessPolicyId": str,
        "accessPolicyArn": str,
        "accessPolicyIdentity": IdentityTypeDef,
        "accessPolicyResource": ResourceTypeDef,
        "accessPolicyPermission": PermissionType,
        "accessPolicyCreationDate": datetime,
        "accessPolicyLastUpdateDate": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAccessPolicyRequestRequestTypeDef = TypedDict(
    "UpdateAccessPolicyRequestRequestTypeDef",
    {
        "accessPolicyId": str,
        "accessPolicyIdentity": IdentityTypeDef,
        "accessPolicyResource": ResourceTypeDef,
        "accessPolicyPermission": PermissionType,
        "clientToken": NotRequired[str],
    },
)

BatchGetAssetPropertyAggregatesResponseTypeDef = TypedDict(
    "BatchGetAssetPropertyAggregatesResponseTypeDef",
    {
        "errorEntries": List[BatchGetAssetPropertyAggregatesErrorEntryTypeDef],
        "successEntries": List[BatchGetAssetPropertyAggregatesSuccessEntryTypeDef],
        "skippedEntries": List[BatchGetAssetPropertyAggregatesSkippedEntryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchPutAssetPropertyValueResponseTypeDef = TypedDict(
    "BatchPutAssetPropertyValueResponseTypeDef",
    {
        "errorEntries": List[BatchPutAssetPropertyErrorEntryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchGetAssetPropertyValueHistoryResponseTypeDef = TypedDict(
    "BatchGetAssetPropertyValueHistoryResponseTypeDef",
    {
        "errorEntries": List[BatchGetAssetPropertyValueHistoryErrorEntryTypeDef],
        "successEntries": List[BatchGetAssetPropertyValueHistorySuccessEntryTypeDef],
        "skippedEntries": List[BatchGetAssetPropertyValueHistorySkippedEntryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchGetAssetPropertyValueResponseTypeDef = TypedDict(
    "BatchGetAssetPropertyValueResponseTypeDef",
    {
        "errorEntries": List[BatchGetAssetPropertyValueErrorEntryTypeDef],
        "successEntries": List[BatchGetAssetPropertyValueSuccessEntryTypeDef],
        "skippedEntries": List[BatchGetAssetPropertyValueSkippedEntryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchPutAssetPropertyValueRequestRequestTypeDef = TypedDict(
    "BatchPutAssetPropertyValueRequestRequestTypeDef",
    {
        "entries": Sequence[PutAssetPropertyValueEntryTypeDef],
    },
)

UpdatePortalRequestRequestTypeDef = TypedDict(
    "UpdatePortalRequestRequestTypeDef",
    {
        "portalId": str,
        "portalName": str,
        "portalContactEmail": str,
        "roleArn": str,
        "portalDescription": NotRequired[str],
        "portalLogoImage": NotRequired[ImageTypeDef],
        "clientToken": NotRequired[str],
        "notificationSenderEmail": NotRequired[str],
        "alarms": NotRequired[AlarmsTypeDef],
    },
)

CreateBulkImportJobRequestRequestTypeDef = TypedDict(
    "CreateBulkImportJobRequestRequestTypeDef",
    {
        "jobName": str,
        "jobRoleArn": str,
        "files": Sequence[FileTypeDef],
        "errorReportLocation": ErrorReportLocationTypeDef,
        "jobConfiguration": JobConfigurationTypeDef,
    },
)

DescribeBulkImportJobResponseTypeDef = TypedDict(
    "DescribeBulkImportJobResponseTypeDef",
    {
        "jobId": str,
        "jobName": str,
        "jobStatus": JobStatusType,
        "jobRoleArn": str,
        "files": List[FileTypeDef],
        "errorReportLocation": ErrorReportLocationTypeDef,
        "jobConfiguration": JobConfigurationTypeDef,
        "jobCreationDate": datetime,
        "jobLastUpdateDate": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssetModelSummaryTypeDef = TypedDict(
    "AssetModelSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "description": str,
        "creationDate": datetime,
        "lastUpdateDate": datetime,
        "status": AssetModelStatusTypeDef,
    },
)

CreateAssetModelResponseTypeDef = TypedDict(
    "CreateAssetModelResponseTypeDef",
    {
        "assetModelId": str,
        "assetModelArn": str,
        "assetModelStatus": AssetModelStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteAssetModelResponseTypeDef = TypedDict(
    "DeleteAssetModelResponseTypeDef",
    {
        "assetModelStatus": AssetModelStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAssetModelResponseTypeDef = TypedDict(
    "UpdateAssetModelResponseTypeDef",
    {
        "assetModelStatus": AssetModelStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssetSummaryTypeDef = TypedDict(
    "AssetSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "assetModelId": str,
        "creationDate": datetime,
        "lastUpdateDate": datetime,
        "status": AssetStatusTypeDef,
        "hierarchies": List[AssetHierarchyTypeDef],
        "description": NotRequired[str],
    },
)

AssociatedAssetsSummaryTypeDef = TypedDict(
    "AssociatedAssetsSummaryTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "assetModelId": str,
        "creationDate": datetime,
        "lastUpdateDate": datetime,
        "status": AssetStatusTypeDef,
        "hierarchies": List[AssetHierarchyTypeDef],
        "description": NotRequired[str],
    },
)

CreateAssetResponseTypeDef = TypedDict(
    "CreateAssetResponseTypeDef",
    {
        "assetId": str,
        "assetArn": str,
        "assetStatus": AssetStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteAssetResponseTypeDef = TypedDict(
    "DeleteAssetResponseTypeDef",
    {
        "assetStatus": AssetStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAssetResponseTypeDef = TypedDict(
    "DescribeAssetResponseTypeDef",
    {
        "assetId": str,
        "assetArn": str,
        "assetName": str,
        "assetModelId": str,
        "assetProperties": List[AssetPropertyTypeDef],
        "assetHierarchies": List[AssetHierarchyTypeDef],
        "assetCompositeModels": List[AssetCompositeModelTypeDef],
        "assetCreationDate": datetime,
        "assetLastUpdateDate": datetime,
        "assetStatus": AssetStatusTypeDef,
        "assetDescription": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAssetResponseTypeDef = TypedDict(
    "UpdateAssetResponseTypeDef",
    {
        "assetStatus": AssetStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListGatewaysResponseTypeDef = TypedDict(
    "ListGatewaysResponseTypeDef",
    {
        "gatewaySummaries": List[GatewaySummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PropertyTypePaginatorTypeDef = TypedDict(
    "PropertyTypePaginatorTypeDef",
    {
        "attribute": NotRequired[AttributeTypeDef],
        "measurement": NotRequired[MeasurementTypeDef],
        "transform": NotRequired[TransformPaginatorTypeDef],
        "metric": NotRequired[MetricPaginatorTypeDef],
    },
)

PropertyTypeTypeDef = TypedDict(
    "PropertyTypeTypeDef",
    {
        "attribute": NotRequired[AttributeTypeDef],
        "measurement": NotRequired[MeasurementTypeDef],
        "transform": NotRequired[TransformTypeDef],
        "metric": NotRequired[MetricTypeDef],
    },
)

ListPortalsResponseTypeDef = TypedDict(
    "ListPortalsResponseTypeDef",
    {
        "portalSummaries": List[PortalSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAccessPoliciesResponseTypeDef = TypedDict(
    "ListAccessPoliciesResponseTypeDef",
    {
        "accessPolicySummaries": List[AccessPolicySummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAssetModelsResponseTypeDef = TypedDict(
    "ListAssetModelsResponseTypeDef",
    {
        "assetModelSummaries": List[AssetModelSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAssetsResponseTypeDef = TypedDict(
    "ListAssetsResponseTypeDef",
    {
        "assetSummaries": List[AssetSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAssociatedAssetsResponseTypeDef = TypedDict(
    "ListAssociatedAssetsResponseTypeDef",
    {
        "assetSummaries": List[AssociatedAssetsSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssetModelPropertySummaryPaginatorTypeDef = TypedDict(
    "AssetModelPropertySummaryPaginatorTypeDef",
    {
        "name": str,
        "dataType": PropertyDataTypeType,
        "type": PropertyTypePaginatorTypeDef,
        "id": NotRequired[str],
        "dataTypeSpec": NotRequired[str],
        "unit": NotRequired[str],
        "assetModelCompositeModelId": NotRequired[str],
    },
)

AssetModelPropertyDefinitionTypeDef = TypedDict(
    "AssetModelPropertyDefinitionTypeDef",
    {
        "name": str,
        "dataType": PropertyDataTypeType,
        "type": PropertyTypeTypeDef,
        "dataTypeSpec": NotRequired[str],
        "unit": NotRequired[str],
    },
)

AssetModelPropertySummaryTypeDef = TypedDict(
    "AssetModelPropertySummaryTypeDef",
    {
        "name": str,
        "dataType": PropertyDataTypeType,
        "type": PropertyTypeTypeDef,
        "id": NotRequired[str],
        "dataTypeSpec": NotRequired[str],
        "unit": NotRequired[str],
        "assetModelCompositeModelId": NotRequired[str],
    },
)

AssetModelPropertyTypeDef = TypedDict(
    "AssetModelPropertyTypeDef",
    {
        "name": str,
        "dataType": PropertyDataTypeType,
        "type": PropertyTypeTypeDef,
        "id": NotRequired[str],
        "dataTypeSpec": NotRequired[str],
        "unit": NotRequired[str],
    },
)

PropertyTypeDef = TypedDict(
    "PropertyTypeDef",
    {
        "id": str,
        "name": str,
        "dataType": PropertyDataTypeType,
        "alias": NotRequired[str],
        "notification": NotRequired[PropertyNotificationTypeDef],
        "unit": NotRequired[str],
        "type": NotRequired[PropertyTypeTypeDef],
    },
)

ListAssetModelPropertiesResponsePaginatorTypeDef = TypedDict(
    "ListAssetModelPropertiesResponsePaginatorTypeDef",
    {
        "assetModelPropertySummaries": List[AssetModelPropertySummaryPaginatorTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssetModelCompositeModelDefinitionTypeDef = TypedDict(
    "AssetModelCompositeModelDefinitionTypeDef",
    {
        "name": str,
        "type": str,
        "description": NotRequired[str],
        "properties": NotRequired[Sequence[AssetModelPropertyDefinitionTypeDef]],
    },
)

ListAssetModelPropertiesResponseTypeDef = TypedDict(
    "ListAssetModelPropertiesResponseTypeDef",
    {
        "assetModelPropertySummaries": List[AssetModelPropertySummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssetModelCompositeModelTypeDef = TypedDict(
    "AssetModelCompositeModelTypeDef",
    {
        "name": str,
        "type": str,
        "description": NotRequired[str],
        "properties": NotRequired[List[AssetModelPropertyTypeDef]],
        "id": NotRequired[str],
    },
)

CompositeModelPropertyTypeDef = TypedDict(
    "CompositeModelPropertyTypeDef",
    {
        "name": str,
        "type": str,
        "assetProperty": PropertyTypeDef,
        "id": NotRequired[str],
    },
)

CreateAssetModelRequestRequestTypeDef = TypedDict(
    "CreateAssetModelRequestRequestTypeDef",
    {
        "assetModelName": str,
        "assetModelDescription": NotRequired[str],
        "assetModelProperties": NotRequired[Sequence[AssetModelPropertyDefinitionTypeDef]],
        "assetModelHierarchies": NotRequired[Sequence[AssetModelHierarchyDefinitionTypeDef]],
        "assetModelCompositeModels": NotRequired[
            Sequence[AssetModelCompositeModelDefinitionTypeDef]
        ],
        "clientToken": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)

DescribeAssetModelResponseTypeDef = TypedDict(
    "DescribeAssetModelResponseTypeDef",
    {
        "assetModelId": str,
        "assetModelArn": str,
        "assetModelName": str,
        "assetModelDescription": str,
        "assetModelProperties": List[AssetModelPropertyTypeDef],
        "assetModelHierarchies": List[AssetModelHierarchyTypeDef],
        "assetModelCompositeModels": List[AssetModelCompositeModelTypeDef],
        "assetModelCreationDate": datetime,
        "assetModelLastUpdateDate": datetime,
        "assetModelStatus": AssetModelStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAssetModelRequestRequestTypeDef = TypedDict(
    "UpdateAssetModelRequestRequestTypeDef",
    {
        "assetModelId": str,
        "assetModelName": str,
        "assetModelDescription": NotRequired[str],
        "assetModelProperties": NotRequired[Sequence[AssetModelPropertyTypeDef]],
        "assetModelHierarchies": NotRequired[Sequence[AssetModelHierarchyTypeDef]],
        "assetModelCompositeModels": NotRequired[Sequence[AssetModelCompositeModelTypeDef]],
        "clientToken": NotRequired[str],
    },
)

DescribeAssetPropertyResponseTypeDef = TypedDict(
    "DescribeAssetPropertyResponseTypeDef",
    {
        "assetId": str,
        "assetName": str,
        "assetModelId": str,
        "assetProperty": PropertyTypeDef,
        "compositeModel": CompositeModelPropertyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
