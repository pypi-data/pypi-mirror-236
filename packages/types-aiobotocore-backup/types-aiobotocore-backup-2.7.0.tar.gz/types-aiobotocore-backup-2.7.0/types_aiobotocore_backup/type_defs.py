"""
Type annotations for backup service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_backup/type_defs/)

Usage::

    ```python
    from types_aiobotocore_backup.type_defs import AdvancedBackupSettingPaginatorTypeDef

    data: AdvancedBackupSettingPaginatorTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    BackupJobStateType,
    BackupVaultEventType,
    CopyJobStateType,
    LegalHoldStatusType,
    RecoveryPointStatusType,
    RestoreJobStatusType,
    StorageClassType,
    VaultStateType,
    VaultTypeType,
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
    "AdvancedBackupSettingPaginatorTypeDef",
    "AdvancedBackupSettingTypeDef",
    "RecoveryPointCreatorTypeDef",
    "BackupPlanTemplatesListMemberTypeDef",
    "LifecycleTypeDef",
    "ConditionTypeDef",
    "BackupSelectionsListMemberTypeDef",
    "BackupVaultListMemberTypeDef",
    "CalculatedLifecycleTypeDef",
    "CancelLegalHoldInputRequestTypeDef",
    "ConditionParameterTypeDef",
    "ControlInputParameterTypeDef",
    "ControlScopeTypeDef",
    "ResponseMetadataTypeDef",
    "CreateBackupVaultInputRequestTypeDef",
    "CreateLogicallyAirGappedBackupVaultInputRequestTypeDef",
    "ReportDeliveryChannelTypeDef",
    "ReportSettingTypeDef",
    "TimestampTypeDef",
    "DeleteBackupPlanInputRequestTypeDef",
    "DeleteBackupSelectionInputRequestTypeDef",
    "DeleteBackupVaultAccessPolicyInputRequestTypeDef",
    "DeleteBackupVaultInputRequestTypeDef",
    "DeleteBackupVaultLockConfigurationInputRequestTypeDef",
    "DeleteBackupVaultNotificationsInputRequestTypeDef",
    "DeleteFrameworkInputRequestTypeDef",
    "DeleteRecoveryPointInputRequestTypeDef",
    "DeleteReportPlanInputRequestTypeDef",
    "DescribeBackupJobInputRequestTypeDef",
    "DescribeBackupVaultInputRequestTypeDef",
    "DescribeCopyJobInputRequestTypeDef",
    "DescribeFrameworkInputRequestTypeDef",
    "DescribeProtectedResourceInputRequestTypeDef",
    "DescribeRecoveryPointInputRequestTypeDef",
    "DescribeReportJobInputRequestTypeDef",
    "DescribeReportPlanInputRequestTypeDef",
    "DescribeRestoreJobInputRequestTypeDef",
    "DisassociateRecoveryPointFromParentInputRequestTypeDef",
    "DisassociateRecoveryPointInputRequestTypeDef",
    "ExportBackupPlanTemplateInputRequestTypeDef",
    "FrameworkTypeDef",
    "GetBackupPlanFromJSONInputRequestTypeDef",
    "GetBackupPlanFromTemplateInputRequestTypeDef",
    "GetBackupPlanInputRequestTypeDef",
    "GetBackupSelectionInputRequestTypeDef",
    "GetBackupVaultAccessPolicyInputRequestTypeDef",
    "GetBackupVaultNotificationsInputRequestTypeDef",
    "GetLegalHoldInputRequestTypeDef",
    "GetRecoveryPointRestoreMetadataInputRequestTypeDef",
    "LegalHoldTypeDef",
    "PaginatorConfigTypeDef",
    "ListBackupPlanTemplatesInputRequestTypeDef",
    "ListBackupPlanVersionsInputRequestTypeDef",
    "ListBackupPlansInputRequestTypeDef",
    "ListBackupSelectionsInputRequestTypeDef",
    "ListBackupVaultsInputRequestTypeDef",
    "ListFrameworksInputRequestTypeDef",
    "ListLegalHoldsInputRequestTypeDef",
    "ListProtectedResourcesByBackupVaultInputRequestTypeDef",
    "ProtectedResourceTypeDef",
    "ListProtectedResourcesInputRequestTypeDef",
    "ListRecoveryPointsByLegalHoldInputRequestTypeDef",
    "RecoveryPointMemberTypeDef",
    "ListRecoveryPointsByResourceInputRequestTypeDef",
    "RecoveryPointByResourceTypeDef",
    "ListReportPlansInputRequestTypeDef",
    "RestoreJobsListMemberTypeDef",
    "ListTagsInputRequestTypeDef",
    "PutBackupVaultAccessPolicyInputRequestTypeDef",
    "PutBackupVaultLockConfigurationInputRequestTypeDef",
    "PutBackupVaultNotificationsInputRequestTypeDef",
    "ReportDestinationTypeDef",
    "StartReportJobInputRequestTypeDef",
    "StartRestoreJobInputRequestTypeDef",
    "StopBackupJobInputRequestTypeDef",
    "TagResourceInputRequestTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UpdateGlobalSettingsInputRequestTypeDef",
    "UpdateRegionSettingsInputRequestTypeDef",
    "BackupPlansListMemberPaginatorTypeDef",
    "BackupPlansListMemberTypeDef",
    "BackupJobTypeDef",
    "CopyJobTypeDef",
    "CopyActionTypeDef",
    "StartBackupJobInputRequestTypeDef",
    "StartCopyJobInputRequestTypeDef",
    "UpdateRecoveryPointLifecycleInputRequestTypeDef",
    "RecoveryPointByBackupVaultTypeDef",
    "ConditionsTypeDef",
    "FrameworkControlTypeDef",
    "CreateBackupPlanOutputTypeDef",
    "CreateBackupSelectionOutputTypeDef",
    "CreateBackupVaultOutputTypeDef",
    "CreateFrameworkOutputTypeDef",
    "CreateLogicallyAirGappedBackupVaultOutputTypeDef",
    "CreateReportPlanOutputTypeDef",
    "DeleteBackupPlanOutputTypeDef",
    "DescribeBackupJobOutputTypeDef",
    "DescribeBackupVaultOutputTypeDef",
    "DescribeGlobalSettingsOutputTypeDef",
    "DescribeProtectedResourceOutputTypeDef",
    "DescribeRecoveryPointOutputTypeDef",
    "DescribeRegionSettingsOutputTypeDef",
    "DescribeRestoreJobOutputTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ExportBackupPlanTemplateOutputTypeDef",
    "GetBackupVaultAccessPolicyOutputTypeDef",
    "GetBackupVaultNotificationsOutputTypeDef",
    "GetRecoveryPointRestoreMetadataOutputTypeDef",
    "GetSupportedResourceTypesOutputTypeDef",
    "ListBackupPlanTemplatesOutputTypeDef",
    "ListBackupSelectionsOutputTypeDef",
    "ListBackupVaultsOutputTypeDef",
    "ListTagsOutputTypeDef",
    "StartBackupJobOutputTypeDef",
    "StartCopyJobOutputTypeDef",
    "StartReportJobOutputTypeDef",
    "StartRestoreJobOutputTypeDef",
    "UpdateBackupPlanOutputTypeDef",
    "UpdateFrameworkOutputTypeDef",
    "UpdateRecoveryPointLifecycleOutputTypeDef",
    "UpdateReportPlanOutputTypeDef",
    "CreateReportPlanInputRequestTypeDef",
    "ReportPlanTypeDef",
    "UpdateReportPlanInputRequestTypeDef",
    "DateRangeTypeDef",
    "ListBackupJobsInputRequestTypeDef",
    "ListCopyJobsInputRequestTypeDef",
    "ListRecoveryPointsByBackupVaultInputRequestTypeDef",
    "ListReportJobsInputRequestTypeDef",
    "ListRestoreJobsInputRequestTypeDef",
    "ListFrameworksOutputTypeDef",
    "ListLegalHoldsOutputTypeDef",
    "ListBackupJobsInputListBackupJobsPaginateTypeDef",
    "ListBackupPlanTemplatesInputListBackupPlanTemplatesPaginateTypeDef",
    "ListBackupPlanVersionsInputListBackupPlanVersionsPaginateTypeDef",
    "ListBackupPlansInputListBackupPlansPaginateTypeDef",
    "ListBackupSelectionsInputListBackupSelectionsPaginateTypeDef",
    "ListBackupVaultsInputListBackupVaultsPaginateTypeDef",
    "ListCopyJobsInputListCopyJobsPaginateTypeDef",
    "ListLegalHoldsInputListLegalHoldsPaginateTypeDef",
    "ListProtectedResourcesByBackupVaultInputListProtectedResourcesByBackupVaultPaginateTypeDef",
    "ListProtectedResourcesInputListProtectedResourcesPaginateTypeDef",
    "ListRecoveryPointsByBackupVaultInputListRecoveryPointsByBackupVaultPaginateTypeDef",
    "ListRecoveryPointsByLegalHoldInputListRecoveryPointsByLegalHoldPaginateTypeDef",
    "ListRecoveryPointsByResourceInputListRecoveryPointsByResourcePaginateTypeDef",
    "ListRestoreJobsInputListRestoreJobsPaginateTypeDef",
    "ListProtectedResourcesByBackupVaultOutputTypeDef",
    "ListProtectedResourcesOutputTypeDef",
    "ListRecoveryPointsByLegalHoldOutputTypeDef",
    "ListRecoveryPointsByResourceOutputTypeDef",
    "ListRestoreJobsOutputTypeDef",
    "ReportJobTypeDef",
    "ListBackupPlanVersionsOutputPaginatorTypeDef",
    "ListBackupPlansOutputPaginatorTypeDef",
    "ListBackupPlanVersionsOutputTypeDef",
    "ListBackupPlansOutputTypeDef",
    "ListBackupJobsOutputTypeDef",
    "DescribeCopyJobOutputTypeDef",
    "ListCopyJobsOutputTypeDef",
    "BackupRuleInputTypeDef",
    "BackupRuleTypeDef",
    "ListRecoveryPointsByBackupVaultOutputTypeDef",
    "BackupSelectionTypeDef",
    "CreateFrameworkInputRequestTypeDef",
    "DescribeFrameworkOutputTypeDef",
    "UpdateFrameworkInputRequestTypeDef",
    "DescribeReportPlanOutputTypeDef",
    "ListReportPlansOutputTypeDef",
    "RecoveryPointSelectionTypeDef",
    "DescribeReportJobOutputTypeDef",
    "ListReportJobsOutputTypeDef",
    "BackupPlanInputTypeDef",
    "BackupPlanTypeDef",
    "CreateBackupSelectionInputRequestTypeDef",
    "GetBackupSelectionOutputTypeDef",
    "CreateLegalHoldInputRequestTypeDef",
    "CreateLegalHoldOutputTypeDef",
    "GetLegalHoldOutputTypeDef",
    "CreateBackupPlanInputRequestTypeDef",
    "UpdateBackupPlanInputRequestTypeDef",
    "GetBackupPlanFromJSONOutputTypeDef",
    "GetBackupPlanFromTemplateOutputTypeDef",
    "GetBackupPlanOutputTypeDef",
)

AdvancedBackupSettingPaginatorTypeDef = TypedDict(
    "AdvancedBackupSettingPaginatorTypeDef",
    {
        "ResourceType": NotRequired[str],
        "BackupOptions": NotRequired[Dict[str, str]],
    },
)

AdvancedBackupSettingTypeDef = TypedDict(
    "AdvancedBackupSettingTypeDef",
    {
        "ResourceType": NotRequired[str],
        "BackupOptions": NotRequired[Mapping[str, str]],
    },
)

RecoveryPointCreatorTypeDef = TypedDict(
    "RecoveryPointCreatorTypeDef",
    {
        "BackupPlanId": NotRequired[str],
        "BackupPlanArn": NotRequired[str],
        "BackupPlanVersion": NotRequired[str],
        "BackupRuleId": NotRequired[str],
    },
)

BackupPlanTemplatesListMemberTypeDef = TypedDict(
    "BackupPlanTemplatesListMemberTypeDef",
    {
        "BackupPlanTemplateId": NotRequired[str],
        "BackupPlanTemplateName": NotRequired[str],
    },
)

LifecycleTypeDef = TypedDict(
    "LifecycleTypeDef",
    {
        "MoveToColdStorageAfterDays": NotRequired[int],
        "DeleteAfterDays": NotRequired[int],
    },
)

ConditionTypeDef = TypedDict(
    "ConditionTypeDef",
    {
        "ConditionType": Literal["STRINGEQUALS"],
        "ConditionKey": str,
        "ConditionValue": str,
    },
)

BackupSelectionsListMemberTypeDef = TypedDict(
    "BackupSelectionsListMemberTypeDef",
    {
        "SelectionId": NotRequired[str],
        "SelectionName": NotRequired[str],
        "BackupPlanId": NotRequired[str],
        "CreationDate": NotRequired[datetime],
        "CreatorRequestId": NotRequired[str],
        "IamRoleArn": NotRequired[str],
    },
)

BackupVaultListMemberTypeDef = TypedDict(
    "BackupVaultListMemberTypeDef",
    {
        "BackupVaultName": NotRequired[str],
        "BackupVaultArn": NotRequired[str],
        "CreationDate": NotRequired[datetime],
        "EncryptionKeyArn": NotRequired[str],
        "CreatorRequestId": NotRequired[str],
        "NumberOfRecoveryPoints": NotRequired[int],
        "Locked": NotRequired[bool],
        "MinRetentionDays": NotRequired[int],
        "MaxRetentionDays": NotRequired[int],
        "LockDate": NotRequired[datetime],
    },
)

CalculatedLifecycleTypeDef = TypedDict(
    "CalculatedLifecycleTypeDef",
    {
        "MoveToColdStorageAt": NotRequired[datetime],
        "DeleteAt": NotRequired[datetime],
    },
)

CancelLegalHoldInputRequestTypeDef = TypedDict(
    "CancelLegalHoldInputRequestTypeDef",
    {
        "LegalHoldId": str,
        "CancelDescription": str,
        "RetainRecordInDays": NotRequired[int],
    },
)

ConditionParameterTypeDef = TypedDict(
    "ConditionParameterTypeDef",
    {
        "ConditionKey": NotRequired[str],
        "ConditionValue": NotRequired[str],
    },
)

ControlInputParameterTypeDef = TypedDict(
    "ControlInputParameterTypeDef",
    {
        "ParameterName": NotRequired[str],
        "ParameterValue": NotRequired[str],
    },
)

ControlScopeTypeDef = TypedDict(
    "ControlScopeTypeDef",
    {
        "ComplianceResourceIds": NotRequired[Sequence[str]],
        "ComplianceResourceTypes": NotRequired[Sequence[str]],
        "Tags": NotRequired[Mapping[str, str]],
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

CreateBackupVaultInputRequestTypeDef = TypedDict(
    "CreateBackupVaultInputRequestTypeDef",
    {
        "BackupVaultName": str,
        "BackupVaultTags": NotRequired[Mapping[str, str]],
        "EncryptionKeyArn": NotRequired[str],
        "CreatorRequestId": NotRequired[str],
    },
)

CreateLogicallyAirGappedBackupVaultInputRequestTypeDef = TypedDict(
    "CreateLogicallyAirGappedBackupVaultInputRequestTypeDef",
    {
        "BackupVaultName": str,
        "MinRetentionDays": int,
        "MaxRetentionDays": int,
        "BackupVaultTags": NotRequired[Mapping[str, str]],
        "CreatorRequestId": NotRequired[str],
    },
)

ReportDeliveryChannelTypeDef = TypedDict(
    "ReportDeliveryChannelTypeDef",
    {
        "S3BucketName": str,
        "S3KeyPrefix": NotRequired[str],
        "Formats": NotRequired[Sequence[str]],
    },
)

ReportSettingTypeDef = TypedDict(
    "ReportSettingTypeDef",
    {
        "ReportTemplate": str,
        "FrameworkArns": NotRequired[Sequence[str]],
        "NumberOfFrameworks": NotRequired[int],
        "Accounts": NotRequired[Sequence[str]],
        "OrganizationUnits": NotRequired[Sequence[str]],
        "Regions": NotRequired[Sequence[str]],
    },
)

TimestampTypeDef = Union[datetime, str]
DeleteBackupPlanInputRequestTypeDef = TypedDict(
    "DeleteBackupPlanInputRequestTypeDef",
    {
        "BackupPlanId": str,
    },
)

DeleteBackupSelectionInputRequestTypeDef = TypedDict(
    "DeleteBackupSelectionInputRequestTypeDef",
    {
        "BackupPlanId": str,
        "SelectionId": str,
    },
)

DeleteBackupVaultAccessPolicyInputRequestTypeDef = TypedDict(
    "DeleteBackupVaultAccessPolicyInputRequestTypeDef",
    {
        "BackupVaultName": str,
    },
)

DeleteBackupVaultInputRequestTypeDef = TypedDict(
    "DeleteBackupVaultInputRequestTypeDef",
    {
        "BackupVaultName": str,
    },
)

DeleteBackupVaultLockConfigurationInputRequestTypeDef = TypedDict(
    "DeleteBackupVaultLockConfigurationInputRequestTypeDef",
    {
        "BackupVaultName": str,
    },
)

DeleteBackupVaultNotificationsInputRequestTypeDef = TypedDict(
    "DeleteBackupVaultNotificationsInputRequestTypeDef",
    {
        "BackupVaultName": str,
    },
)

DeleteFrameworkInputRequestTypeDef = TypedDict(
    "DeleteFrameworkInputRequestTypeDef",
    {
        "FrameworkName": str,
    },
)

DeleteRecoveryPointInputRequestTypeDef = TypedDict(
    "DeleteRecoveryPointInputRequestTypeDef",
    {
        "BackupVaultName": str,
        "RecoveryPointArn": str,
    },
)

DeleteReportPlanInputRequestTypeDef = TypedDict(
    "DeleteReportPlanInputRequestTypeDef",
    {
        "ReportPlanName": str,
    },
)

DescribeBackupJobInputRequestTypeDef = TypedDict(
    "DescribeBackupJobInputRequestTypeDef",
    {
        "BackupJobId": str,
    },
)

DescribeBackupVaultInputRequestTypeDef = TypedDict(
    "DescribeBackupVaultInputRequestTypeDef",
    {
        "BackupVaultName": str,
        "BackupVaultAccountId": NotRequired[str],
    },
)

DescribeCopyJobInputRequestTypeDef = TypedDict(
    "DescribeCopyJobInputRequestTypeDef",
    {
        "CopyJobId": str,
    },
)

DescribeFrameworkInputRequestTypeDef = TypedDict(
    "DescribeFrameworkInputRequestTypeDef",
    {
        "FrameworkName": str,
    },
)

DescribeProtectedResourceInputRequestTypeDef = TypedDict(
    "DescribeProtectedResourceInputRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

DescribeRecoveryPointInputRequestTypeDef = TypedDict(
    "DescribeRecoveryPointInputRequestTypeDef",
    {
        "BackupVaultName": str,
        "RecoveryPointArn": str,
        "BackupVaultAccountId": NotRequired[str],
    },
)

DescribeReportJobInputRequestTypeDef = TypedDict(
    "DescribeReportJobInputRequestTypeDef",
    {
        "ReportJobId": str,
    },
)

DescribeReportPlanInputRequestTypeDef = TypedDict(
    "DescribeReportPlanInputRequestTypeDef",
    {
        "ReportPlanName": str,
    },
)

DescribeRestoreJobInputRequestTypeDef = TypedDict(
    "DescribeRestoreJobInputRequestTypeDef",
    {
        "RestoreJobId": str,
    },
)

DisassociateRecoveryPointFromParentInputRequestTypeDef = TypedDict(
    "DisassociateRecoveryPointFromParentInputRequestTypeDef",
    {
        "BackupVaultName": str,
        "RecoveryPointArn": str,
    },
)

DisassociateRecoveryPointInputRequestTypeDef = TypedDict(
    "DisassociateRecoveryPointInputRequestTypeDef",
    {
        "BackupVaultName": str,
        "RecoveryPointArn": str,
    },
)

ExportBackupPlanTemplateInputRequestTypeDef = TypedDict(
    "ExportBackupPlanTemplateInputRequestTypeDef",
    {
        "BackupPlanId": str,
    },
)

FrameworkTypeDef = TypedDict(
    "FrameworkTypeDef",
    {
        "FrameworkName": NotRequired[str],
        "FrameworkArn": NotRequired[str],
        "FrameworkDescription": NotRequired[str],
        "NumberOfControls": NotRequired[int],
        "CreationTime": NotRequired[datetime],
        "DeploymentStatus": NotRequired[str],
    },
)

GetBackupPlanFromJSONInputRequestTypeDef = TypedDict(
    "GetBackupPlanFromJSONInputRequestTypeDef",
    {
        "BackupPlanTemplateJson": str,
    },
)

GetBackupPlanFromTemplateInputRequestTypeDef = TypedDict(
    "GetBackupPlanFromTemplateInputRequestTypeDef",
    {
        "BackupPlanTemplateId": str,
    },
)

GetBackupPlanInputRequestTypeDef = TypedDict(
    "GetBackupPlanInputRequestTypeDef",
    {
        "BackupPlanId": str,
        "VersionId": NotRequired[str],
    },
)

GetBackupSelectionInputRequestTypeDef = TypedDict(
    "GetBackupSelectionInputRequestTypeDef",
    {
        "BackupPlanId": str,
        "SelectionId": str,
    },
)

GetBackupVaultAccessPolicyInputRequestTypeDef = TypedDict(
    "GetBackupVaultAccessPolicyInputRequestTypeDef",
    {
        "BackupVaultName": str,
    },
)

GetBackupVaultNotificationsInputRequestTypeDef = TypedDict(
    "GetBackupVaultNotificationsInputRequestTypeDef",
    {
        "BackupVaultName": str,
    },
)

GetLegalHoldInputRequestTypeDef = TypedDict(
    "GetLegalHoldInputRequestTypeDef",
    {
        "LegalHoldId": str,
    },
)

GetRecoveryPointRestoreMetadataInputRequestTypeDef = TypedDict(
    "GetRecoveryPointRestoreMetadataInputRequestTypeDef",
    {
        "BackupVaultName": str,
        "RecoveryPointArn": str,
        "BackupVaultAccountId": NotRequired[str],
    },
)

LegalHoldTypeDef = TypedDict(
    "LegalHoldTypeDef",
    {
        "Title": NotRequired[str],
        "Status": NotRequired[LegalHoldStatusType],
        "Description": NotRequired[str],
        "LegalHoldId": NotRequired[str],
        "LegalHoldArn": NotRequired[str],
        "CreationDate": NotRequired[datetime],
        "CancellationDate": NotRequired[datetime],
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

ListBackupPlanTemplatesInputRequestTypeDef = TypedDict(
    "ListBackupPlanTemplatesInputRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ListBackupPlanVersionsInputRequestTypeDef = TypedDict(
    "ListBackupPlanVersionsInputRequestTypeDef",
    {
        "BackupPlanId": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ListBackupPlansInputRequestTypeDef = TypedDict(
    "ListBackupPlansInputRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
        "IncludeDeleted": NotRequired[bool],
    },
)

ListBackupSelectionsInputRequestTypeDef = TypedDict(
    "ListBackupSelectionsInputRequestTypeDef",
    {
        "BackupPlanId": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ListBackupVaultsInputRequestTypeDef = TypedDict(
    "ListBackupVaultsInputRequestTypeDef",
    {
        "ByVaultType": NotRequired[VaultTypeType],
        "ByShared": NotRequired[bool],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ListFrameworksInputRequestTypeDef = TypedDict(
    "ListFrameworksInputRequestTypeDef",
    {
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

ListLegalHoldsInputRequestTypeDef = TypedDict(
    "ListLegalHoldsInputRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ListProtectedResourcesByBackupVaultInputRequestTypeDef = TypedDict(
    "ListProtectedResourcesByBackupVaultInputRequestTypeDef",
    {
        "BackupVaultName": str,
        "BackupVaultAccountId": NotRequired[str],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ProtectedResourceTypeDef = TypedDict(
    "ProtectedResourceTypeDef",
    {
        "ResourceArn": NotRequired[str],
        "ResourceType": NotRequired[str],
        "LastBackupTime": NotRequired[datetime],
        "ResourceName": NotRequired[str],
    },
)

ListProtectedResourcesInputRequestTypeDef = TypedDict(
    "ListProtectedResourcesInputRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ListRecoveryPointsByLegalHoldInputRequestTypeDef = TypedDict(
    "ListRecoveryPointsByLegalHoldInputRequestTypeDef",
    {
        "LegalHoldId": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

RecoveryPointMemberTypeDef = TypedDict(
    "RecoveryPointMemberTypeDef",
    {
        "RecoveryPointArn": NotRequired[str],
        "ResourceArn": NotRequired[str],
        "ResourceType": NotRequired[str],
        "BackupVaultName": NotRequired[str],
    },
)

ListRecoveryPointsByResourceInputRequestTypeDef = TypedDict(
    "ListRecoveryPointsByResourceInputRequestTypeDef",
    {
        "ResourceArn": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

RecoveryPointByResourceTypeDef = TypedDict(
    "RecoveryPointByResourceTypeDef",
    {
        "RecoveryPointArn": NotRequired[str],
        "CreationDate": NotRequired[datetime],
        "Status": NotRequired[RecoveryPointStatusType],
        "StatusMessage": NotRequired[str],
        "EncryptionKeyArn": NotRequired[str],
        "BackupSizeBytes": NotRequired[int],
        "BackupVaultName": NotRequired[str],
        "IsParent": NotRequired[bool],
        "ParentRecoveryPointArn": NotRequired[str],
        "ResourceName": NotRequired[str],
    },
)

ListReportPlansInputRequestTypeDef = TypedDict(
    "ListReportPlansInputRequestTypeDef",
    {
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

RestoreJobsListMemberTypeDef = TypedDict(
    "RestoreJobsListMemberTypeDef",
    {
        "AccountId": NotRequired[str],
        "RestoreJobId": NotRequired[str],
        "RecoveryPointArn": NotRequired[str],
        "CreationDate": NotRequired[datetime],
        "CompletionDate": NotRequired[datetime],
        "Status": NotRequired[RestoreJobStatusType],
        "StatusMessage": NotRequired[str],
        "PercentDone": NotRequired[str],
        "BackupSizeInBytes": NotRequired[int],
        "IamRoleArn": NotRequired[str],
        "ExpectedCompletionTimeMinutes": NotRequired[int],
        "CreatedResourceArn": NotRequired[str],
        "ResourceType": NotRequired[str],
    },
)

ListTagsInputRequestTypeDef = TypedDict(
    "ListTagsInputRequestTypeDef",
    {
        "ResourceArn": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

PutBackupVaultAccessPolicyInputRequestTypeDef = TypedDict(
    "PutBackupVaultAccessPolicyInputRequestTypeDef",
    {
        "BackupVaultName": str,
        "Policy": NotRequired[str],
    },
)

PutBackupVaultLockConfigurationInputRequestTypeDef = TypedDict(
    "PutBackupVaultLockConfigurationInputRequestTypeDef",
    {
        "BackupVaultName": str,
        "MinRetentionDays": NotRequired[int],
        "MaxRetentionDays": NotRequired[int],
        "ChangeableForDays": NotRequired[int],
    },
)

PutBackupVaultNotificationsInputRequestTypeDef = TypedDict(
    "PutBackupVaultNotificationsInputRequestTypeDef",
    {
        "BackupVaultName": str,
        "SNSTopicArn": str,
        "BackupVaultEvents": Sequence[BackupVaultEventType],
    },
)

ReportDestinationTypeDef = TypedDict(
    "ReportDestinationTypeDef",
    {
        "S3BucketName": NotRequired[str],
        "S3Keys": NotRequired[List[str]],
    },
)

StartReportJobInputRequestTypeDef = TypedDict(
    "StartReportJobInputRequestTypeDef",
    {
        "ReportPlanName": str,
        "IdempotencyToken": NotRequired[str],
    },
)

StartRestoreJobInputRequestTypeDef = TypedDict(
    "StartRestoreJobInputRequestTypeDef",
    {
        "RecoveryPointArn": str,
        "Metadata": Mapping[str, str],
        "IamRoleArn": NotRequired[str],
        "IdempotencyToken": NotRequired[str],
        "ResourceType": NotRequired[str],
        "CopySourceTagsToRestoredResource": NotRequired[bool],
    },
)

StopBackupJobInputRequestTypeDef = TypedDict(
    "StopBackupJobInputRequestTypeDef",
    {
        "BackupJobId": str,
    },
)

TagResourceInputRequestTypeDef = TypedDict(
    "TagResourceInputRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Mapping[str, str],
    },
)

UntagResourceInputRequestTypeDef = TypedDict(
    "UntagResourceInputRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeyList": Sequence[str],
    },
)

UpdateGlobalSettingsInputRequestTypeDef = TypedDict(
    "UpdateGlobalSettingsInputRequestTypeDef",
    {
        "GlobalSettings": NotRequired[Mapping[str, str]],
    },
)

UpdateRegionSettingsInputRequestTypeDef = TypedDict(
    "UpdateRegionSettingsInputRequestTypeDef",
    {
        "ResourceTypeOptInPreference": NotRequired[Mapping[str, bool]],
        "ResourceTypeManagementPreference": NotRequired[Mapping[str, bool]],
    },
)

BackupPlansListMemberPaginatorTypeDef = TypedDict(
    "BackupPlansListMemberPaginatorTypeDef",
    {
        "BackupPlanArn": NotRequired[str],
        "BackupPlanId": NotRequired[str],
        "CreationDate": NotRequired[datetime],
        "DeletionDate": NotRequired[datetime],
        "VersionId": NotRequired[str],
        "BackupPlanName": NotRequired[str],
        "CreatorRequestId": NotRequired[str],
        "LastExecutionDate": NotRequired[datetime],
        "AdvancedBackupSettings": NotRequired[List[AdvancedBackupSettingPaginatorTypeDef]],
    },
)

BackupPlansListMemberTypeDef = TypedDict(
    "BackupPlansListMemberTypeDef",
    {
        "BackupPlanArn": NotRequired[str],
        "BackupPlanId": NotRequired[str],
        "CreationDate": NotRequired[datetime],
        "DeletionDate": NotRequired[datetime],
        "VersionId": NotRequired[str],
        "BackupPlanName": NotRequired[str],
        "CreatorRequestId": NotRequired[str],
        "LastExecutionDate": NotRequired[datetime],
        "AdvancedBackupSettings": NotRequired[List[AdvancedBackupSettingTypeDef]],
    },
)

BackupJobTypeDef = TypedDict(
    "BackupJobTypeDef",
    {
        "AccountId": NotRequired[str],
        "BackupJobId": NotRequired[str],
        "BackupVaultName": NotRequired[str],
        "BackupVaultArn": NotRequired[str],
        "RecoveryPointArn": NotRequired[str],
        "ResourceArn": NotRequired[str],
        "CreationDate": NotRequired[datetime],
        "CompletionDate": NotRequired[datetime],
        "State": NotRequired[BackupJobStateType],
        "StatusMessage": NotRequired[str],
        "PercentDone": NotRequired[str],
        "BackupSizeInBytes": NotRequired[int],
        "IamRoleArn": NotRequired[str],
        "CreatedBy": NotRequired[RecoveryPointCreatorTypeDef],
        "ExpectedCompletionDate": NotRequired[datetime],
        "StartBy": NotRequired[datetime],
        "ResourceType": NotRequired[str],
        "BytesTransferred": NotRequired[int],
        "BackupOptions": NotRequired[Dict[str, str]],
        "BackupType": NotRequired[str],
        "ParentJobId": NotRequired[str],
        "IsParent": NotRequired[bool],
        "ResourceName": NotRequired[str],
    },
)

CopyJobTypeDef = TypedDict(
    "CopyJobTypeDef",
    {
        "AccountId": NotRequired[str],
        "CopyJobId": NotRequired[str],
        "SourceBackupVaultArn": NotRequired[str],
        "SourceRecoveryPointArn": NotRequired[str],
        "DestinationBackupVaultArn": NotRequired[str],
        "DestinationRecoveryPointArn": NotRequired[str],
        "ResourceArn": NotRequired[str],
        "CreationDate": NotRequired[datetime],
        "CompletionDate": NotRequired[datetime],
        "State": NotRequired[CopyJobStateType],
        "StatusMessage": NotRequired[str],
        "BackupSizeInBytes": NotRequired[int],
        "IamRoleArn": NotRequired[str],
        "CreatedBy": NotRequired[RecoveryPointCreatorTypeDef],
        "ResourceType": NotRequired[str],
        "ParentJobId": NotRequired[str],
        "IsParent": NotRequired[bool],
        "CompositeMemberIdentifier": NotRequired[str],
        "NumberOfChildJobs": NotRequired[int],
        "ChildJobsInState": NotRequired[Dict[CopyJobStateType, int]],
        "ResourceName": NotRequired[str],
    },
)

CopyActionTypeDef = TypedDict(
    "CopyActionTypeDef",
    {
        "DestinationBackupVaultArn": str,
        "Lifecycle": NotRequired[LifecycleTypeDef],
    },
)

StartBackupJobInputRequestTypeDef = TypedDict(
    "StartBackupJobInputRequestTypeDef",
    {
        "BackupVaultName": str,
        "ResourceArn": str,
        "IamRoleArn": str,
        "IdempotencyToken": NotRequired[str],
        "StartWindowMinutes": NotRequired[int],
        "CompleteWindowMinutes": NotRequired[int],
        "Lifecycle": NotRequired[LifecycleTypeDef],
        "RecoveryPointTags": NotRequired[Mapping[str, str]],
        "BackupOptions": NotRequired[Mapping[str, str]],
    },
)

StartCopyJobInputRequestTypeDef = TypedDict(
    "StartCopyJobInputRequestTypeDef",
    {
        "RecoveryPointArn": str,
        "SourceBackupVaultName": str,
        "DestinationBackupVaultArn": str,
        "IamRoleArn": str,
        "IdempotencyToken": NotRequired[str],
        "Lifecycle": NotRequired[LifecycleTypeDef],
    },
)

UpdateRecoveryPointLifecycleInputRequestTypeDef = TypedDict(
    "UpdateRecoveryPointLifecycleInputRequestTypeDef",
    {
        "BackupVaultName": str,
        "RecoveryPointArn": str,
        "Lifecycle": NotRequired[LifecycleTypeDef],
    },
)

RecoveryPointByBackupVaultTypeDef = TypedDict(
    "RecoveryPointByBackupVaultTypeDef",
    {
        "RecoveryPointArn": NotRequired[str],
        "BackupVaultName": NotRequired[str],
        "BackupVaultArn": NotRequired[str],
        "SourceBackupVaultArn": NotRequired[str],
        "ResourceArn": NotRequired[str],
        "ResourceType": NotRequired[str],
        "CreatedBy": NotRequired[RecoveryPointCreatorTypeDef],
        "IamRoleArn": NotRequired[str],
        "Status": NotRequired[RecoveryPointStatusType],
        "StatusMessage": NotRequired[str],
        "CreationDate": NotRequired[datetime],
        "CompletionDate": NotRequired[datetime],
        "BackupSizeInBytes": NotRequired[int],
        "CalculatedLifecycle": NotRequired[CalculatedLifecycleTypeDef],
        "Lifecycle": NotRequired[LifecycleTypeDef],
        "EncryptionKeyArn": NotRequired[str],
        "IsEncrypted": NotRequired[bool],
        "LastRestoreTime": NotRequired[datetime],
        "ParentRecoveryPointArn": NotRequired[str],
        "CompositeMemberIdentifier": NotRequired[str],
        "IsParent": NotRequired[bool],
        "ResourceName": NotRequired[str],
    },
)

ConditionsTypeDef = TypedDict(
    "ConditionsTypeDef",
    {
        "StringEquals": NotRequired[Sequence[ConditionParameterTypeDef]],
        "StringNotEquals": NotRequired[Sequence[ConditionParameterTypeDef]],
        "StringLike": NotRequired[Sequence[ConditionParameterTypeDef]],
        "StringNotLike": NotRequired[Sequence[ConditionParameterTypeDef]],
    },
)

FrameworkControlTypeDef = TypedDict(
    "FrameworkControlTypeDef",
    {
        "ControlName": str,
        "ControlInputParameters": NotRequired[Sequence[ControlInputParameterTypeDef]],
        "ControlScope": NotRequired[ControlScopeTypeDef],
    },
)

CreateBackupPlanOutputTypeDef = TypedDict(
    "CreateBackupPlanOutputTypeDef",
    {
        "BackupPlanId": str,
        "BackupPlanArn": str,
        "CreationDate": datetime,
        "VersionId": str,
        "AdvancedBackupSettings": List[AdvancedBackupSettingTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateBackupSelectionOutputTypeDef = TypedDict(
    "CreateBackupSelectionOutputTypeDef",
    {
        "SelectionId": str,
        "BackupPlanId": str,
        "CreationDate": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateBackupVaultOutputTypeDef = TypedDict(
    "CreateBackupVaultOutputTypeDef",
    {
        "BackupVaultName": str,
        "BackupVaultArn": str,
        "CreationDate": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateFrameworkOutputTypeDef = TypedDict(
    "CreateFrameworkOutputTypeDef",
    {
        "FrameworkName": str,
        "FrameworkArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateLogicallyAirGappedBackupVaultOutputTypeDef = TypedDict(
    "CreateLogicallyAirGappedBackupVaultOutputTypeDef",
    {
        "BackupVaultName": str,
        "BackupVaultArn": str,
        "CreationDate": datetime,
        "VaultState": VaultStateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateReportPlanOutputTypeDef = TypedDict(
    "CreateReportPlanOutputTypeDef",
    {
        "ReportPlanName": str,
        "ReportPlanArn": str,
        "CreationTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteBackupPlanOutputTypeDef = TypedDict(
    "DeleteBackupPlanOutputTypeDef",
    {
        "BackupPlanId": str,
        "BackupPlanArn": str,
        "DeletionDate": datetime,
        "VersionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeBackupJobOutputTypeDef = TypedDict(
    "DescribeBackupJobOutputTypeDef",
    {
        "AccountId": str,
        "BackupJobId": str,
        "BackupVaultName": str,
        "BackupVaultArn": str,
        "RecoveryPointArn": str,
        "ResourceArn": str,
        "CreationDate": datetime,
        "CompletionDate": datetime,
        "State": BackupJobStateType,
        "StatusMessage": str,
        "PercentDone": str,
        "BackupSizeInBytes": int,
        "IamRoleArn": str,
        "CreatedBy": RecoveryPointCreatorTypeDef,
        "ResourceType": str,
        "BytesTransferred": int,
        "ExpectedCompletionDate": datetime,
        "StartBy": datetime,
        "BackupOptions": Dict[str, str],
        "BackupType": str,
        "ParentJobId": str,
        "IsParent": bool,
        "NumberOfChildJobs": int,
        "ChildJobsInState": Dict[BackupJobStateType, int],
        "ResourceName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeBackupVaultOutputTypeDef = TypedDict(
    "DescribeBackupVaultOutputTypeDef",
    {
        "BackupVaultName": str,
        "BackupVaultArn": str,
        "VaultType": VaultTypeType,
        "EncryptionKeyArn": str,
        "CreationDate": datetime,
        "CreatorRequestId": str,
        "NumberOfRecoveryPoints": int,
        "Locked": bool,
        "MinRetentionDays": int,
        "MaxRetentionDays": int,
        "LockDate": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeGlobalSettingsOutputTypeDef = TypedDict(
    "DescribeGlobalSettingsOutputTypeDef",
    {
        "GlobalSettings": Dict[str, str],
        "LastUpdateTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeProtectedResourceOutputTypeDef = TypedDict(
    "DescribeProtectedResourceOutputTypeDef",
    {
        "ResourceArn": str,
        "ResourceType": str,
        "LastBackupTime": datetime,
        "ResourceName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeRecoveryPointOutputTypeDef = TypedDict(
    "DescribeRecoveryPointOutputTypeDef",
    {
        "RecoveryPointArn": str,
        "BackupVaultName": str,
        "BackupVaultArn": str,
        "SourceBackupVaultArn": str,
        "ResourceArn": str,
        "ResourceType": str,
        "CreatedBy": RecoveryPointCreatorTypeDef,
        "IamRoleArn": str,
        "Status": RecoveryPointStatusType,
        "StatusMessage": str,
        "CreationDate": datetime,
        "CompletionDate": datetime,
        "BackupSizeInBytes": int,
        "CalculatedLifecycle": CalculatedLifecycleTypeDef,
        "Lifecycle": LifecycleTypeDef,
        "EncryptionKeyArn": str,
        "IsEncrypted": bool,
        "StorageClass": StorageClassType,
        "LastRestoreTime": datetime,
        "ParentRecoveryPointArn": str,
        "CompositeMemberIdentifier": str,
        "IsParent": bool,
        "ResourceName": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeRegionSettingsOutputTypeDef = TypedDict(
    "DescribeRegionSettingsOutputTypeDef",
    {
        "ResourceTypeOptInPreference": Dict[str, bool],
        "ResourceTypeManagementPreference": Dict[str, bool],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeRestoreJobOutputTypeDef = TypedDict(
    "DescribeRestoreJobOutputTypeDef",
    {
        "AccountId": str,
        "RestoreJobId": str,
        "RecoveryPointArn": str,
        "CreationDate": datetime,
        "CompletionDate": datetime,
        "Status": RestoreJobStatusType,
        "StatusMessage": str,
        "PercentDone": str,
        "BackupSizeInBytes": int,
        "IamRoleArn": str,
        "ExpectedCompletionTimeMinutes": int,
        "CreatedResourceArn": str,
        "ResourceType": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ExportBackupPlanTemplateOutputTypeDef = TypedDict(
    "ExportBackupPlanTemplateOutputTypeDef",
    {
        "BackupPlanTemplateJson": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetBackupVaultAccessPolicyOutputTypeDef = TypedDict(
    "GetBackupVaultAccessPolicyOutputTypeDef",
    {
        "BackupVaultName": str,
        "BackupVaultArn": str,
        "Policy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetBackupVaultNotificationsOutputTypeDef = TypedDict(
    "GetBackupVaultNotificationsOutputTypeDef",
    {
        "BackupVaultName": str,
        "BackupVaultArn": str,
        "SNSTopicArn": str,
        "BackupVaultEvents": List[BackupVaultEventType],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetRecoveryPointRestoreMetadataOutputTypeDef = TypedDict(
    "GetRecoveryPointRestoreMetadataOutputTypeDef",
    {
        "BackupVaultArn": str,
        "RecoveryPointArn": str,
        "RestoreMetadata": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSupportedResourceTypesOutputTypeDef = TypedDict(
    "GetSupportedResourceTypesOutputTypeDef",
    {
        "ResourceTypes": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListBackupPlanTemplatesOutputTypeDef = TypedDict(
    "ListBackupPlanTemplatesOutputTypeDef",
    {
        "NextToken": str,
        "BackupPlanTemplatesList": List[BackupPlanTemplatesListMemberTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListBackupSelectionsOutputTypeDef = TypedDict(
    "ListBackupSelectionsOutputTypeDef",
    {
        "NextToken": str,
        "BackupSelectionsList": List[BackupSelectionsListMemberTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListBackupVaultsOutputTypeDef = TypedDict(
    "ListBackupVaultsOutputTypeDef",
    {
        "BackupVaultList": List[BackupVaultListMemberTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsOutputTypeDef = TypedDict(
    "ListTagsOutputTypeDef",
    {
        "NextToken": str,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartBackupJobOutputTypeDef = TypedDict(
    "StartBackupJobOutputTypeDef",
    {
        "BackupJobId": str,
        "RecoveryPointArn": str,
        "CreationDate": datetime,
        "IsParent": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartCopyJobOutputTypeDef = TypedDict(
    "StartCopyJobOutputTypeDef",
    {
        "CopyJobId": str,
        "CreationDate": datetime,
        "IsParent": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartReportJobOutputTypeDef = TypedDict(
    "StartReportJobOutputTypeDef",
    {
        "ReportJobId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartRestoreJobOutputTypeDef = TypedDict(
    "StartRestoreJobOutputTypeDef",
    {
        "RestoreJobId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateBackupPlanOutputTypeDef = TypedDict(
    "UpdateBackupPlanOutputTypeDef",
    {
        "BackupPlanId": str,
        "BackupPlanArn": str,
        "CreationDate": datetime,
        "VersionId": str,
        "AdvancedBackupSettings": List[AdvancedBackupSettingTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateFrameworkOutputTypeDef = TypedDict(
    "UpdateFrameworkOutputTypeDef",
    {
        "FrameworkName": str,
        "FrameworkArn": str,
        "CreationTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateRecoveryPointLifecycleOutputTypeDef = TypedDict(
    "UpdateRecoveryPointLifecycleOutputTypeDef",
    {
        "BackupVaultArn": str,
        "RecoveryPointArn": str,
        "Lifecycle": LifecycleTypeDef,
        "CalculatedLifecycle": CalculatedLifecycleTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateReportPlanOutputTypeDef = TypedDict(
    "UpdateReportPlanOutputTypeDef",
    {
        "ReportPlanName": str,
        "ReportPlanArn": str,
        "CreationTime": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateReportPlanInputRequestTypeDef = TypedDict(
    "CreateReportPlanInputRequestTypeDef",
    {
        "ReportPlanName": str,
        "ReportDeliveryChannel": ReportDeliveryChannelTypeDef,
        "ReportSetting": ReportSettingTypeDef,
        "ReportPlanDescription": NotRequired[str],
        "ReportPlanTags": NotRequired[Mapping[str, str]],
        "IdempotencyToken": NotRequired[str],
    },
)

ReportPlanTypeDef = TypedDict(
    "ReportPlanTypeDef",
    {
        "ReportPlanArn": NotRequired[str],
        "ReportPlanName": NotRequired[str],
        "ReportPlanDescription": NotRequired[str],
        "ReportSetting": NotRequired[ReportSettingTypeDef],
        "ReportDeliveryChannel": NotRequired[ReportDeliveryChannelTypeDef],
        "DeploymentStatus": NotRequired[str],
        "CreationTime": NotRequired[datetime],
        "LastAttemptedExecutionTime": NotRequired[datetime],
        "LastSuccessfulExecutionTime": NotRequired[datetime],
    },
)

UpdateReportPlanInputRequestTypeDef = TypedDict(
    "UpdateReportPlanInputRequestTypeDef",
    {
        "ReportPlanName": str,
        "ReportPlanDescription": NotRequired[str],
        "ReportDeliveryChannel": NotRequired[ReportDeliveryChannelTypeDef],
        "ReportSetting": NotRequired[ReportSettingTypeDef],
        "IdempotencyToken": NotRequired[str],
    },
)

DateRangeTypeDef = TypedDict(
    "DateRangeTypeDef",
    {
        "FromDate": TimestampTypeDef,
        "ToDate": TimestampTypeDef,
    },
)

ListBackupJobsInputRequestTypeDef = TypedDict(
    "ListBackupJobsInputRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
        "ByResourceArn": NotRequired[str],
        "ByState": NotRequired[BackupJobStateType],
        "ByBackupVaultName": NotRequired[str],
        "ByCreatedBefore": NotRequired[TimestampTypeDef],
        "ByCreatedAfter": NotRequired[TimestampTypeDef],
        "ByResourceType": NotRequired[str],
        "ByAccountId": NotRequired[str],
        "ByCompleteAfter": NotRequired[TimestampTypeDef],
        "ByCompleteBefore": NotRequired[TimestampTypeDef],
        "ByParentJobId": NotRequired[str],
    },
)

ListCopyJobsInputRequestTypeDef = TypedDict(
    "ListCopyJobsInputRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
        "ByResourceArn": NotRequired[str],
        "ByState": NotRequired[CopyJobStateType],
        "ByCreatedBefore": NotRequired[TimestampTypeDef],
        "ByCreatedAfter": NotRequired[TimestampTypeDef],
        "ByResourceType": NotRequired[str],
        "ByDestinationVaultArn": NotRequired[str],
        "ByAccountId": NotRequired[str],
        "ByCompleteBefore": NotRequired[TimestampTypeDef],
        "ByCompleteAfter": NotRequired[TimestampTypeDef],
        "ByParentJobId": NotRequired[str],
    },
)

ListRecoveryPointsByBackupVaultInputRequestTypeDef = TypedDict(
    "ListRecoveryPointsByBackupVaultInputRequestTypeDef",
    {
        "BackupVaultName": str,
        "BackupVaultAccountId": NotRequired[str],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
        "ByResourceArn": NotRequired[str],
        "ByResourceType": NotRequired[str],
        "ByBackupPlanId": NotRequired[str],
        "ByCreatedBefore": NotRequired[TimestampTypeDef],
        "ByCreatedAfter": NotRequired[TimestampTypeDef],
        "ByParentRecoveryPointArn": NotRequired[str],
    },
)

ListReportJobsInputRequestTypeDef = TypedDict(
    "ListReportJobsInputRequestTypeDef",
    {
        "ByReportPlanName": NotRequired[str],
        "ByCreationBefore": NotRequired[TimestampTypeDef],
        "ByCreationAfter": NotRequired[TimestampTypeDef],
        "ByStatus": NotRequired[str],
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

ListRestoreJobsInputRequestTypeDef = TypedDict(
    "ListRestoreJobsInputRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
        "ByAccountId": NotRequired[str],
        "ByCreatedBefore": NotRequired[TimestampTypeDef],
        "ByCreatedAfter": NotRequired[TimestampTypeDef],
        "ByStatus": NotRequired[RestoreJobStatusType],
        "ByCompleteBefore": NotRequired[TimestampTypeDef],
        "ByCompleteAfter": NotRequired[TimestampTypeDef],
    },
)

ListFrameworksOutputTypeDef = TypedDict(
    "ListFrameworksOutputTypeDef",
    {
        "Frameworks": List[FrameworkTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListLegalHoldsOutputTypeDef = TypedDict(
    "ListLegalHoldsOutputTypeDef",
    {
        "NextToken": str,
        "LegalHolds": List[LegalHoldTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListBackupJobsInputListBackupJobsPaginateTypeDef = TypedDict(
    "ListBackupJobsInputListBackupJobsPaginateTypeDef",
    {
        "ByResourceArn": NotRequired[str],
        "ByState": NotRequired[BackupJobStateType],
        "ByBackupVaultName": NotRequired[str],
        "ByCreatedBefore": NotRequired[TimestampTypeDef],
        "ByCreatedAfter": NotRequired[TimestampTypeDef],
        "ByResourceType": NotRequired[str],
        "ByAccountId": NotRequired[str],
        "ByCompleteAfter": NotRequired[TimestampTypeDef],
        "ByCompleteBefore": NotRequired[TimestampTypeDef],
        "ByParentJobId": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListBackupPlanTemplatesInputListBackupPlanTemplatesPaginateTypeDef = TypedDict(
    "ListBackupPlanTemplatesInputListBackupPlanTemplatesPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListBackupPlanVersionsInputListBackupPlanVersionsPaginateTypeDef = TypedDict(
    "ListBackupPlanVersionsInputListBackupPlanVersionsPaginateTypeDef",
    {
        "BackupPlanId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListBackupPlansInputListBackupPlansPaginateTypeDef = TypedDict(
    "ListBackupPlansInputListBackupPlansPaginateTypeDef",
    {
        "IncludeDeleted": NotRequired[bool],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListBackupSelectionsInputListBackupSelectionsPaginateTypeDef = TypedDict(
    "ListBackupSelectionsInputListBackupSelectionsPaginateTypeDef",
    {
        "BackupPlanId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListBackupVaultsInputListBackupVaultsPaginateTypeDef = TypedDict(
    "ListBackupVaultsInputListBackupVaultsPaginateTypeDef",
    {
        "ByVaultType": NotRequired[VaultTypeType],
        "ByShared": NotRequired[bool],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListCopyJobsInputListCopyJobsPaginateTypeDef = TypedDict(
    "ListCopyJobsInputListCopyJobsPaginateTypeDef",
    {
        "ByResourceArn": NotRequired[str],
        "ByState": NotRequired[CopyJobStateType],
        "ByCreatedBefore": NotRequired[TimestampTypeDef],
        "ByCreatedAfter": NotRequired[TimestampTypeDef],
        "ByResourceType": NotRequired[str],
        "ByDestinationVaultArn": NotRequired[str],
        "ByAccountId": NotRequired[str],
        "ByCompleteBefore": NotRequired[TimestampTypeDef],
        "ByCompleteAfter": NotRequired[TimestampTypeDef],
        "ByParentJobId": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListLegalHoldsInputListLegalHoldsPaginateTypeDef = TypedDict(
    "ListLegalHoldsInputListLegalHoldsPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListProtectedResourcesByBackupVaultInputListProtectedResourcesByBackupVaultPaginateTypeDef = TypedDict(
    "ListProtectedResourcesByBackupVaultInputListProtectedResourcesByBackupVaultPaginateTypeDef",
    {
        "BackupVaultName": str,
        "BackupVaultAccountId": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListProtectedResourcesInputListProtectedResourcesPaginateTypeDef = TypedDict(
    "ListProtectedResourcesInputListProtectedResourcesPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListRecoveryPointsByBackupVaultInputListRecoveryPointsByBackupVaultPaginateTypeDef = TypedDict(
    "ListRecoveryPointsByBackupVaultInputListRecoveryPointsByBackupVaultPaginateTypeDef",
    {
        "BackupVaultName": str,
        "BackupVaultAccountId": NotRequired[str],
        "ByResourceArn": NotRequired[str],
        "ByResourceType": NotRequired[str],
        "ByBackupPlanId": NotRequired[str],
        "ByCreatedBefore": NotRequired[TimestampTypeDef],
        "ByCreatedAfter": NotRequired[TimestampTypeDef],
        "ByParentRecoveryPointArn": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListRecoveryPointsByLegalHoldInputListRecoveryPointsByLegalHoldPaginateTypeDef = TypedDict(
    "ListRecoveryPointsByLegalHoldInputListRecoveryPointsByLegalHoldPaginateTypeDef",
    {
        "LegalHoldId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListRecoveryPointsByResourceInputListRecoveryPointsByResourcePaginateTypeDef = TypedDict(
    "ListRecoveryPointsByResourceInputListRecoveryPointsByResourcePaginateTypeDef",
    {
        "ResourceArn": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListRestoreJobsInputListRestoreJobsPaginateTypeDef = TypedDict(
    "ListRestoreJobsInputListRestoreJobsPaginateTypeDef",
    {
        "ByAccountId": NotRequired[str],
        "ByCreatedBefore": NotRequired[TimestampTypeDef],
        "ByCreatedAfter": NotRequired[TimestampTypeDef],
        "ByStatus": NotRequired[RestoreJobStatusType],
        "ByCompleteBefore": NotRequired[TimestampTypeDef],
        "ByCompleteAfter": NotRequired[TimestampTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListProtectedResourcesByBackupVaultOutputTypeDef = TypedDict(
    "ListProtectedResourcesByBackupVaultOutputTypeDef",
    {
        "Results": List[ProtectedResourceTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListProtectedResourcesOutputTypeDef = TypedDict(
    "ListProtectedResourcesOutputTypeDef",
    {
        "Results": List[ProtectedResourceTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRecoveryPointsByLegalHoldOutputTypeDef = TypedDict(
    "ListRecoveryPointsByLegalHoldOutputTypeDef",
    {
        "RecoveryPoints": List[RecoveryPointMemberTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRecoveryPointsByResourceOutputTypeDef = TypedDict(
    "ListRecoveryPointsByResourceOutputTypeDef",
    {
        "NextToken": str,
        "RecoveryPoints": List[RecoveryPointByResourceTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRestoreJobsOutputTypeDef = TypedDict(
    "ListRestoreJobsOutputTypeDef",
    {
        "RestoreJobs": List[RestoreJobsListMemberTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ReportJobTypeDef = TypedDict(
    "ReportJobTypeDef",
    {
        "ReportJobId": NotRequired[str],
        "ReportPlanArn": NotRequired[str],
        "ReportTemplate": NotRequired[str],
        "CreationTime": NotRequired[datetime],
        "CompletionTime": NotRequired[datetime],
        "Status": NotRequired[str],
        "StatusMessage": NotRequired[str],
        "ReportDestination": NotRequired[ReportDestinationTypeDef],
    },
)

ListBackupPlanVersionsOutputPaginatorTypeDef = TypedDict(
    "ListBackupPlanVersionsOutputPaginatorTypeDef",
    {
        "NextToken": str,
        "BackupPlanVersionsList": List[BackupPlansListMemberPaginatorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListBackupPlansOutputPaginatorTypeDef = TypedDict(
    "ListBackupPlansOutputPaginatorTypeDef",
    {
        "NextToken": str,
        "BackupPlansList": List[BackupPlansListMemberPaginatorTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListBackupPlanVersionsOutputTypeDef = TypedDict(
    "ListBackupPlanVersionsOutputTypeDef",
    {
        "NextToken": str,
        "BackupPlanVersionsList": List[BackupPlansListMemberTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListBackupPlansOutputTypeDef = TypedDict(
    "ListBackupPlansOutputTypeDef",
    {
        "NextToken": str,
        "BackupPlansList": List[BackupPlansListMemberTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListBackupJobsOutputTypeDef = TypedDict(
    "ListBackupJobsOutputTypeDef",
    {
        "BackupJobs": List[BackupJobTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeCopyJobOutputTypeDef = TypedDict(
    "DescribeCopyJobOutputTypeDef",
    {
        "CopyJob": CopyJobTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListCopyJobsOutputTypeDef = TypedDict(
    "ListCopyJobsOutputTypeDef",
    {
        "CopyJobs": List[CopyJobTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BackupRuleInputTypeDef = TypedDict(
    "BackupRuleInputTypeDef",
    {
        "RuleName": str,
        "TargetBackupVaultName": str,
        "ScheduleExpression": NotRequired[str],
        "StartWindowMinutes": NotRequired[int],
        "CompletionWindowMinutes": NotRequired[int],
        "Lifecycle": NotRequired[LifecycleTypeDef],
        "RecoveryPointTags": NotRequired[Mapping[str, str]],
        "CopyActions": NotRequired[Sequence[CopyActionTypeDef]],
        "EnableContinuousBackup": NotRequired[bool],
        "ScheduleExpressionTimezone": NotRequired[str],
    },
)

BackupRuleTypeDef = TypedDict(
    "BackupRuleTypeDef",
    {
        "RuleName": str,
        "TargetBackupVaultName": str,
        "ScheduleExpression": NotRequired[str],
        "StartWindowMinutes": NotRequired[int],
        "CompletionWindowMinutes": NotRequired[int],
        "Lifecycle": NotRequired[LifecycleTypeDef],
        "RecoveryPointTags": NotRequired[Dict[str, str]],
        "RuleId": NotRequired[str],
        "CopyActions": NotRequired[List[CopyActionTypeDef]],
        "EnableContinuousBackup": NotRequired[bool],
        "ScheduleExpressionTimezone": NotRequired[str],
    },
)

ListRecoveryPointsByBackupVaultOutputTypeDef = TypedDict(
    "ListRecoveryPointsByBackupVaultOutputTypeDef",
    {
        "NextToken": str,
        "RecoveryPoints": List[RecoveryPointByBackupVaultTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BackupSelectionTypeDef = TypedDict(
    "BackupSelectionTypeDef",
    {
        "SelectionName": str,
        "IamRoleArn": str,
        "Resources": NotRequired[Sequence[str]],
        "ListOfTags": NotRequired[Sequence[ConditionTypeDef]],
        "NotResources": NotRequired[Sequence[str]],
        "Conditions": NotRequired[ConditionsTypeDef],
    },
)

CreateFrameworkInputRequestTypeDef = TypedDict(
    "CreateFrameworkInputRequestTypeDef",
    {
        "FrameworkName": str,
        "FrameworkControls": Sequence[FrameworkControlTypeDef],
        "FrameworkDescription": NotRequired[str],
        "IdempotencyToken": NotRequired[str],
        "FrameworkTags": NotRequired[Mapping[str, str]],
    },
)

DescribeFrameworkOutputTypeDef = TypedDict(
    "DescribeFrameworkOutputTypeDef",
    {
        "FrameworkName": str,
        "FrameworkArn": str,
        "FrameworkDescription": str,
        "FrameworkControls": List[FrameworkControlTypeDef],
        "CreationTime": datetime,
        "DeploymentStatus": str,
        "FrameworkStatus": str,
        "IdempotencyToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateFrameworkInputRequestTypeDef = TypedDict(
    "UpdateFrameworkInputRequestTypeDef",
    {
        "FrameworkName": str,
        "FrameworkDescription": NotRequired[str],
        "FrameworkControls": NotRequired[Sequence[FrameworkControlTypeDef]],
        "IdempotencyToken": NotRequired[str],
    },
)

DescribeReportPlanOutputTypeDef = TypedDict(
    "DescribeReportPlanOutputTypeDef",
    {
        "ReportPlan": ReportPlanTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListReportPlansOutputTypeDef = TypedDict(
    "ListReportPlansOutputTypeDef",
    {
        "ReportPlans": List[ReportPlanTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RecoveryPointSelectionTypeDef = TypedDict(
    "RecoveryPointSelectionTypeDef",
    {
        "VaultNames": NotRequired[Sequence[str]],
        "ResourceIdentifiers": NotRequired[Sequence[str]],
        "DateRange": NotRequired[DateRangeTypeDef],
    },
)

DescribeReportJobOutputTypeDef = TypedDict(
    "DescribeReportJobOutputTypeDef",
    {
        "ReportJob": ReportJobTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListReportJobsOutputTypeDef = TypedDict(
    "ListReportJobsOutputTypeDef",
    {
        "ReportJobs": List[ReportJobTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BackupPlanInputTypeDef = TypedDict(
    "BackupPlanInputTypeDef",
    {
        "BackupPlanName": str,
        "Rules": Sequence[BackupRuleInputTypeDef],
        "AdvancedBackupSettings": NotRequired[Sequence[AdvancedBackupSettingTypeDef]],
    },
)

BackupPlanTypeDef = TypedDict(
    "BackupPlanTypeDef",
    {
        "BackupPlanName": str,
        "Rules": List[BackupRuleTypeDef],
        "AdvancedBackupSettings": NotRequired[List[AdvancedBackupSettingTypeDef]],
    },
)

CreateBackupSelectionInputRequestTypeDef = TypedDict(
    "CreateBackupSelectionInputRequestTypeDef",
    {
        "BackupPlanId": str,
        "BackupSelection": BackupSelectionTypeDef,
        "CreatorRequestId": NotRequired[str],
    },
)

GetBackupSelectionOutputTypeDef = TypedDict(
    "GetBackupSelectionOutputTypeDef",
    {
        "BackupSelection": BackupSelectionTypeDef,
        "SelectionId": str,
        "BackupPlanId": str,
        "CreationDate": datetime,
        "CreatorRequestId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateLegalHoldInputRequestTypeDef = TypedDict(
    "CreateLegalHoldInputRequestTypeDef",
    {
        "Title": str,
        "Description": str,
        "IdempotencyToken": NotRequired[str],
        "RecoveryPointSelection": NotRequired[RecoveryPointSelectionTypeDef],
        "Tags": NotRequired[Mapping[str, str]],
    },
)

CreateLegalHoldOutputTypeDef = TypedDict(
    "CreateLegalHoldOutputTypeDef",
    {
        "Title": str,
        "Status": LegalHoldStatusType,
        "Description": str,
        "LegalHoldId": str,
        "LegalHoldArn": str,
        "CreationDate": datetime,
        "RecoveryPointSelection": RecoveryPointSelectionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetLegalHoldOutputTypeDef = TypedDict(
    "GetLegalHoldOutputTypeDef",
    {
        "Title": str,
        "Status": LegalHoldStatusType,
        "Description": str,
        "CancelDescription": str,
        "LegalHoldId": str,
        "LegalHoldArn": str,
        "CreationDate": datetime,
        "CancellationDate": datetime,
        "RetainRecordUntil": datetime,
        "RecoveryPointSelection": RecoveryPointSelectionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateBackupPlanInputRequestTypeDef = TypedDict(
    "CreateBackupPlanInputRequestTypeDef",
    {
        "BackupPlan": BackupPlanInputTypeDef,
        "BackupPlanTags": NotRequired[Mapping[str, str]],
        "CreatorRequestId": NotRequired[str],
    },
)

UpdateBackupPlanInputRequestTypeDef = TypedDict(
    "UpdateBackupPlanInputRequestTypeDef",
    {
        "BackupPlanId": str,
        "BackupPlan": BackupPlanInputTypeDef,
    },
)

GetBackupPlanFromJSONOutputTypeDef = TypedDict(
    "GetBackupPlanFromJSONOutputTypeDef",
    {
        "BackupPlan": BackupPlanTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetBackupPlanFromTemplateOutputTypeDef = TypedDict(
    "GetBackupPlanFromTemplateOutputTypeDef",
    {
        "BackupPlanDocument": BackupPlanTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetBackupPlanOutputTypeDef = TypedDict(
    "GetBackupPlanOutputTypeDef",
    {
        "BackupPlan": BackupPlanTypeDef,
        "BackupPlanId": str,
        "BackupPlanArn": str,
        "VersionId": str,
        "CreatorRequestId": str,
        "CreationDate": datetime,
        "DeletionDate": datetime,
        "LastExecutionDate": datetime,
        "AdvancedBackupSettings": List[AdvancedBackupSettingTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
