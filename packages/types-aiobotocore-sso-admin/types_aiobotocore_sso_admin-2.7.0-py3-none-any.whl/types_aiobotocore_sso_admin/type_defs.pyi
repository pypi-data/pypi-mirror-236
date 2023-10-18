"""
Type annotations for sso-admin service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/type_defs/)

Usage::

    ```python
    from types_aiobotocore_sso_admin.type_defs import AccessControlAttributeValueTypeDef

    data: AccessControlAttributeValueTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import (
    InstanceAccessControlAttributeConfigurationStatusType,
    PrincipalTypeType,
    ProvisioningStatusType,
    ProvisionTargetTypeType,
    StatusValuesType,
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
    "AccessControlAttributeValueTypeDef",
    "AccountAssignmentOperationStatusMetadataTypeDef",
    "AccountAssignmentOperationStatusTypeDef",
    "AccountAssignmentTypeDef",
    "CustomerManagedPolicyReferenceTypeDef",
    "AttachManagedPolicyToPermissionSetRequestRequestTypeDef",
    "AttachedManagedPolicyTypeDef",
    "CreateAccountAssignmentRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "TagTypeDef",
    "PermissionSetTypeDef",
    "DeleteAccountAssignmentRequestRequestTypeDef",
    "DeleteInlinePolicyFromPermissionSetRequestRequestTypeDef",
    "DeleteInstanceAccessControlAttributeConfigurationRequestRequestTypeDef",
    "DeletePermissionSetRequestRequestTypeDef",
    "DeletePermissionsBoundaryFromPermissionSetRequestRequestTypeDef",
    "DescribeAccountAssignmentCreationStatusRequestRequestTypeDef",
    "DescribeAccountAssignmentDeletionStatusRequestRequestTypeDef",
    "DescribeInstanceAccessControlAttributeConfigurationRequestRequestTypeDef",
    "DescribePermissionSetProvisioningStatusRequestRequestTypeDef",
    "PermissionSetProvisioningStatusTypeDef",
    "DescribePermissionSetRequestRequestTypeDef",
    "DetachManagedPolicyFromPermissionSetRequestRequestTypeDef",
    "GetInlinePolicyForPermissionSetRequestRequestTypeDef",
    "GetPermissionsBoundaryForPermissionSetRequestRequestTypeDef",
    "InstanceMetadataTypeDef",
    "OperationStatusFilterTypeDef",
    "PaginatorConfigTypeDef",
    "ListAccountAssignmentsRequestRequestTypeDef",
    "ListAccountsForProvisionedPermissionSetRequestRequestTypeDef",
    "ListCustomerManagedPolicyReferencesInPermissionSetRequestRequestTypeDef",
    "ListInstancesRequestRequestTypeDef",
    "ListManagedPoliciesInPermissionSetRequestRequestTypeDef",
    "PermissionSetProvisioningStatusMetadataTypeDef",
    "ListPermissionSetsProvisionedToAccountRequestRequestTypeDef",
    "ListPermissionSetsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ProvisionPermissionSetRequestRequestTypeDef",
    "PutInlinePolicyToPermissionSetRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdatePermissionSetRequestRequestTypeDef",
    "AccessControlAttributeTypeDef",
    "AttachCustomerManagedPolicyReferenceToPermissionSetRequestRequestTypeDef",
    "DetachCustomerManagedPolicyReferenceFromPermissionSetRequestRequestTypeDef",
    "PermissionsBoundaryTypeDef",
    "CreateAccountAssignmentResponseTypeDef",
    "DeleteAccountAssignmentResponseTypeDef",
    "DescribeAccountAssignmentCreationStatusResponseTypeDef",
    "DescribeAccountAssignmentDeletionStatusResponseTypeDef",
    "GetInlinePolicyForPermissionSetResponseTypeDef",
    "ListAccountAssignmentCreationStatusResponseTypeDef",
    "ListAccountAssignmentDeletionStatusResponseTypeDef",
    "ListAccountAssignmentsResponseTypeDef",
    "ListAccountsForProvisionedPermissionSetResponseTypeDef",
    "ListCustomerManagedPolicyReferencesInPermissionSetResponseTypeDef",
    "ListManagedPoliciesInPermissionSetResponseTypeDef",
    "ListPermissionSetsProvisionedToAccountResponseTypeDef",
    "ListPermissionSetsResponseTypeDef",
    "CreatePermissionSetRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CreatePermissionSetResponseTypeDef",
    "DescribePermissionSetResponseTypeDef",
    "DescribePermissionSetProvisioningStatusResponseTypeDef",
    "ProvisionPermissionSetResponseTypeDef",
    "ListInstancesResponseTypeDef",
    "ListAccountAssignmentCreationStatusRequestRequestTypeDef",
    "ListAccountAssignmentDeletionStatusRequestRequestTypeDef",
    "ListPermissionSetProvisioningStatusRequestRequestTypeDef",
    "ListAccountAssignmentCreationStatusRequestListAccountAssignmentCreationStatusPaginateTypeDef",
    "ListAccountAssignmentDeletionStatusRequestListAccountAssignmentDeletionStatusPaginateTypeDef",
    "ListAccountAssignmentsRequestListAccountAssignmentsPaginateTypeDef",
    "ListAccountsForProvisionedPermissionSetRequestListAccountsForProvisionedPermissionSetPaginateTypeDef",
    "ListCustomerManagedPolicyReferencesInPermissionSetRequestListCustomerManagedPolicyReferencesInPermissionSetPaginateTypeDef",
    "ListInstancesRequestListInstancesPaginateTypeDef",
    "ListManagedPoliciesInPermissionSetRequestListManagedPoliciesInPermissionSetPaginateTypeDef",
    "ListPermissionSetProvisioningStatusRequestListPermissionSetProvisioningStatusPaginateTypeDef",
    "ListPermissionSetsProvisionedToAccountRequestListPermissionSetsProvisionedToAccountPaginateTypeDef",
    "ListPermissionSetsRequestListPermissionSetsPaginateTypeDef",
    "ListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    "ListPermissionSetProvisioningStatusResponseTypeDef",
    "InstanceAccessControlAttributeConfigurationTypeDef",
    "GetPermissionsBoundaryForPermissionSetResponseTypeDef",
    "PutPermissionsBoundaryToPermissionSetRequestRequestTypeDef",
    "CreateInstanceAccessControlAttributeConfigurationRequestRequestTypeDef",
    "DescribeInstanceAccessControlAttributeConfigurationResponseTypeDef",
    "UpdateInstanceAccessControlAttributeConfigurationRequestRequestTypeDef",
)

AccessControlAttributeValueTypeDef = TypedDict(
    "AccessControlAttributeValueTypeDef",
    {
        "Source": Sequence[str],
    },
)

AccountAssignmentOperationStatusMetadataTypeDef = TypedDict(
    "AccountAssignmentOperationStatusMetadataTypeDef",
    {
        "CreatedDate": NotRequired[datetime],
        "RequestId": NotRequired[str],
        "Status": NotRequired[StatusValuesType],
    },
)

AccountAssignmentOperationStatusTypeDef = TypedDict(
    "AccountAssignmentOperationStatusTypeDef",
    {
        "CreatedDate": NotRequired[datetime],
        "FailureReason": NotRequired[str],
        "PermissionSetArn": NotRequired[str],
        "PrincipalId": NotRequired[str],
        "PrincipalType": NotRequired[PrincipalTypeType],
        "RequestId": NotRequired[str],
        "Status": NotRequired[StatusValuesType],
        "TargetId": NotRequired[str],
        "TargetType": NotRequired[Literal["AWS_ACCOUNT"]],
    },
)

AccountAssignmentTypeDef = TypedDict(
    "AccountAssignmentTypeDef",
    {
        "AccountId": NotRequired[str],
        "PermissionSetArn": NotRequired[str],
        "PrincipalId": NotRequired[str],
        "PrincipalType": NotRequired[PrincipalTypeType],
    },
)

CustomerManagedPolicyReferenceTypeDef = TypedDict(
    "CustomerManagedPolicyReferenceTypeDef",
    {
        "Name": str,
        "Path": NotRequired[str],
    },
)

AttachManagedPolicyToPermissionSetRequestRequestTypeDef = TypedDict(
    "AttachManagedPolicyToPermissionSetRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "ManagedPolicyArn": str,
        "PermissionSetArn": str,
    },
)

AttachedManagedPolicyTypeDef = TypedDict(
    "AttachedManagedPolicyTypeDef",
    {
        "Arn": NotRequired[str],
        "Name": NotRequired[str],
    },
)

CreateAccountAssignmentRequestRequestTypeDef = TypedDict(
    "CreateAccountAssignmentRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "PermissionSetArn": str,
        "PrincipalId": str,
        "PrincipalType": PrincipalTypeType,
        "TargetId": str,
        "TargetType": Literal["AWS_ACCOUNT"],
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

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

PermissionSetTypeDef = TypedDict(
    "PermissionSetTypeDef",
    {
        "CreatedDate": NotRequired[datetime],
        "Description": NotRequired[str],
        "Name": NotRequired[str],
        "PermissionSetArn": NotRequired[str],
        "RelayState": NotRequired[str],
        "SessionDuration": NotRequired[str],
    },
)

DeleteAccountAssignmentRequestRequestTypeDef = TypedDict(
    "DeleteAccountAssignmentRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "PermissionSetArn": str,
        "PrincipalId": str,
        "PrincipalType": PrincipalTypeType,
        "TargetId": str,
        "TargetType": Literal["AWS_ACCOUNT"],
    },
)

DeleteInlinePolicyFromPermissionSetRequestRequestTypeDef = TypedDict(
    "DeleteInlinePolicyFromPermissionSetRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "PermissionSetArn": str,
    },
)

DeleteInstanceAccessControlAttributeConfigurationRequestRequestTypeDef = TypedDict(
    "DeleteInstanceAccessControlAttributeConfigurationRequestRequestTypeDef",
    {
        "InstanceArn": str,
    },
)

DeletePermissionSetRequestRequestTypeDef = TypedDict(
    "DeletePermissionSetRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "PermissionSetArn": str,
    },
)

DeletePermissionsBoundaryFromPermissionSetRequestRequestTypeDef = TypedDict(
    "DeletePermissionsBoundaryFromPermissionSetRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "PermissionSetArn": str,
    },
)

DescribeAccountAssignmentCreationStatusRequestRequestTypeDef = TypedDict(
    "DescribeAccountAssignmentCreationStatusRequestRequestTypeDef",
    {
        "AccountAssignmentCreationRequestId": str,
        "InstanceArn": str,
    },
)

DescribeAccountAssignmentDeletionStatusRequestRequestTypeDef = TypedDict(
    "DescribeAccountAssignmentDeletionStatusRequestRequestTypeDef",
    {
        "AccountAssignmentDeletionRequestId": str,
        "InstanceArn": str,
    },
)

DescribeInstanceAccessControlAttributeConfigurationRequestRequestTypeDef = TypedDict(
    "DescribeInstanceAccessControlAttributeConfigurationRequestRequestTypeDef",
    {
        "InstanceArn": str,
    },
)

DescribePermissionSetProvisioningStatusRequestRequestTypeDef = TypedDict(
    "DescribePermissionSetProvisioningStatusRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "ProvisionPermissionSetRequestId": str,
    },
)

PermissionSetProvisioningStatusTypeDef = TypedDict(
    "PermissionSetProvisioningStatusTypeDef",
    {
        "AccountId": NotRequired[str],
        "CreatedDate": NotRequired[datetime],
        "FailureReason": NotRequired[str],
        "PermissionSetArn": NotRequired[str],
        "RequestId": NotRequired[str],
        "Status": NotRequired[StatusValuesType],
    },
)

DescribePermissionSetRequestRequestTypeDef = TypedDict(
    "DescribePermissionSetRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "PermissionSetArn": str,
    },
)

DetachManagedPolicyFromPermissionSetRequestRequestTypeDef = TypedDict(
    "DetachManagedPolicyFromPermissionSetRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "ManagedPolicyArn": str,
        "PermissionSetArn": str,
    },
)

GetInlinePolicyForPermissionSetRequestRequestTypeDef = TypedDict(
    "GetInlinePolicyForPermissionSetRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "PermissionSetArn": str,
    },
)

GetPermissionsBoundaryForPermissionSetRequestRequestTypeDef = TypedDict(
    "GetPermissionsBoundaryForPermissionSetRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "PermissionSetArn": str,
    },
)

InstanceMetadataTypeDef = TypedDict(
    "InstanceMetadataTypeDef",
    {
        "IdentityStoreId": NotRequired[str],
        "InstanceArn": NotRequired[str],
    },
)

OperationStatusFilterTypeDef = TypedDict(
    "OperationStatusFilterTypeDef",
    {
        "Status": NotRequired[StatusValuesType],
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

ListAccountAssignmentsRequestRequestTypeDef = TypedDict(
    "ListAccountAssignmentsRequestRequestTypeDef",
    {
        "AccountId": str,
        "InstanceArn": str,
        "PermissionSetArn": str,
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

ListAccountsForProvisionedPermissionSetRequestRequestTypeDef = TypedDict(
    "ListAccountsForProvisionedPermissionSetRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "PermissionSetArn": str,
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
        "ProvisioningStatus": NotRequired[ProvisioningStatusType],
    },
)

ListCustomerManagedPolicyReferencesInPermissionSetRequestRequestTypeDef = TypedDict(
    "ListCustomerManagedPolicyReferencesInPermissionSetRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "PermissionSetArn": str,
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

ListInstancesRequestRequestTypeDef = TypedDict(
    "ListInstancesRequestRequestTypeDef",
    {
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

ListManagedPoliciesInPermissionSetRequestRequestTypeDef = TypedDict(
    "ListManagedPoliciesInPermissionSetRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "PermissionSetArn": str,
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

PermissionSetProvisioningStatusMetadataTypeDef = TypedDict(
    "PermissionSetProvisioningStatusMetadataTypeDef",
    {
        "CreatedDate": NotRequired[datetime],
        "RequestId": NotRequired[str],
        "Status": NotRequired[StatusValuesType],
    },
)

ListPermissionSetsProvisionedToAccountRequestRequestTypeDef = TypedDict(
    "ListPermissionSetsProvisionedToAccountRequestRequestTypeDef",
    {
        "AccountId": str,
        "InstanceArn": str,
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
        "ProvisioningStatus": NotRequired[ProvisioningStatusType],
    },
)

ListPermissionSetsRequestRequestTypeDef = TypedDict(
    "ListPermissionSetsRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "ResourceArn": str,
        "NextToken": NotRequired[str],
    },
)

ProvisionPermissionSetRequestRequestTypeDef = TypedDict(
    "ProvisionPermissionSetRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "PermissionSetArn": str,
        "TargetType": ProvisionTargetTypeType,
        "TargetId": NotRequired[str],
    },
)

PutInlinePolicyToPermissionSetRequestRequestTypeDef = TypedDict(
    "PutInlinePolicyToPermissionSetRequestRequestTypeDef",
    {
        "InlinePolicy": str,
        "InstanceArn": str,
        "PermissionSetArn": str,
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

UpdatePermissionSetRequestRequestTypeDef = TypedDict(
    "UpdatePermissionSetRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "PermissionSetArn": str,
        "Description": NotRequired[str],
        "RelayState": NotRequired[str],
        "SessionDuration": NotRequired[str],
    },
)

AccessControlAttributeTypeDef = TypedDict(
    "AccessControlAttributeTypeDef",
    {
        "Key": str,
        "Value": AccessControlAttributeValueTypeDef,
    },
)

AttachCustomerManagedPolicyReferenceToPermissionSetRequestRequestTypeDef = TypedDict(
    "AttachCustomerManagedPolicyReferenceToPermissionSetRequestRequestTypeDef",
    {
        "CustomerManagedPolicyReference": CustomerManagedPolicyReferenceTypeDef,
        "InstanceArn": str,
        "PermissionSetArn": str,
    },
)

DetachCustomerManagedPolicyReferenceFromPermissionSetRequestRequestTypeDef = TypedDict(
    "DetachCustomerManagedPolicyReferenceFromPermissionSetRequestRequestTypeDef",
    {
        "CustomerManagedPolicyReference": CustomerManagedPolicyReferenceTypeDef,
        "InstanceArn": str,
        "PermissionSetArn": str,
    },
)

PermissionsBoundaryTypeDef = TypedDict(
    "PermissionsBoundaryTypeDef",
    {
        "CustomerManagedPolicyReference": NotRequired[CustomerManagedPolicyReferenceTypeDef],
        "ManagedPolicyArn": NotRequired[str],
    },
)

CreateAccountAssignmentResponseTypeDef = TypedDict(
    "CreateAccountAssignmentResponseTypeDef",
    {
        "AccountAssignmentCreationStatus": AccountAssignmentOperationStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteAccountAssignmentResponseTypeDef = TypedDict(
    "DeleteAccountAssignmentResponseTypeDef",
    {
        "AccountAssignmentDeletionStatus": AccountAssignmentOperationStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAccountAssignmentCreationStatusResponseTypeDef = TypedDict(
    "DescribeAccountAssignmentCreationStatusResponseTypeDef",
    {
        "AccountAssignmentCreationStatus": AccountAssignmentOperationStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAccountAssignmentDeletionStatusResponseTypeDef = TypedDict(
    "DescribeAccountAssignmentDeletionStatusResponseTypeDef",
    {
        "AccountAssignmentDeletionStatus": AccountAssignmentOperationStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetInlinePolicyForPermissionSetResponseTypeDef = TypedDict(
    "GetInlinePolicyForPermissionSetResponseTypeDef",
    {
        "InlinePolicy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAccountAssignmentCreationStatusResponseTypeDef = TypedDict(
    "ListAccountAssignmentCreationStatusResponseTypeDef",
    {
        "AccountAssignmentsCreationStatus": List[AccountAssignmentOperationStatusMetadataTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAccountAssignmentDeletionStatusResponseTypeDef = TypedDict(
    "ListAccountAssignmentDeletionStatusResponseTypeDef",
    {
        "AccountAssignmentsDeletionStatus": List[AccountAssignmentOperationStatusMetadataTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAccountAssignmentsResponseTypeDef = TypedDict(
    "ListAccountAssignmentsResponseTypeDef",
    {
        "AccountAssignments": List[AccountAssignmentTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAccountsForProvisionedPermissionSetResponseTypeDef = TypedDict(
    "ListAccountsForProvisionedPermissionSetResponseTypeDef",
    {
        "AccountIds": List[str],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListCustomerManagedPolicyReferencesInPermissionSetResponseTypeDef = TypedDict(
    "ListCustomerManagedPolicyReferencesInPermissionSetResponseTypeDef",
    {
        "CustomerManagedPolicyReferences": List[CustomerManagedPolicyReferenceTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListManagedPoliciesInPermissionSetResponseTypeDef = TypedDict(
    "ListManagedPoliciesInPermissionSetResponseTypeDef",
    {
        "AttachedManagedPolicies": List[AttachedManagedPolicyTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListPermissionSetsProvisionedToAccountResponseTypeDef = TypedDict(
    "ListPermissionSetsProvisionedToAccountResponseTypeDef",
    {
        "NextToken": str,
        "PermissionSets": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListPermissionSetsResponseTypeDef = TypedDict(
    "ListPermissionSetsResponseTypeDef",
    {
        "NextToken": str,
        "PermissionSets": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreatePermissionSetRequestRequestTypeDef = TypedDict(
    "CreatePermissionSetRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "Name": str,
        "Description": NotRequired[str],
        "RelayState": NotRequired[str],
        "SessionDuration": NotRequired[str],
        "Tags": NotRequired[Sequence[TagTypeDef]],
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "NextToken": str,
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "ResourceArn": str,
        "Tags": Sequence[TagTypeDef],
    },
)

CreatePermissionSetResponseTypeDef = TypedDict(
    "CreatePermissionSetResponseTypeDef",
    {
        "PermissionSet": PermissionSetTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribePermissionSetResponseTypeDef = TypedDict(
    "DescribePermissionSetResponseTypeDef",
    {
        "PermissionSet": PermissionSetTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribePermissionSetProvisioningStatusResponseTypeDef = TypedDict(
    "DescribePermissionSetProvisioningStatusResponseTypeDef",
    {
        "PermissionSetProvisioningStatus": PermissionSetProvisioningStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ProvisionPermissionSetResponseTypeDef = TypedDict(
    "ProvisionPermissionSetResponseTypeDef",
    {
        "PermissionSetProvisioningStatus": PermissionSetProvisioningStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListInstancesResponseTypeDef = TypedDict(
    "ListInstancesResponseTypeDef",
    {
        "Instances": List[InstanceMetadataTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAccountAssignmentCreationStatusRequestRequestTypeDef = TypedDict(
    "ListAccountAssignmentCreationStatusRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "Filter": NotRequired[OperationStatusFilterTypeDef],
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

ListAccountAssignmentDeletionStatusRequestRequestTypeDef = TypedDict(
    "ListAccountAssignmentDeletionStatusRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "Filter": NotRequired[OperationStatusFilterTypeDef],
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

ListPermissionSetProvisioningStatusRequestRequestTypeDef = TypedDict(
    "ListPermissionSetProvisioningStatusRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "Filter": NotRequired[OperationStatusFilterTypeDef],
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

ListAccountAssignmentCreationStatusRequestListAccountAssignmentCreationStatusPaginateTypeDef = TypedDict(
    "ListAccountAssignmentCreationStatusRequestListAccountAssignmentCreationStatusPaginateTypeDef",
    {
        "InstanceArn": str,
        "Filter": NotRequired[OperationStatusFilterTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListAccountAssignmentDeletionStatusRequestListAccountAssignmentDeletionStatusPaginateTypeDef = TypedDict(
    "ListAccountAssignmentDeletionStatusRequestListAccountAssignmentDeletionStatusPaginateTypeDef",
    {
        "InstanceArn": str,
        "Filter": NotRequired[OperationStatusFilterTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListAccountAssignmentsRequestListAccountAssignmentsPaginateTypeDef = TypedDict(
    "ListAccountAssignmentsRequestListAccountAssignmentsPaginateTypeDef",
    {
        "AccountId": str,
        "InstanceArn": str,
        "PermissionSetArn": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListAccountsForProvisionedPermissionSetRequestListAccountsForProvisionedPermissionSetPaginateTypeDef = TypedDict(
    "ListAccountsForProvisionedPermissionSetRequestListAccountsForProvisionedPermissionSetPaginateTypeDef",
    {
        "InstanceArn": str,
        "PermissionSetArn": str,
        "ProvisioningStatus": NotRequired[ProvisioningStatusType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListCustomerManagedPolicyReferencesInPermissionSetRequestListCustomerManagedPolicyReferencesInPermissionSetPaginateTypeDef = TypedDict(
    "ListCustomerManagedPolicyReferencesInPermissionSetRequestListCustomerManagedPolicyReferencesInPermissionSetPaginateTypeDef",
    {
        "InstanceArn": str,
        "PermissionSetArn": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListInstancesRequestListInstancesPaginateTypeDef = TypedDict(
    "ListInstancesRequestListInstancesPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListManagedPoliciesInPermissionSetRequestListManagedPoliciesInPermissionSetPaginateTypeDef = TypedDict(
    "ListManagedPoliciesInPermissionSetRequestListManagedPoliciesInPermissionSetPaginateTypeDef",
    {
        "InstanceArn": str,
        "PermissionSetArn": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListPermissionSetProvisioningStatusRequestListPermissionSetProvisioningStatusPaginateTypeDef = TypedDict(
    "ListPermissionSetProvisioningStatusRequestListPermissionSetProvisioningStatusPaginateTypeDef",
    {
        "InstanceArn": str,
        "Filter": NotRequired[OperationStatusFilterTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListPermissionSetsProvisionedToAccountRequestListPermissionSetsProvisionedToAccountPaginateTypeDef = TypedDict(
    "ListPermissionSetsProvisionedToAccountRequestListPermissionSetsProvisionedToAccountPaginateTypeDef",
    {
        "AccountId": str,
        "InstanceArn": str,
        "ProvisioningStatus": NotRequired[ProvisioningStatusType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListPermissionSetsRequestListPermissionSetsPaginateTypeDef = TypedDict(
    "ListPermissionSetsRequestListPermissionSetsPaginateTypeDef",
    {
        "InstanceArn": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListTagsForResourceRequestListTagsForResourcePaginateTypeDef = TypedDict(
    "ListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    {
        "InstanceArn": str,
        "ResourceArn": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListPermissionSetProvisioningStatusResponseTypeDef = TypedDict(
    "ListPermissionSetProvisioningStatusResponseTypeDef",
    {
        "NextToken": str,
        "PermissionSetsProvisioningStatus": List[PermissionSetProvisioningStatusMetadataTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

InstanceAccessControlAttributeConfigurationTypeDef = TypedDict(
    "InstanceAccessControlAttributeConfigurationTypeDef",
    {
        "AccessControlAttributes": Sequence[AccessControlAttributeTypeDef],
    },
)

GetPermissionsBoundaryForPermissionSetResponseTypeDef = TypedDict(
    "GetPermissionsBoundaryForPermissionSetResponseTypeDef",
    {
        "PermissionsBoundary": PermissionsBoundaryTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutPermissionsBoundaryToPermissionSetRequestRequestTypeDef = TypedDict(
    "PutPermissionsBoundaryToPermissionSetRequestRequestTypeDef",
    {
        "InstanceArn": str,
        "PermissionSetArn": str,
        "PermissionsBoundary": PermissionsBoundaryTypeDef,
    },
)

CreateInstanceAccessControlAttributeConfigurationRequestRequestTypeDef = TypedDict(
    "CreateInstanceAccessControlAttributeConfigurationRequestRequestTypeDef",
    {
        "InstanceAccessControlAttributeConfiguration": (
            InstanceAccessControlAttributeConfigurationTypeDef
        ),
        "InstanceArn": str,
    },
)

DescribeInstanceAccessControlAttributeConfigurationResponseTypeDef = TypedDict(
    "DescribeInstanceAccessControlAttributeConfigurationResponseTypeDef",
    {
        "InstanceAccessControlAttributeConfiguration": (
            InstanceAccessControlAttributeConfigurationTypeDef
        ),
        "Status": InstanceAccessControlAttributeConfigurationStatusType,
        "StatusReason": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateInstanceAccessControlAttributeConfigurationRequestRequestTypeDef = TypedDict(
    "UpdateInstanceAccessControlAttributeConfigurationRequestRequestTypeDef",
    {
        "InstanceAccessControlAttributeConfiguration": (
            InstanceAccessControlAttributeConfigurationTypeDef
        ),
        "InstanceArn": str,
    },
)
