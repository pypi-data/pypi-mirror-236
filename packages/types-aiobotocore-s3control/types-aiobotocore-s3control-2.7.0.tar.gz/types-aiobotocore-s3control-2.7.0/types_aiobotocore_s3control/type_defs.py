"""
Type annotations for s3control service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/type_defs/)

Usage::

    ```python
    from types_aiobotocore_s3control.type_defs import AbortIncompleteMultipartUploadTypeDef

    data: AbortIncompleteMultipartUploadTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence, Union

from .literals import (
    AsyncOperationNameType,
    BucketCannedACLType,
    BucketLocationConstraintType,
    BucketVersioningStatusType,
    DeleteMarkerReplicationStatusType,
    ExistingObjectReplicationStatusType,
    ExpirationStatusType,
    FormatType,
    JobManifestFieldNameType,
    JobManifestFormatType,
    JobReportScopeType,
    JobStatusType,
    MetricsStatusType,
    MFADeleteStatusType,
    MFADeleteType,
    MultiRegionAccessPointStatusType,
    NetworkOriginType,
    ObjectLambdaAccessPointAliasStatusType,
    ObjectLambdaAllowedFeatureType,
    ObjectLambdaTransformationConfigurationActionType,
    OperationNameType,
    ReplicaModificationsStatusType,
    ReplicationRuleStatusType,
    ReplicationStatusType,
    ReplicationStorageClassType,
    ReplicationTimeStatusType,
    RequestedJobStatusType,
    S3CannedAccessControlListType,
    S3ChecksumAlgorithmType,
    S3GlacierJobTierType,
    S3GranteeTypeIdentifierType,
    S3MetadataDirectiveType,
    S3ObjectLockLegalHoldStatusType,
    S3ObjectLockModeType,
    S3ObjectLockRetentionModeType,
    S3PermissionType,
    S3SSEAlgorithmType,
    S3StorageClassType,
    SseKmsEncryptedObjectsStatusType,
    TransitionStorageClassType,
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
    "AbortIncompleteMultipartUploadTypeDef",
    "AccessControlTranslationTypeDef",
    "VpcConfigurationTypeDef",
    "ActivityMetricsTypeDef",
    "AdvancedCostOptimizationMetricsTypeDef",
    "AdvancedDataProtectionMetricsTypeDef",
    "DetailedStatusCodesMetricsTypeDef",
    "AsyncErrorDetailsTypeDef",
    "DeleteMultiRegionAccessPointInputTypeDef",
    "PutMultiRegionAccessPointPolicyInputTypeDef",
    "AwsLambdaTransformationTypeDef",
    "CloudWatchMetricsTypeDef",
    "ObjectLambdaAccessPointAliasTypeDef",
    "ResponseMetadataTypeDef",
    "PublicAccessBlockConfigurationTypeDef",
    "CreateBucketConfigurationTypeDef",
    "JobReportTypeDef",
    "S3TagTypeDef",
    "RegionTypeDef",
    "DeleteAccessPointForObjectLambdaRequestRequestTypeDef",
    "DeleteAccessPointPolicyForObjectLambdaRequestRequestTypeDef",
    "DeleteAccessPointPolicyRequestRequestTypeDef",
    "DeleteAccessPointRequestRequestTypeDef",
    "DeleteBucketLifecycleConfigurationRequestRequestTypeDef",
    "DeleteBucketPolicyRequestRequestTypeDef",
    "DeleteBucketReplicationRequestRequestTypeDef",
    "DeleteBucketRequestRequestTypeDef",
    "DeleteBucketTaggingRequestRequestTypeDef",
    "DeleteJobTaggingRequestRequestTypeDef",
    "DeleteMarkerReplicationTypeDef",
    "DeletePublicAccessBlockRequestRequestTypeDef",
    "DeleteStorageLensConfigurationRequestRequestTypeDef",
    "DeleteStorageLensConfigurationTaggingRequestRequestTypeDef",
    "DescribeJobRequestRequestTypeDef",
    "DescribeMultiRegionAccessPointOperationRequestRequestTypeDef",
    "EncryptionConfigurationTypeDef",
    "EstablishedMultiRegionAccessPointPolicyTypeDef",
    "ExcludeTypeDef",
    "ExistingObjectReplicationTypeDef",
    "SSEKMSEncryptionTypeDef",
    "GetAccessPointConfigurationForObjectLambdaRequestRequestTypeDef",
    "GetAccessPointForObjectLambdaRequestRequestTypeDef",
    "GetAccessPointPolicyForObjectLambdaRequestRequestTypeDef",
    "GetAccessPointPolicyRequestRequestTypeDef",
    "GetAccessPointPolicyStatusForObjectLambdaRequestRequestTypeDef",
    "PolicyStatusTypeDef",
    "GetAccessPointPolicyStatusRequestRequestTypeDef",
    "GetAccessPointRequestRequestTypeDef",
    "GetBucketLifecycleConfigurationRequestRequestTypeDef",
    "GetBucketPolicyRequestRequestTypeDef",
    "GetBucketReplicationRequestRequestTypeDef",
    "GetBucketRequestRequestTypeDef",
    "GetBucketTaggingRequestRequestTypeDef",
    "GetBucketVersioningRequestRequestTypeDef",
    "GetJobTaggingRequestRequestTypeDef",
    "GetMultiRegionAccessPointPolicyRequestRequestTypeDef",
    "GetMultiRegionAccessPointPolicyStatusRequestRequestTypeDef",
    "GetMultiRegionAccessPointRequestRequestTypeDef",
    "GetMultiRegionAccessPointRoutesRequestRequestTypeDef",
    "MultiRegionAccessPointRouteTypeDef",
    "GetPublicAccessBlockRequestRequestTypeDef",
    "GetStorageLensConfigurationRequestRequestTypeDef",
    "GetStorageLensConfigurationTaggingRequestRequestTypeDef",
    "StorageLensTagTypeDef",
    "IncludeTypeDef",
    "JobFailureTypeDef",
    "TimestampTypeDef",
    "JobManifestLocationTypeDef",
    "JobManifestSpecTypeDef",
    "LambdaInvokeOperationTypeDef",
    "S3InitiateRestoreObjectOperationTypeDef",
    "JobTimersTypeDef",
    "LifecycleExpirationTypeDef",
    "NoncurrentVersionExpirationTypeDef",
    "NoncurrentVersionTransitionTypeDef",
    "TransitionTypeDef",
    "PaginatorConfigTypeDef",
    "ListAccessPointsForObjectLambdaRequestRequestTypeDef",
    "ListAccessPointsRequestRequestTypeDef",
    "ListJobsRequestRequestTypeDef",
    "ListMultiRegionAccessPointsRequestRequestTypeDef",
    "ListRegionalBucketsRequestRequestTypeDef",
    "RegionalBucketTypeDef",
    "ListStorageLensConfigurationEntryTypeDef",
    "ListStorageLensConfigurationsRequestRequestTypeDef",
    "ReplicationTimeValueTypeDef",
    "ProposedMultiRegionAccessPointPolicyTypeDef",
    "MultiRegionAccessPointRegionalResponseTypeDef",
    "RegionReportTypeDef",
    "SelectionCriteriaTypeDef",
    "PutAccessPointPolicyForObjectLambdaRequestRequestTypeDef",
    "PutAccessPointPolicyRequestRequestTypeDef",
    "PutBucketPolicyRequestRequestTypeDef",
    "VersioningConfigurationTypeDef",
    "ReplicaModificationsTypeDef",
    "S3ObjectOwnerTypeDef",
    "S3GranteeTypeDef",
    "S3ObjectLockLegalHoldTypeDef",
    "SSEKMSTypeDef",
    "SseKmsEncryptedObjectsTypeDef",
    "StorageLensAwsOrgTypeDef",
    "UpdateJobPriorityRequestRequestTypeDef",
    "UpdateJobStatusRequestRequestTypeDef",
    "AccessPointTypeDef",
    "DeleteMultiRegionAccessPointRequestRequestTypeDef",
    "PutMultiRegionAccessPointPolicyRequestRequestTypeDef",
    "ObjectLambdaContentTransformationTypeDef",
    "ObjectLambdaAccessPointTypeDef",
    "CreateAccessPointForObjectLambdaResultTypeDef",
    "CreateAccessPointResultTypeDef",
    "CreateBucketResultTypeDef",
    "CreateJobResultTypeDef",
    "CreateMultiRegionAccessPointResultTypeDef",
    "DeleteMultiRegionAccessPointResultTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetAccessPointPolicyForObjectLambdaResultTypeDef",
    "GetAccessPointPolicyResultTypeDef",
    "GetBucketPolicyResultTypeDef",
    "GetBucketResultTypeDef",
    "GetBucketVersioningResultTypeDef",
    "PutMultiRegionAccessPointPolicyResultTypeDef",
    "UpdateJobPriorityResultTypeDef",
    "UpdateJobStatusResultTypeDef",
    "CreateAccessPointRequestRequestTypeDef",
    "GetAccessPointForObjectLambdaResultTypeDef",
    "GetAccessPointResultTypeDef",
    "GetPublicAccessBlockOutputTypeDef",
    "PutPublicAccessBlockRequestRequestTypeDef",
    "CreateBucketRequestRequestTypeDef",
    "GetBucketTaggingResultTypeDef",
    "GetJobTaggingResultTypeDef",
    "LifecycleRuleAndOperatorTypeDef",
    "PutJobTaggingRequestRequestTypeDef",
    "ReplicationRuleAndOperatorTypeDef",
    "S3SetObjectTaggingOperationTypeDef",
    "TaggingTypeDef",
    "CreateMultiRegionAccessPointInputTypeDef",
    "GeneratedManifestEncryptionTypeDef",
    "GetAccessPointPolicyStatusForObjectLambdaResultTypeDef",
    "GetAccessPointPolicyStatusResultTypeDef",
    "GetMultiRegionAccessPointPolicyStatusResultTypeDef",
    "GetMultiRegionAccessPointRoutesResultTypeDef",
    "SubmitMultiRegionAccessPointRoutesRequestRequestTypeDef",
    "GetStorageLensConfigurationTaggingResultTypeDef",
    "PutStorageLensConfigurationTaggingRequestRequestTypeDef",
    "JobManifestGeneratorFilterTypeDef",
    "S3ObjectMetadataTypeDef",
    "S3RetentionTypeDef",
    "S3GeneratedManifestDescriptorTypeDef",
    "JobManifestTypeDef",
    "JobProgressSummaryTypeDef",
    "ListAccessPointsForObjectLambdaRequestListAccessPointsForObjectLambdaPaginateTypeDef",
    "ListRegionalBucketsResultTypeDef",
    "ListStorageLensConfigurationsResultTypeDef",
    "MetricsTypeDef",
    "ReplicationTimeTypeDef",
    "MultiRegionAccessPointPolicyDocumentTypeDef",
    "MultiRegionAccessPointsAsyncResponseTypeDef",
    "MultiRegionAccessPointReportTypeDef",
    "PrefixLevelStorageMetricsTypeDef",
    "PutBucketVersioningRequestRequestTypeDef",
    "S3GrantTypeDef",
    "S3SetObjectLegalHoldOperationTypeDef",
    "StorageLensDataExportEncryptionTypeDef",
    "SourceSelectionCriteriaTypeDef",
    "ListAccessPointsResultTypeDef",
    "ObjectLambdaTransformationConfigurationTypeDef",
    "ListAccessPointsForObjectLambdaResultTypeDef",
    "LifecycleRuleFilterTypeDef",
    "ReplicationRuleFilterTypeDef",
    "PutBucketTaggingRequestRequestTypeDef",
    "AsyncRequestParametersTypeDef",
    "CreateMultiRegionAccessPointRequestRequestTypeDef",
    "S3ManifestOutputLocationTypeDef",
    "S3SetObjectRetentionOperationTypeDef",
    "JobListDescriptorTypeDef",
    "DestinationTypeDef",
    "GetMultiRegionAccessPointPolicyResultTypeDef",
    "AsyncResponseDetailsTypeDef",
    "GetMultiRegionAccessPointResultTypeDef",
    "ListMultiRegionAccessPointsResultTypeDef",
    "PrefixLevelTypeDef",
    "S3AccessControlListTypeDef",
    "S3CopyObjectOperationTypeDef",
    "S3BucketDestinationTypeDef",
    "ObjectLambdaConfigurationTypeDef",
    "LifecycleRuleTypeDef",
    "S3JobManifestGeneratorTypeDef",
    "ListJobsResultTypeDef",
    "ReplicationRuleTypeDef",
    "AsyncOperationTypeDef",
    "BucketLevelTypeDef",
    "S3AccessControlPolicyTypeDef",
    "StorageLensDataExportTypeDef",
    "CreateAccessPointForObjectLambdaRequestRequestTypeDef",
    "GetAccessPointConfigurationForObjectLambdaResultTypeDef",
    "PutAccessPointConfigurationForObjectLambdaRequestRequestTypeDef",
    "GetBucketLifecycleConfigurationResultTypeDef",
    "LifecycleConfigurationTypeDef",
    "JobManifestGeneratorTypeDef",
    "ReplicationConfigurationTypeDef",
    "DescribeMultiRegionAccessPointOperationResultTypeDef",
    "AccountLevelTypeDef",
    "S3SetObjectAclOperationTypeDef",
    "PutBucketLifecycleConfigurationRequestRequestTypeDef",
    "GetBucketReplicationResultTypeDef",
    "PutBucketReplicationRequestRequestTypeDef",
    "StorageLensConfigurationTypeDef",
    "JobOperationTypeDef",
    "GetStorageLensConfigurationResultTypeDef",
    "PutStorageLensConfigurationRequestRequestTypeDef",
    "CreateJobRequestRequestTypeDef",
    "JobDescriptorTypeDef",
    "DescribeJobResultTypeDef",
)

AbortIncompleteMultipartUploadTypeDef = TypedDict(
    "AbortIncompleteMultipartUploadTypeDef",
    {
        "DaysAfterInitiation": NotRequired[int],
    },
)

AccessControlTranslationTypeDef = TypedDict(
    "AccessControlTranslationTypeDef",
    {
        "Owner": Literal["Destination"],
    },
)

VpcConfigurationTypeDef = TypedDict(
    "VpcConfigurationTypeDef",
    {
        "VpcId": str,
    },
)

ActivityMetricsTypeDef = TypedDict(
    "ActivityMetricsTypeDef",
    {
        "IsEnabled": NotRequired[bool],
    },
)

AdvancedCostOptimizationMetricsTypeDef = TypedDict(
    "AdvancedCostOptimizationMetricsTypeDef",
    {
        "IsEnabled": NotRequired[bool],
    },
)

AdvancedDataProtectionMetricsTypeDef = TypedDict(
    "AdvancedDataProtectionMetricsTypeDef",
    {
        "IsEnabled": NotRequired[bool],
    },
)

DetailedStatusCodesMetricsTypeDef = TypedDict(
    "DetailedStatusCodesMetricsTypeDef",
    {
        "IsEnabled": NotRequired[bool],
    },
)

AsyncErrorDetailsTypeDef = TypedDict(
    "AsyncErrorDetailsTypeDef",
    {
        "Code": NotRequired[str],
        "Message": NotRequired[str],
        "Resource": NotRequired[str],
        "RequestId": NotRequired[str],
    },
)

DeleteMultiRegionAccessPointInputTypeDef = TypedDict(
    "DeleteMultiRegionAccessPointInputTypeDef",
    {
        "Name": str,
    },
)

PutMultiRegionAccessPointPolicyInputTypeDef = TypedDict(
    "PutMultiRegionAccessPointPolicyInputTypeDef",
    {
        "Name": str,
        "Policy": str,
    },
)

AwsLambdaTransformationTypeDef = TypedDict(
    "AwsLambdaTransformationTypeDef",
    {
        "FunctionArn": str,
        "FunctionPayload": NotRequired[str],
    },
)

CloudWatchMetricsTypeDef = TypedDict(
    "CloudWatchMetricsTypeDef",
    {
        "IsEnabled": bool,
    },
)

ObjectLambdaAccessPointAliasTypeDef = TypedDict(
    "ObjectLambdaAccessPointAliasTypeDef",
    {
        "Value": NotRequired[str],
        "Status": NotRequired[ObjectLambdaAccessPointAliasStatusType],
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

PublicAccessBlockConfigurationTypeDef = TypedDict(
    "PublicAccessBlockConfigurationTypeDef",
    {
        "BlockPublicAcls": NotRequired[bool],
        "IgnorePublicAcls": NotRequired[bool],
        "BlockPublicPolicy": NotRequired[bool],
        "RestrictPublicBuckets": NotRequired[bool],
    },
)

CreateBucketConfigurationTypeDef = TypedDict(
    "CreateBucketConfigurationTypeDef",
    {
        "LocationConstraint": NotRequired[BucketLocationConstraintType],
    },
)

JobReportTypeDef = TypedDict(
    "JobReportTypeDef",
    {
        "Enabled": bool,
        "Bucket": NotRequired[str],
        "Format": NotRequired[Literal["Report_CSV_20180820"]],
        "Prefix": NotRequired[str],
        "ReportScope": NotRequired[JobReportScopeType],
    },
)

S3TagTypeDef = TypedDict(
    "S3TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

RegionTypeDef = TypedDict(
    "RegionTypeDef",
    {
        "Bucket": str,
        "BucketAccountId": NotRequired[str],
    },
)

DeleteAccessPointForObjectLambdaRequestRequestTypeDef = TypedDict(
    "DeleteAccessPointForObjectLambdaRequestRequestTypeDef",
    {
        "AccountId": str,
        "Name": str,
    },
)

DeleteAccessPointPolicyForObjectLambdaRequestRequestTypeDef = TypedDict(
    "DeleteAccessPointPolicyForObjectLambdaRequestRequestTypeDef",
    {
        "AccountId": str,
        "Name": str,
    },
)

DeleteAccessPointPolicyRequestRequestTypeDef = TypedDict(
    "DeleteAccessPointPolicyRequestRequestTypeDef",
    {
        "AccountId": str,
        "Name": str,
    },
)

DeleteAccessPointRequestRequestTypeDef = TypedDict(
    "DeleteAccessPointRequestRequestTypeDef",
    {
        "AccountId": str,
        "Name": str,
    },
)

DeleteBucketLifecycleConfigurationRequestRequestTypeDef = TypedDict(
    "DeleteBucketLifecycleConfigurationRequestRequestTypeDef",
    {
        "AccountId": str,
        "Bucket": str,
    },
)

DeleteBucketPolicyRequestRequestTypeDef = TypedDict(
    "DeleteBucketPolicyRequestRequestTypeDef",
    {
        "AccountId": str,
        "Bucket": str,
    },
)

DeleteBucketReplicationRequestRequestTypeDef = TypedDict(
    "DeleteBucketReplicationRequestRequestTypeDef",
    {
        "AccountId": str,
        "Bucket": str,
    },
)

DeleteBucketRequestRequestTypeDef = TypedDict(
    "DeleteBucketRequestRequestTypeDef",
    {
        "AccountId": str,
        "Bucket": str,
    },
)

DeleteBucketTaggingRequestRequestTypeDef = TypedDict(
    "DeleteBucketTaggingRequestRequestTypeDef",
    {
        "AccountId": str,
        "Bucket": str,
    },
)

DeleteJobTaggingRequestRequestTypeDef = TypedDict(
    "DeleteJobTaggingRequestRequestTypeDef",
    {
        "AccountId": str,
        "JobId": str,
    },
)

DeleteMarkerReplicationTypeDef = TypedDict(
    "DeleteMarkerReplicationTypeDef",
    {
        "Status": DeleteMarkerReplicationStatusType,
    },
)

DeletePublicAccessBlockRequestRequestTypeDef = TypedDict(
    "DeletePublicAccessBlockRequestRequestTypeDef",
    {
        "AccountId": str,
    },
)

DeleteStorageLensConfigurationRequestRequestTypeDef = TypedDict(
    "DeleteStorageLensConfigurationRequestRequestTypeDef",
    {
        "ConfigId": str,
        "AccountId": str,
    },
)

DeleteStorageLensConfigurationTaggingRequestRequestTypeDef = TypedDict(
    "DeleteStorageLensConfigurationTaggingRequestRequestTypeDef",
    {
        "ConfigId": str,
        "AccountId": str,
    },
)

DescribeJobRequestRequestTypeDef = TypedDict(
    "DescribeJobRequestRequestTypeDef",
    {
        "AccountId": str,
        "JobId": str,
    },
)

DescribeMultiRegionAccessPointOperationRequestRequestTypeDef = TypedDict(
    "DescribeMultiRegionAccessPointOperationRequestRequestTypeDef",
    {
        "AccountId": str,
        "RequestTokenARN": str,
    },
)

EncryptionConfigurationTypeDef = TypedDict(
    "EncryptionConfigurationTypeDef",
    {
        "ReplicaKmsKeyID": NotRequired[str],
    },
)

EstablishedMultiRegionAccessPointPolicyTypeDef = TypedDict(
    "EstablishedMultiRegionAccessPointPolicyTypeDef",
    {
        "Policy": NotRequired[str],
    },
)

ExcludeTypeDef = TypedDict(
    "ExcludeTypeDef",
    {
        "Buckets": NotRequired[List[str]],
        "Regions": NotRequired[List[str]],
    },
)

ExistingObjectReplicationTypeDef = TypedDict(
    "ExistingObjectReplicationTypeDef",
    {
        "Status": ExistingObjectReplicationStatusType,
    },
)

SSEKMSEncryptionTypeDef = TypedDict(
    "SSEKMSEncryptionTypeDef",
    {
        "KeyId": str,
    },
)

GetAccessPointConfigurationForObjectLambdaRequestRequestTypeDef = TypedDict(
    "GetAccessPointConfigurationForObjectLambdaRequestRequestTypeDef",
    {
        "AccountId": str,
        "Name": str,
    },
)

GetAccessPointForObjectLambdaRequestRequestTypeDef = TypedDict(
    "GetAccessPointForObjectLambdaRequestRequestTypeDef",
    {
        "AccountId": str,
        "Name": str,
    },
)

GetAccessPointPolicyForObjectLambdaRequestRequestTypeDef = TypedDict(
    "GetAccessPointPolicyForObjectLambdaRequestRequestTypeDef",
    {
        "AccountId": str,
        "Name": str,
    },
)

GetAccessPointPolicyRequestRequestTypeDef = TypedDict(
    "GetAccessPointPolicyRequestRequestTypeDef",
    {
        "AccountId": str,
        "Name": str,
    },
)

GetAccessPointPolicyStatusForObjectLambdaRequestRequestTypeDef = TypedDict(
    "GetAccessPointPolicyStatusForObjectLambdaRequestRequestTypeDef",
    {
        "AccountId": str,
        "Name": str,
    },
)

PolicyStatusTypeDef = TypedDict(
    "PolicyStatusTypeDef",
    {
        "IsPublic": NotRequired[bool],
    },
)

GetAccessPointPolicyStatusRequestRequestTypeDef = TypedDict(
    "GetAccessPointPolicyStatusRequestRequestTypeDef",
    {
        "AccountId": str,
        "Name": str,
    },
)

GetAccessPointRequestRequestTypeDef = TypedDict(
    "GetAccessPointRequestRequestTypeDef",
    {
        "AccountId": str,
        "Name": str,
    },
)

GetBucketLifecycleConfigurationRequestRequestTypeDef = TypedDict(
    "GetBucketLifecycleConfigurationRequestRequestTypeDef",
    {
        "AccountId": str,
        "Bucket": str,
    },
)

GetBucketPolicyRequestRequestTypeDef = TypedDict(
    "GetBucketPolicyRequestRequestTypeDef",
    {
        "AccountId": str,
        "Bucket": str,
    },
)

GetBucketReplicationRequestRequestTypeDef = TypedDict(
    "GetBucketReplicationRequestRequestTypeDef",
    {
        "AccountId": str,
        "Bucket": str,
    },
)

GetBucketRequestRequestTypeDef = TypedDict(
    "GetBucketRequestRequestTypeDef",
    {
        "AccountId": str,
        "Bucket": str,
    },
)

GetBucketTaggingRequestRequestTypeDef = TypedDict(
    "GetBucketTaggingRequestRequestTypeDef",
    {
        "AccountId": str,
        "Bucket": str,
    },
)

GetBucketVersioningRequestRequestTypeDef = TypedDict(
    "GetBucketVersioningRequestRequestTypeDef",
    {
        "AccountId": str,
        "Bucket": str,
    },
)

GetJobTaggingRequestRequestTypeDef = TypedDict(
    "GetJobTaggingRequestRequestTypeDef",
    {
        "AccountId": str,
        "JobId": str,
    },
)

GetMultiRegionAccessPointPolicyRequestRequestTypeDef = TypedDict(
    "GetMultiRegionAccessPointPolicyRequestRequestTypeDef",
    {
        "AccountId": str,
        "Name": str,
    },
)

GetMultiRegionAccessPointPolicyStatusRequestRequestTypeDef = TypedDict(
    "GetMultiRegionAccessPointPolicyStatusRequestRequestTypeDef",
    {
        "AccountId": str,
        "Name": str,
    },
)

GetMultiRegionAccessPointRequestRequestTypeDef = TypedDict(
    "GetMultiRegionAccessPointRequestRequestTypeDef",
    {
        "AccountId": str,
        "Name": str,
    },
)

GetMultiRegionAccessPointRoutesRequestRequestTypeDef = TypedDict(
    "GetMultiRegionAccessPointRoutesRequestRequestTypeDef",
    {
        "AccountId": str,
        "Mrap": str,
    },
)

MultiRegionAccessPointRouteTypeDef = TypedDict(
    "MultiRegionAccessPointRouteTypeDef",
    {
        "TrafficDialPercentage": int,
        "Bucket": NotRequired[str],
        "Region": NotRequired[str],
    },
)

GetPublicAccessBlockRequestRequestTypeDef = TypedDict(
    "GetPublicAccessBlockRequestRequestTypeDef",
    {
        "AccountId": str,
    },
)

GetStorageLensConfigurationRequestRequestTypeDef = TypedDict(
    "GetStorageLensConfigurationRequestRequestTypeDef",
    {
        "ConfigId": str,
        "AccountId": str,
    },
)

GetStorageLensConfigurationTaggingRequestRequestTypeDef = TypedDict(
    "GetStorageLensConfigurationTaggingRequestRequestTypeDef",
    {
        "ConfigId": str,
        "AccountId": str,
    },
)

StorageLensTagTypeDef = TypedDict(
    "StorageLensTagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

IncludeTypeDef = TypedDict(
    "IncludeTypeDef",
    {
        "Buckets": NotRequired[List[str]],
        "Regions": NotRequired[List[str]],
    },
)

JobFailureTypeDef = TypedDict(
    "JobFailureTypeDef",
    {
        "FailureCode": NotRequired[str],
        "FailureReason": NotRequired[str],
    },
)

TimestampTypeDef = Union[datetime, str]
JobManifestLocationTypeDef = TypedDict(
    "JobManifestLocationTypeDef",
    {
        "ObjectArn": str,
        "ETag": str,
        "ObjectVersionId": NotRequired[str],
    },
)

JobManifestSpecTypeDef = TypedDict(
    "JobManifestSpecTypeDef",
    {
        "Format": JobManifestFormatType,
        "Fields": NotRequired[Sequence[JobManifestFieldNameType]],
    },
)

LambdaInvokeOperationTypeDef = TypedDict(
    "LambdaInvokeOperationTypeDef",
    {
        "FunctionArn": NotRequired[str],
    },
)

S3InitiateRestoreObjectOperationTypeDef = TypedDict(
    "S3InitiateRestoreObjectOperationTypeDef",
    {
        "ExpirationInDays": NotRequired[int],
        "GlacierJobTier": NotRequired[S3GlacierJobTierType],
    },
)

JobTimersTypeDef = TypedDict(
    "JobTimersTypeDef",
    {
        "ElapsedTimeInActiveSeconds": NotRequired[int],
    },
)

LifecycleExpirationTypeDef = TypedDict(
    "LifecycleExpirationTypeDef",
    {
        "Date": NotRequired[datetime],
        "Days": NotRequired[int],
        "ExpiredObjectDeleteMarker": NotRequired[bool],
    },
)

NoncurrentVersionExpirationTypeDef = TypedDict(
    "NoncurrentVersionExpirationTypeDef",
    {
        "NoncurrentDays": NotRequired[int],
        "NewerNoncurrentVersions": NotRequired[int],
    },
)

NoncurrentVersionTransitionTypeDef = TypedDict(
    "NoncurrentVersionTransitionTypeDef",
    {
        "NoncurrentDays": NotRequired[int],
        "StorageClass": NotRequired[TransitionStorageClassType],
    },
)

TransitionTypeDef = TypedDict(
    "TransitionTypeDef",
    {
        "Date": NotRequired[datetime],
        "Days": NotRequired[int],
        "StorageClass": NotRequired[TransitionStorageClassType],
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

ListAccessPointsForObjectLambdaRequestRequestTypeDef = TypedDict(
    "ListAccessPointsForObjectLambdaRequestRequestTypeDef",
    {
        "AccountId": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ListAccessPointsRequestRequestTypeDef = TypedDict(
    "ListAccessPointsRequestRequestTypeDef",
    {
        "AccountId": str,
        "Bucket": NotRequired[str],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ListJobsRequestRequestTypeDef = TypedDict(
    "ListJobsRequestRequestTypeDef",
    {
        "AccountId": str,
        "JobStatuses": NotRequired[Sequence[JobStatusType]],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ListMultiRegionAccessPointsRequestRequestTypeDef = TypedDict(
    "ListMultiRegionAccessPointsRequestRequestTypeDef",
    {
        "AccountId": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ListRegionalBucketsRequestRequestTypeDef = TypedDict(
    "ListRegionalBucketsRequestRequestTypeDef",
    {
        "AccountId": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
        "OutpostId": NotRequired[str],
    },
)

RegionalBucketTypeDef = TypedDict(
    "RegionalBucketTypeDef",
    {
        "Bucket": str,
        "PublicAccessBlockEnabled": bool,
        "CreationDate": datetime,
        "BucketArn": NotRequired[str],
        "OutpostId": NotRequired[str],
    },
)

ListStorageLensConfigurationEntryTypeDef = TypedDict(
    "ListStorageLensConfigurationEntryTypeDef",
    {
        "Id": str,
        "StorageLensArn": str,
        "HomeRegion": str,
        "IsEnabled": NotRequired[bool],
    },
)

ListStorageLensConfigurationsRequestRequestTypeDef = TypedDict(
    "ListStorageLensConfigurationsRequestRequestTypeDef",
    {
        "AccountId": str,
        "NextToken": NotRequired[str],
    },
)

ReplicationTimeValueTypeDef = TypedDict(
    "ReplicationTimeValueTypeDef",
    {
        "Minutes": NotRequired[int],
    },
)

ProposedMultiRegionAccessPointPolicyTypeDef = TypedDict(
    "ProposedMultiRegionAccessPointPolicyTypeDef",
    {
        "Policy": NotRequired[str],
    },
)

MultiRegionAccessPointRegionalResponseTypeDef = TypedDict(
    "MultiRegionAccessPointRegionalResponseTypeDef",
    {
        "Name": NotRequired[str],
        "RequestStatus": NotRequired[str],
    },
)

RegionReportTypeDef = TypedDict(
    "RegionReportTypeDef",
    {
        "Bucket": NotRequired[str],
        "Region": NotRequired[str],
        "BucketAccountId": NotRequired[str],
    },
)

SelectionCriteriaTypeDef = TypedDict(
    "SelectionCriteriaTypeDef",
    {
        "Delimiter": NotRequired[str],
        "MaxDepth": NotRequired[int],
        "MinStorageBytesPercentage": NotRequired[float],
    },
)

PutAccessPointPolicyForObjectLambdaRequestRequestTypeDef = TypedDict(
    "PutAccessPointPolicyForObjectLambdaRequestRequestTypeDef",
    {
        "AccountId": str,
        "Name": str,
        "Policy": str,
    },
)

PutAccessPointPolicyRequestRequestTypeDef = TypedDict(
    "PutAccessPointPolicyRequestRequestTypeDef",
    {
        "AccountId": str,
        "Name": str,
        "Policy": str,
    },
)

PutBucketPolicyRequestRequestTypeDef = TypedDict(
    "PutBucketPolicyRequestRequestTypeDef",
    {
        "AccountId": str,
        "Bucket": str,
        "Policy": str,
        "ConfirmRemoveSelfBucketAccess": NotRequired[bool],
    },
)

VersioningConfigurationTypeDef = TypedDict(
    "VersioningConfigurationTypeDef",
    {
        "MFADelete": NotRequired[MFADeleteType],
        "Status": NotRequired[BucketVersioningStatusType],
    },
)

ReplicaModificationsTypeDef = TypedDict(
    "ReplicaModificationsTypeDef",
    {
        "Status": ReplicaModificationsStatusType,
    },
)

S3ObjectOwnerTypeDef = TypedDict(
    "S3ObjectOwnerTypeDef",
    {
        "ID": NotRequired[str],
        "DisplayName": NotRequired[str],
    },
)

S3GranteeTypeDef = TypedDict(
    "S3GranteeTypeDef",
    {
        "TypeIdentifier": NotRequired[S3GranteeTypeIdentifierType],
        "Identifier": NotRequired[str],
        "DisplayName": NotRequired[str],
    },
)

S3ObjectLockLegalHoldTypeDef = TypedDict(
    "S3ObjectLockLegalHoldTypeDef",
    {
        "Status": S3ObjectLockLegalHoldStatusType,
    },
)

SSEKMSTypeDef = TypedDict(
    "SSEKMSTypeDef",
    {
        "KeyId": str,
    },
)

SseKmsEncryptedObjectsTypeDef = TypedDict(
    "SseKmsEncryptedObjectsTypeDef",
    {
        "Status": SseKmsEncryptedObjectsStatusType,
    },
)

StorageLensAwsOrgTypeDef = TypedDict(
    "StorageLensAwsOrgTypeDef",
    {
        "Arn": str,
    },
)

UpdateJobPriorityRequestRequestTypeDef = TypedDict(
    "UpdateJobPriorityRequestRequestTypeDef",
    {
        "AccountId": str,
        "JobId": str,
        "Priority": int,
    },
)

UpdateJobStatusRequestRequestTypeDef = TypedDict(
    "UpdateJobStatusRequestRequestTypeDef",
    {
        "AccountId": str,
        "JobId": str,
        "RequestedJobStatus": RequestedJobStatusType,
        "StatusUpdateReason": NotRequired[str],
    },
)

AccessPointTypeDef = TypedDict(
    "AccessPointTypeDef",
    {
        "Name": str,
        "NetworkOrigin": NetworkOriginType,
        "Bucket": str,
        "VpcConfiguration": NotRequired[VpcConfigurationTypeDef],
        "AccessPointArn": NotRequired[str],
        "Alias": NotRequired[str],
        "BucketAccountId": NotRequired[str],
    },
)

DeleteMultiRegionAccessPointRequestRequestTypeDef = TypedDict(
    "DeleteMultiRegionAccessPointRequestRequestTypeDef",
    {
        "AccountId": str,
        "ClientToken": str,
        "Details": DeleteMultiRegionAccessPointInputTypeDef,
    },
)

PutMultiRegionAccessPointPolicyRequestRequestTypeDef = TypedDict(
    "PutMultiRegionAccessPointPolicyRequestRequestTypeDef",
    {
        "AccountId": str,
        "ClientToken": str,
        "Details": PutMultiRegionAccessPointPolicyInputTypeDef,
    },
)

ObjectLambdaContentTransformationTypeDef = TypedDict(
    "ObjectLambdaContentTransformationTypeDef",
    {
        "AwsLambda": NotRequired[AwsLambdaTransformationTypeDef],
    },
)

ObjectLambdaAccessPointTypeDef = TypedDict(
    "ObjectLambdaAccessPointTypeDef",
    {
        "Name": str,
        "ObjectLambdaAccessPointArn": NotRequired[str],
        "Alias": NotRequired[ObjectLambdaAccessPointAliasTypeDef],
    },
)

CreateAccessPointForObjectLambdaResultTypeDef = TypedDict(
    "CreateAccessPointForObjectLambdaResultTypeDef",
    {
        "ObjectLambdaAccessPointArn": str,
        "Alias": ObjectLambdaAccessPointAliasTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAccessPointResultTypeDef = TypedDict(
    "CreateAccessPointResultTypeDef",
    {
        "AccessPointArn": str,
        "Alias": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateBucketResultTypeDef = TypedDict(
    "CreateBucketResultTypeDef",
    {
        "Location": str,
        "BucketArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateJobResultTypeDef = TypedDict(
    "CreateJobResultTypeDef",
    {
        "JobId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateMultiRegionAccessPointResultTypeDef = TypedDict(
    "CreateMultiRegionAccessPointResultTypeDef",
    {
        "RequestTokenARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteMultiRegionAccessPointResultTypeDef = TypedDict(
    "DeleteMultiRegionAccessPointResultTypeDef",
    {
        "RequestTokenARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAccessPointPolicyForObjectLambdaResultTypeDef = TypedDict(
    "GetAccessPointPolicyForObjectLambdaResultTypeDef",
    {
        "Policy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAccessPointPolicyResultTypeDef = TypedDict(
    "GetAccessPointPolicyResultTypeDef",
    {
        "Policy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetBucketPolicyResultTypeDef = TypedDict(
    "GetBucketPolicyResultTypeDef",
    {
        "Policy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetBucketResultTypeDef = TypedDict(
    "GetBucketResultTypeDef",
    {
        "Bucket": str,
        "PublicAccessBlockEnabled": bool,
        "CreationDate": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetBucketVersioningResultTypeDef = TypedDict(
    "GetBucketVersioningResultTypeDef",
    {
        "Status": BucketVersioningStatusType,
        "MFADelete": MFADeleteStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutMultiRegionAccessPointPolicyResultTypeDef = TypedDict(
    "PutMultiRegionAccessPointPolicyResultTypeDef",
    {
        "RequestTokenARN": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateJobPriorityResultTypeDef = TypedDict(
    "UpdateJobPriorityResultTypeDef",
    {
        "JobId": str,
        "Priority": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateJobStatusResultTypeDef = TypedDict(
    "UpdateJobStatusResultTypeDef",
    {
        "JobId": str,
        "Status": JobStatusType,
        "StatusUpdateReason": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAccessPointRequestRequestTypeDef = TypedDict(
    "CreateAccessPointRequestRequestTypeDef",
    {
        "AccountId": str,
        "Name": str,
        "Bucket": str,
        "VpcConfiguration": NotRequired[VpcConfigurationTypeDef],
        "PublicAccessBlockConfiguration": NotRequired[PublicAccessBlockConfigurationTypeDef],
        "BucketAccountId": NotRequired[str],
    },
)

GetAccessPointForObjectLambdaResultTypeDef = TypedDict(
    "GetAccessPointForObjectLambdaResultTypeDef",
    {
        "Name": str,
        "PublicAccessBlockConfiguration": PublicAccessBlockConfigurationTypeDef,
        "CreationDate": datetime,
        "Alias": ObjectLambdaAccessPointAliasTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAccessPointResultTypeDef = TypedDict(
    "GetAccessPointResultTypeDef",
    {
        "Name": str,
        "Bucket": str,
        "NetworkOrigin": NetworkOriginType,
        "VpcConfiguration": VpcConfigurationTypeDef,
        "PublicAccessBlockConfiguration": PublicAccessBlockConfigurationTypeDef,
        "CreationDate": datetime,
        "Alias": str,
        "AccessPointArn": str,
        "Endpoints": Dict[str, str],
        "BucketAccountId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetPublicAccessBlockOutputTypeDef = TypedDict(
    "GetPublicAccessBlockOutputTypeDef",
    {
        "PublicAccessBlockConfiguration": PublicAccessBlockConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutPublicAccessBlockRequestRequestTypeDef = TypedDict(
    "PutPublicAccessBlockRequestRequestTypeDef",
    {
        "PublicAccessBlockConfiguration": PublicAccessBlockConfigurationTypeDef,
        "AccountId": str,
    },
)

CreateBucketRequestRequestTypeDef = TypedDict(
    "CreateBucketRequestRequestTypeDef",
    {
        "Bucket": str,
        "ACL": NotRequired[BucketCannedACLType],
        "CreateBucketConfiguration": NotRequired[CreateBucketConfigurationTypeDef],
        "GrantFullControl": NotRequired[str],
        "GrantRead": NotRequired[str],
        "GrantReadACP": NotRequired[str],
        "GrantWrite": NotRequired[str],
        "GrantWriteACP": NotRequired[str],
        "ObjectLockEnabledForBucket": NotRequired[bool],
        "OutpostId": NotRequired[str],
    },
)

GetBucketTaggingResultTypeDef = TypedDict(
    "GetBucketTaggingResultTypeDef",
    {
        "TagSet": List[S3TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetJobTaggingResultTypeDef = TypedDict(
    "GetJobTaggingResultTypeDef",
    {
        "Tags": List[S3TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LifecycleRuleAndOperatorTypeDef = TypedDict(
    "LifecycleRuleAndOperatorTypeDef",
    {
        "Prefix": NotRequired[str],
        "Tags": NotRequired[List[S3TagTypeDef]],
        "ObjectSizeGreaterThan": NotRequired[int],
        "ObjectSizeLessThan": NotRequired[int],
    },
)

PutJobTaggingRequestRequestTypeDef = TypedDict(
    "PutJobTaggingRequestRequestTypeDef",
    {
        "AccountId": str,
        "JobId": str,
        "Tags": Sequence[S3TagTypeDef],
    },
)

ReplicationRuleAndOperatorTypeDef = TypedDict(
    "ReplicationRuleAndOperatorTypeDef",
    {
        "Prefix": NotRequired[str],
        "Tags": NotRequired[List[S3TagTypeDef]],
    },
)

S3SetObjectTaggingOperationTypeDef = TypedDict(
    "S3SetObjectTaggingOperationTypeDef",
    {
        "TagSet": NotRequired[Sequence[S3TagTypeDef]],
    },
)

TaggingTypeDef = TypedDict(
    "TaggingTypeDef",
    {
        "TagSet": Sequence[S3TagTypeDef],
    },
)

CreateMultiRegionAccessPointInputTypeDef = TypedDict(
    "CreateMultiRegionAccessPointInputTypeDef",
    {
        "Name": str,
        "Regions": Sequence[RegionTypeDef],
        "PublicAccessBlock": NotRequired[PublicAccessBlockConfigurationTypeDef],
    },
)

GeneratedManifestEncryptionTypeDef = TypedDict(
    "GeneratedManifestEncryptionTypeDef",
    {
        "SSES3": NotRequired[Mapping[str, Any]],
        "SSEKMS": NotRequired[SSEKMSEncryptionTypeDef],
    },
)

GetAccessPointPolicyStatusForObjectLambdaResultTypeDef = TypedDict(
    "GetAccessPointPolicyStatusForObjectLambdaResultTypeDef",
    {
        "PolicyStatus": PolicyStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAccessPointPolicyStatusResultTypeDef = TypedDict(
    "GetAccessPointPolicyStatusResultTypeDef",
    {
        "PolicyStatus": PolicyStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetMultiRegionAccessPointPolicyStatusResultTypeDef = TypedDict(
    "GetMultiRegionAccessPointPolicyStatusResultTypeDef",
    {
        "Established": PolicyStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetMultiRegionAccessPointRoutesResultTypeDef = TypedDict(
    "GetMultiRegionAccessPointRoutesResultTypeDef",
    {
        "Mrap": str,
        "Routes": List[MultiRegionAccessPointRouteTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

SubmitMultiRegionAccessPointRoutesRequestRequestTypeDef = TypedDict(
    "SubmitMultiRegionAccessPointRoutesRequestRequestTypeDef",
    {
        "AccountId": str,
        "Mrap": str,
        "RouteUpdates": Sequence[MultiRegionAccessPointRouteTypeDef],
    },
)

GetStorageLensConfigurationTaggingResultTypeDef = TypedDict(
    "GetStorageLensConfigurationTaggingResultTypeDef",
    {
        "Tags": List[StorageLensTagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutStorageLensConfigurationTaggingRequestRequestTypeDef = TypedDict(
    "PutStorageLensConfigurationTaggingRequestRequestTypeDef",
    {
        "ConfigId": str,
        "AccountId": str,
        "Tags": Sequence[StorageLensTagTypeDef],
    },
)

JobManifestGeneratorFilterTypeDef = TypedDict(
    "JobManifestGeneratorFilterTypeDef",
    {
        "EligibleForReplication": NotRequired[bool],
        "CreatedAfter": NotRequired[TimestampTypeDef],
        "CreatedBefore": NotRequired[TimestampTypeDef],
        "ObjectReplicationStatuses": NotRequired[Sequence[ReplicationStatusType]],
    },
)

S3ObjectMetadataTypeDef = TypedDict(
    "S3ObjectMetadataTypeDef",
    {
        "CacheControl": NotRequired[str],
        "ContentDisposition": NotRequired[str],
        "ContentEncoding": NotRequired[str],
        "ContentLanguage": NotRequired[str],
        "UserMetadata": NotRequired[Mapping[str, str]],
        "ContentLength": NotRequired[int],
        "ContentMD5": NotRequired[str],
        "ContentType": NotRequired[str],
        "HttpExpiresDate": NotRequired[TimestampTypeDef],
        "RequesterCharged": NotRequired[bool],
        "SSEAlgorithm": NotRequired[S3SSEAlgorithmType],
    },
)

S3RetentionTypeDef = TypedDict(
    "S3RetentionTypeDef",
    {
        "RetainUntilDate": NotRequired[TimestampTypeDef],
        "Mode": NotRequired[S3ObjectLockRetentionModeType],
    },
)

S3GeneratedManifestDescriptorTypeDef = TypedDict(
    "S3GeneratedManifestDescriptorTypeDef",
    {
        "Format": NotRequired[Literal["S3InventoryReport_CSV_20211130"]],
        "Location": NotRequired[JobManifestLocationTypeDef],
    },
)

JobManifestTypeDef = TypedDict(
    "JobManifestTypeDef",
    {
        "Spec": JobManifestSpecTypeDef,
        "Location": JobManifestLocationTypeDef,
    },
)

JobProgressSummaryTypeDef = TypedDict(
    "JobProgressSummaryTypeDef",
    {
        "TotalNumberOfTasks": NotRequired[int],
        "NumberOfTasksSucceeded": NotRequired[int],
        "NumberOfTasksFailed": NotRequired[int],
        "Timers": NotRequired[JobTimersTypeDef],
    },
)

ListAccessPointsForObjectLambdaRequestListAccessPointsForObjectLambdaPaginateTypeDef = TypedDict(
    "ListAccessPointsForObjectLambdaRequestListAccessPointsForObjectLambdaPaginateTypeDef",
    {
        "AccountId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListRegionalBucketsResultTypeDef = TypedDict(
    "ListRegionalBucketsResultTypeDef",
    {
        "RegionalBucketList": List[RegionalBucketTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListStorageLensConfigurationsResultTypeDef = TypedDict(
    "ListStorageLensConfigurationsResultTypeDef",
    {
        "NextToken": str,
        "StorageLensConfigurationList": List[ListStorageLensConfigurationEntryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

MetricsTypeDef = TypedDict(
    "MetricsTypeDef",
    {
        "Status": MetricsStatusType,
        "EventThreshold": NotRequired[ReplicationTimeValueTypeDef],
    },
)

ReplicationTimeTypeDef = TypedDict(
    "ReplicationTimeTypeDef",
    {
        "Status": ReplicationTimeStatusType,
        "Time": ReplicationTimeValueTypeDef,
    },
)

MultiRegionAccessPointPolicyDocumentTypeDef = TypedDict(
    "MultiRegionAccessPointPolicyDocumentTypeDef",
    {
        "Established": NotRequired[EstablishedMultiRegionAccessPointPolicyTypeDef],
        "Proposed": NotRequired[ProposedMultiRegionAccessPointPolicyTypeDef],
    },
)

MultiRegionAccessPointsAsyncResponseTypeDef = TypedDict(
    "MultiRegionAccessPointsAsyncResponseTypeDef",
    {
        "Regions": NotRequired[List[MultiRegionAccessPointRegionalResponseTypeDef]],
    },
)

MultiRegionAccessPointReportTypeDef = TypedDict(
    "MultiRegionAccessPointReportTypeDef",
    {
        "Name": NotRequired[str],
        "Alias": NotRequired[str],
        "CreatedAt": NotRequired[datetime],
        "PublicAccessBlock": NotRequired[PublicAccessBlockConfigurationTypeDef],
        "Status": NotRequired[MultiRegionAccessPointStatusType],
        "Regions": NotRequired[List[RegionReportTypeDef]],
    },
)

PrefixLevelStorageMetricsTypeDef = TypedDict(
    "PrefixLevelStorageMetricsTypeDef",
    {
        "IsEnabled": NotRequired[bool],
        "SelectionCriteria": NotRequired[SelectionCriteriaTypeDef],
    },
)

PutBucketVersioningRequestRequestTypeDef = TypedDict(
    "PutBucketVersioningRequestRequestTypeDef",
    {
        "AccountId": str,
        "Bucket": str,
        "VersioningConfiguration": VersioningConfigurationTypeDef,
        "MFA": NotRequired[str],
    },
)

S3GrantTypeDef = TypedDict(
    "S3GrantTypeDef",
    {
        "Grantee": NotRequired[S3GranteeTypeDef],
        "Permission": NotRequired[S3PermissionType],
    },
)

S3SetObjectLegalHoldOperationTypeDef = TypedDict(
    "S3SetObjectLegalHoldOperationTypeDef",
    {
        "LegalHold": S3ObjectLockLegalHoldTypeDef,
    },
)

StorageLensDataExportEncryptionTypeDef = TypedDict(
    "StorageLensDataExportEncryptionTypeDef",
    {
        "SSES3": NotRequired[Dict[str, Any]],
        "SSEKMS": NotRequired[SSEKMSTypeDef],
    },
)

SourceSelectionCriteriaTypeDef = TypedDict(
    "SourceSelectionCriteriaTypeDef",
    {
        "SseKmsEncryptedObjects": NotRequired[SseKmsEncryptedObjectsTypeDef],
        "ReplicaModifications": NotRequired[ReplicaModificationsTypeDef],
    },
)

ListAccessPointsResultTypeDef = TypedDict(
    "ListAccessPointsResultTypeDef",
    {
        "AccessPointList": List[AccessPointTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ObjectLambdaTransformationConfigurationTypeDef = TypedDict(
    "ObjectLambdaTransformationConfigurationTypeDef",
    {
        "Actions": Sequence[ObjectLambdaTransformationConfigurationActionType],
        "ContentTransformation": ObjectLambdaContentTransformationTypeDef,
    },
)

ListAccessPointsForObjectLambdaResultTypeDef = TypedDict(
    "ListAccessPointsForObjectLambdaResultTypeDef",
    {
        "ObjectLambdaAccessPointList": List[ObjectLambdaAccessPointTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LifecycleRuleFilterTypeDef = TypedDict(
    "LifecycleRuleFilterTypeDef",
    {
        "Prefix": NotRequired[str],
        "Tag": NotRequired[S3TagTypeDef],
        "And": NotRequired[LifecycleRuleAndOperatorTypeDef],
        "ObjectSizeGreaterThan": NotRequired[int],
        "ObjectSizeLessThan": NotRequired[int],
    },
)

ReplicationRuleFilterTypeDef = TypedDict(
    "ReplicationRuleFilterTypeDef",
    {
        "Prefix": NotRequired[str],
        "Tag": NotRequired[S3TagTypeDef],
        "And": NotRequired[ReplicationRuleAndOperatorTypeDef],
    },
)

PutBucketTaggingRequestRequestTypeDef = TypedDict(
    "PutBucketTaggingRequestRequestTypeDef",
    {
        "AccountId": str,
        "Bucket": str,
        "Tagging": TaggingTypeDef,
    },
)

AsyncRequestParametersTypeDef = TypedDict(
    "AsyncRequestParametersTypeDef",
    {
        "CreateMultiRegionAccessPointRequest": NotRequired[
            CreateMultiRegionAccessPointInputTypeDef
        ],
        "DeleteMultiRegionAccessPointRequest": NotRequired[
            DeleteMultiRegionAccessPointInputTypeDef
        ],
        "PutMultiRegionAccessPointPolicyRequest": NotRequired[
            PutMultiRegionAccessPointPolicyInputTypeDef
        ],
    },
)

CreateMultiRegionAccessPointRequestRequestTypeDef = TypedDict(
    "CreateMultiRegionAccessPointRequestRequestTypeDef",
    {
        "AccountId": str,
        "ClientToken": str,
        "Details": CreateMultiRegionAccessPointInputTypeDef,
    },
)

S3ManifestOutputLocationTypeDef = TypedDict(
    "S3ManifestOutputLocationTypeDef",
    {
        "Bucket": str,
        "ManifestFormat": Literal["S3InventoryReport_CSV_20211130"],
        "ExpectedManifestBucketOwner": NotRequired[str],
        "ManifestPrefix": NotRequired[str],
        "ManifestEncryption": NotRequired[GeneratedManifestEncryptionTypeDef],
    },
)

S3SetObjectRetentionOperationTypeDef = TypedDict(
    "S3SetObjectRetentionOperationTypeDef",
    {
        "Retention": S3RetentionTypeDef,
        "BypassGovernanceRetention": NotRequired[bool],
    },
)

JobListDescriptorTypeDef = TypedDict(
    "JobListDescriptorTypeDef",
    {
        "JobId": NotRequired[str],
        "Description": NotRequired[str],
        "Operation": NotRequired[OperationNameType],
        "Priority": NotRequired[int],
        "Status": NotRequired[JobStatusType],
        "CreationTime": NotRequired[datetime],
        "TerminationDate": NotRequired[datetime],
        "ProgressSummary": NotRequired[JobProgressSummaryTypeDef],
    },
)

DestinationTypeDef = TypedDict(
    "DestinationTypeDef",
    {
        "Bucket": str,
        "Account": NotRequired[str],
        "ReplicationTime": NotRequired[ReplicationTimeTypeDef],
        "AccessControlTranslation": NotRequired[AccessControlTranslationTypeDef],
        "EncryptionConfiguration": NotRequired[EncryptionConfigurationTypeDef],
        "Metrics": NotRequired[MetricsTypeDef],
        "StorageClass": NotRequired[ReplicationStorageClassType],
    },
)

GetMultiRegionAccessPointPolicyResultTypeDef = TypedDict(
    "GetMultiRegionAccessPointPolicyResultTypeDef",
    {
        "Policy": MultiRegionAccessPointPolicyDocumentTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AsyncResponseDetailsTypeDef = TypedDict(
    "AsyncResponseDetailsTypeDef",
    {
        "MultiRegionAccessPointDetails": NotRequired[MultiRegionAccessPointsAsyncResponseTypeDef],
        "ErrorDetails": NotRequired[AsyncErrorDetailsTypeDef],
    },
)

GetMultiRegionAccessPointResultTypeDef = TypedDict(
    "GetMultiRegionAccessPointResultTypeDef",
    {
        "AccessPoint": MultiRegionAccessPointReportTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListMultiRegionAccessPointsResultTypeDef = TypedDict(
    "ListMultiRegionAccessPointsResultTypeDef",
    {
        "AccessPoints": List[MultiRegionAccessPointReportTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PrefixLevelTypeDef = TypedDict(
    "PrefixLevelTypeDef",
    {
        "StorageMetrics": PrefixLevelStorageMetricsTypeDef,
    },
)

S3AccessControlListTypeDef = TypedDict(
    "S3AccessControlListTypeDef",
    {
        "Owner": S3ObjectOwnerTypeDef,
        "Grants": NotRequired[Sequence[S3GrantTypeDef]],
    },
)

S3CopyObjectOperationTypeDef = TypedDict(
    "S3CopyObjectOperationTypeDef",
    {
        "TargetResource": NotRequired[str],
        "CannedAccessControlList": NotRequired[S3CannedAccessControlListType],
        "AccessControlGrants": NotRequired[Sequence[S3GrantTypeDef]],
        "MetadataDirective": NotRequired[S3MetadataDirectiveType],
        "ModifiedSinceConstraint": NotRequired[TimestampTypeDef],
        "NewObjectMetadata": NotRequired[S3ObjectMetadataTypeDef],
        "NewObjectTagging": NotRequired[Sequence[S3TagTypeDef]],
        "RedirectLocation": NotRequired[str],
        "RequesterPays": NotRequired[bool],
        "StorageClass": NotRequired[S3StorageClassType],
        "UnModifiedSinceConstraint": NotRequired[TimestampTypeDef],
        "SSEAwsKmsKeyId": NotRequired[str],
        "TargetKeyPrefix": NotRequired[str],
        "ObjectLockLegalHoldStatus": NotRequired[S3ObjectLockLegalHoldStatusType],
        "ObjectLockMode": NotRequired[S3ObjectLockModeType],
        "ObjectLockRetainUntilDate": NotRequired[TimestampTypeDef],
        "BucketKeyEnabled": NotRequired[bool],
        "ChecksumAlgorithm": NotRequired[S3ChecksumAlgorithmType],
    },
)

S3BucketDestinationTypeDef = TypedDict(
    "S3BucketDestinationTypeDef",
    {
        "Format": FormatType,
        "OutputSchemaVersion": Literal["V_1"],
        "AccountId": str,
        "Arn": str,
        "Prefix": NotRequired[str],
        "Encryption": NotRequired[StorageLensDataExportEncryptionTypeDef],
    },
)

ObjectLambdaConfigurationTypeDef = TypedDict(
    "ObjectLambdaConfigurationTypeDef",
    {
        "SupportingAccessPoint": str,
        "TransformationConfigurations": Sequence[ObjectLambdaTransformationConfigurationTypeDef],
        "CloudWatchMetricsEnabled": NotRequired[bool],
        "AllowedFeatures": NotRequired[Sequence[ObjectLambdaAllowedFeatureType]],
    },
)

LifecycleRuleTypeDef = TypedDict(
    "LifecycleRuleTypeDef",
    {
        "Status": ExpirationStatusType,
        "Expiration": NotRequired[LifecycleExpirationTypeDef],
        "ID": NotRequired[str],
        "Filter": NotRequired[LifecycleRuleFilterTypeDef],
        "Transitions": NotRequired[List[TransitionTypeDef]],
        "NoncurrentVersionTransitions": NotRequired[List[NoncurrentVersionTransitionTypeDef]],
        "NoncurrentVersionExpiration": NotRequired[NoncurrentVersionExpirationTypeDef],
        "AbortIncompleteMultipartUpload": NotRequired[AbortIncompleteMultipartUploadTypeDef],
    },
)

S3JobManifestGeneratorTypeDef = TypedDict(
    "S3JobManifestGeneratorTypeDef",
    {
        "SourceBucket": str,
        "EnableManifestOutput": bool,
        "ExpectedBucketOwner": NotRequired[str],
        "ManifestOutputLocation": NotRequired[S3ManifestOutputLocationTypeDef],
        "Filter": NotRequired[JobManifestGeneratorFilterTypeDef],
    },
)

ListJobsResultTypeDef = TypedDict(
    "ListJobsResultTypeDef",
    {
        "NextToken": str,
        "Jobs": List[JobListDescriptorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ReplicationRuleTypeDef = TypedDict(
    "ReplicationRuleTypeDef",
    {
        "Status": ReplicationRuleStatusType,
        "Destination": DestinationTypeDef,
        "Bucket": str,
        "ID": NotRequired[str],
        "Priority": NotRequired[int],
        "Prefix": NotRequired[str],
        "Filter": NotRequired[ReplicationRuleFilterTypeDef],
        "SourceSelectionCriteria": NotRequired[SourceSelectionCriteriaTypeDef],
        "ExistingObjectReplication": NotRequired[ExistingObjectReplicationTypeDef],
        "DeleteMarkerReplication": NotRequired[DeleteMarkerReplicationTypeDef],
    },
)

AsyncOperationTypeDef = TypedDict(
    "AsyncOperationTypeDef",
    {
        "CreationTime": NotRequired[datetime],
        "Operation": NotRequired[AsyncOperationNameType],
        "RequestTokenARN": NotRequired[str],
        "RequestParameters": NotRequired[AsyncRequestParametersTypeDef],
        "RequestStatus": NotRequired[str],
        "ResponseDetails": NotRequired[AsyncResponseDetailsTypeDef],
    },
)

BucketLevelTypeDef = TypedDict(
    "BucketLevelTypeDef",
    {
        "ActivityMetrics": NotRequired[ActivityMetricsTypeDef],
        "PrefixLevel": NotRequired[PrefixLevelTypeDef],
        "AdvancedCostOptimizationMetrics": NotRequired[AdvancedCostOptimizationMetricsTypeDef],
        "AdvancedDataProtectionMetrics": NotRequired[AdvancedDataProtectionMetricsTypeDef],
        "DetailedStatusCodesMetrics": NotRequired[DetailedStatusCodesMetricsTypeDef],
    },
)

S3AccessControlPolicyTypeDef = TypedDict(
    "S3AccessControlPolicyTypeDef",
    {
        "AccessControlList": NotRequired[S3AccessControlListTypeDef],
        "CannedAccessControlList": NotRequired[S3CannedAccessControlListType],
    },
)

StorageLensDataExportTypeDef = TypedDict(
    "StorageLensDataExportTypeDef",
    {
        "S3BucketDestination": NotRequired[S3BucketDestinationTypeDef],
        "CloudWatchMetrics": NotRequired[CloudWatchMetricsTypeDef],
    },
)

CreateAccessPointForObjectLambdaRequestRequestTypeDef = TypedDict(
    "CreateAccessPointForObjectLambdaRequestRequestTypeDef",
    {
        "AccountId": str,
        "Name": str,
        "Configuration": ObjectLambdaConfigurationTypeDef,
    },
)

GetAccessPointConfigurationForObjectLambdaResultTypeDef = TypedDict(
    "GetAccessPointConfigurationForObjectLambdaResultTypeDef",
    {
        "Configuration": ObjectLambdaConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutAccessPointConfigurationForObjectLambdaRequestRequestTypeDef = TypedDict(
    "PutAccessPointConfigurationForObjectLambdaRequestRequestTypeDef",
    {
        "AccountId": str,
        "Name": str,
        "Configuration": ObjectLambdaConfigurationTypeDef,
    },
)

GetBucketLifecycleConfigurationResultTypeDef = TypedDict(
    "GetBucketLifecycleConfigurationResultTypeDef",
    {
        "Rules": List[LifecycleRuleTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LifecycleConfigurationTypeDef = TypedDict(
    "LifecycleConfigurationTypeDef",
    {
        "Rules": NotRequired[Sequence[LifecycleRuleTypeDef]],
    },
)

JobManifestGeneratorTypeDef = TypedDict(
    "JobManifestGeneratorTypeDef",
    {
        "S3JobManifestGenerator": NotRequired[S3JobManifestGeneratorTypeDef],
    },
)

ReplicationConfigurationTypeDef = TypedDict(
    "ReplicationConfigurationTypeDef",
    {
        "Role": str,
        "Rules": List[ReplicationRuleTypeDef],
    },
)

DescribeMultiRegionAccessPointOperationResultTypeDef = TypedDict(
    "DescribeMultiRegionAccessPointOperationResultTypeDef",
    {
        "AsyncOperation": AsyncOperationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AccountLevelTypeDef = TypedDict(
    "AccountLevelTypeDef",
    {
        "BucketLevel": BucketLevelTypeDef,
        "ActivityMetrics": NotRequired[ActivityMetricsTypeDef],
        "AdvancedCostOptimizationMetrics": NotRequired[AdvancedCostOptimizationMetricsTypeDef],
        "AdvancedDataProtectionMetrics": NotRequired[AdvancedDataProtectionMetricsTypeDef],
        "DetailedStatusCodesMetrics": NotRequired[DetailedStatusCodesMetricsTypeDef],
    },
)

S3SetObjectAclOperationTypeDef = TypedDict(
    "S3SetObjectAclOperationTypeDef",
    {
        "AccessControlPolicy": NotRequired[S3AccessControlPolicyTypeDef],
    },
)

PutBucketLifecycleConfigurationRequestRequestTypeDef = TypedDict(
    "PutBucketLifecycleConfigurationRequestRequestTypeDef",
    {
        "AccountId": str,
        "Bucket": str,
        "LifecycleConfiguration": NotRequired[LifecycleConfigurationTypeDef],
    },
)

GetBucketReplicationResultTypeDef = TypedDict(
    "GetBucketReplicationResultTypeDef",
    {
        "ReplicationConfiguration": ReplicationConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutBucketReplicationRequestRequestTypeDef = TypedDict(
    "PutBucketReplicationRequestRequestTypeDef",
    {
        "AccountId": str,
        "Bucket": str,
        "ReplicationConfiguration": ReplicationConfigurationTypeDef,
    },
)

StorageLensConfigurationTypeDef = TypedDict(
    "StorageLensConfigurationTypeDef",
    {
        "Id": str,
        "AccountLevel": AccountLevelTypeDef,
        "IsEnabled": bool,
        "Include": NotRequired[IncludeTypeDef],
        "Exclude": NotRequired[ExcludeTypeDef],
        "DataExport": NotRequired[StorageLensDataExportTypeDef],
        "AwsOrg": NotRequired[StorageLensAwsOrgTypeDef],
        "StorageLensArn": NotRequired[str],
    },
)

JobOperationTypeDef = TypedDict(
    "JobOperationTypeDef",
    {
        "LambdaInvoke": NotRequired[LambdaInvokeOperationTypeDef],
        "S3PutObjectCopy": NotRequired[S3CopyObjectOperationTypeDef],
        "S3PutObjectAcl": NotRequired[S3SetObjectAclOperationTypeDef],
        "S3PutObjectTagging": NotRequired[S3SetObjectTaggingOperationTypeDef],
        "S3DeleteObjectTagging": NotRequired[Mapping[str, Any]],
        "S3InitiateRestoreObject": NotRequired[S3InitiateRestoreObjectOperationTypeDef],
        "S3PutObjectLegalHold": NotRequired[S3SetObjectLegalHoldOperationTypeDef],
        "S3PutObjectRetention": NotRequired[S3SetObjectRetentionOperationTypeDef],
        "S3ReplicateObject": NotRequired[Mapping[str, Any]],
    },
)

GetStorageLensConfigurationResultTypeDef = TypedDict(
    "GetStorageLensConfigurationResultTypeDef",
    {
        "StorageLensConfiguration": StorageLensConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutStorageLensConfigurationRequestRequestTypeDef = TypedDict(
    "PutStorageLensConfigurationRequestRequestTypeDef",
    {
        "ConfigId": str,
        "AccountId": str,
        "StorageLensConfiguration": StorageLensConfigurationTypeDef,
        "Tags": NotRequired[Sequence[StorageLensTagTypeDef]],
    },
)

CreateJobRequestRequestTypeDef = TypedDict(
    "CreateJobRequestRequestTypeDef",
    {
        "AccountId": str,
        "Operation": JobOperationTypeDef,
        "Report": JobReportTypeDef,
        "ClientRequestToken": str,
        "Priority": int,
        "RoleArn": str,
        "ConfirmationRequired": NotRequired[bool],
        "Manifest": NotRequired[JobManifestTypeDef],
        "Description": NotRequired[str],
        "Tags": NotRequired[Sequence[S3TagTypeDef]],
        "ManifestGenerator": NotRequired[JobManifestGeneratorTypeDef],
    },
)

JobDescriptorTypeDef = TypedDict(
    "JobDescriptorTypeDef",
    {
        "JobId": NotRequired[str],
        "ConfirmationRequired": NotRequired[bool],
        "Description": NotRequired[str],
        "JobArn": NotRequired[str],
        "Status": NotRequired[JobStatusType],
        "Manifest": NotRequired[JobManifestTypeDef],
        "Operation": NotRequired[JobOperationTypeDef],
        "Priority": NotRequired[int],
        "ProgressSummary": NotRequired[JobProgressSummaryTypeDef],
        "StatusUpdateReason": NotRequired[str],
        "FailureReasons": NotRequired[List[JobFailureTypeDef]],
        "Report": NotRequired[JobReportTypeDef],
        "CreationTime": NotRequired[datetime],
        "TerminationDate": NotRequired[datetime],
        "RoleArn": NotRequired[str],
        "SuspendedDate": NotRequired[datetime],
        "SuspendedCause": NotRequired[str],
        "ManifestGenerator": NotRequired[JobManifestGeneratorTypeDef],
        "GeneratedManifestDescriptor": NotRequired[S3GeneratedManifestDescriptorTypeDef],
    },
)

DescribeJobResultTypeDef = TypedDict(
    "DescribeJobResultTypeDef",
    {
        "Job": JobDescriptorTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
