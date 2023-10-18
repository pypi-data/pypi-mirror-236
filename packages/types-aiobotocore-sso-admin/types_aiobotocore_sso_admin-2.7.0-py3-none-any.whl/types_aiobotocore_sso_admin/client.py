"""
Type annotations for sso-admin service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_sso_admin.client import SSOAdminClient

    session = get_session()
    async with session.create_client("sso-admin") as client:
        client: SSOAdminClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import PrincipalTypeType, ProvisioningStatusType, ProvisionTargetTypeType
from .paginator import (
    ListAccountAssignmentCreationStatusPaginator,
    ListAccountAssignmentDeletionStatusPaginator,
    ListAccountAssignmentsPaginator,
    ListAccountsForProvisionedPermissionSetPaginator,
    ListCustomerManagedPolicyReferencesInPermissionSetPaginator,
    ListInstancesPaginator,
    ListManagedPoliciesInPermissionSetPaginator,
    ListPermissionSetProvisioningStatusPaginator,
    ListPermissionSetsPaginator,
    ListPermissionSetsProvisionedToAccountPaginator,
    ListTagsForResourcePaginator,
)
from .type_defs import (
    CreateAccountAssignmentResponseTypeDef,
    CreatePermissionSetResponseTypeDef,
    CustomerManagedPolicyReferenceTypeDef,
    DeleteAccountAssignmentResponseTypeDef,
    DescribeAccountAssignmentCreationStatusResponseTypeDef,
    DescribeAccountAssignmentDeletionStatusResponseTypeDef,
    DescribeInstanceAccessControlAttributeConfigurationResponseTypeDef,
    DescribePermissionSetProvisioningStatusResponseTypeDef,
    DescribePermissionSetResponseTypeDef,
    GetInlinePolicyForPermissionSetResponseTypeDef,
    GetPermissionsBoundaryForPermissionSetResponseTypeDef,
    InstanceAccessControlAttributeConfigurationTypeDef,
    ListAccountAssignmentCreationStatusResponseTypeDef,
    ListAccountAssignmentDeletionStatusResponseTypeDef,
    ListAccountAssignmentsResponseTypeDef,
    ListAccountsForProvisionedPermissionSetResponseTypeDef,
    ListCustomerManagedPolicyReferencesInPermissionSetResponseTypeDef,
    ListInstancesResponseTypeDef,
    ListManagedPoliciesInPermissionSetResponseTypeDef,
    ListPermissionSetProvisioningStatusResponseTypeDef,
    ListPermissionSetsProvisionedToAccountResponseTypeDef,
    ListPermissionSetsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    OperationStatusFilterTypeDef,
    PermissionsBoundaryTypeDef,
    ProvisionPermissionSetResponseTypeDef,
    TagTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("SSOAdminClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class SSOAdminClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SSOAdminClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#exceptions)
        """

    async def attach_customer_managed_policy_reference_to_permission_set(
        self,
        *,
        CustomerManagedPolicyReference: CustomerManagedPolicyReferenceTypeDef,
        InstanceArn: str,
        PermissionSetArn: str
    ) -> Dict[str, Any]:
        """
        Attaches the specified customer managed policy to the specified  PermissionSet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.attach_customer_managed_policy_reference_to_permission_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#attach_customer_managed_policy_reference_to_permission_set)
        """

    async def attach_managed_policy_to_permission_set(
        self, *, InstanceArn: str, ManagedPolicyArn: str, PermissionSetArn: str
    ) -> Dict[str, Any]:
        """
        Attaches an Amazon Web Services managed policy ARN to a permission set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.attach_managed_policy_to_permission_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#attach_managed_policy_to_permission_set)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#close)
        """

    async def create_account_assignment(
        self,
        *,
        InstanceArn: str,
        PermissionSetArn: str,
        PrincipalId: str,
        PrincipalType: PrincipalTypeType,
        TargetId: str,
        TargetType: Literal["AWS_ACCOUNT"]
    ) -> CreateAccountAssignmentResponseTypeDef:
        """
        Assigns access to a principal for a specified Amazon Web Services account using
        a specified permission
        set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.create_account_assignment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#create_account_assignment)
        """

    async def create_instance_access_control_attribute_configuration(
        self,
        *,
        InstanceAccessControlAttributeConfiguration: InstanceAccessControlAttributeConfigurationTypeDef,
        InstanceArn: str
    ) -> Dict[str, Any]:
        """
        Enables the attributes-based access control (ABAC) feature for the specified
        IAM Identity Center
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.create_instance_access_control_attribute_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#create_instance_access_control_attribute_configuration)
        """

    async def create_permission_set(
        self,
        *,
        InstanceArn: str,
        Name: str,
        Description: str = ...,
        RelayState: str = ...,
        SessionDuration: str = ...,
        Tags: Sequence[TagTypeDef] = ...
    ) -> CreatePermissionSetResponseTypeDef:
        """
        Creates a permission set within a specified IAM Identity Center instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.create_permission_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#create_permission_set)
        """

    async def delete_account_assignment(
        self,
        *,
        InstanceArn: str,
        PermissionSetArn: str,
        PrincipalId: str,
        PrincipalType: PrincipalTypeType,
        TargetId: str,
        TargetType: Literal["AWS_ACCOUNT"]
    ) -> DeleteAccountAssignmentResponseTypeDef:
        """
        Deletes a principal's access from a specified Amazon Web Services account using
        a specified permission
        set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.delete_account_assignment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#delete_account_assignment)
        """

    async def delete_inline_policy_from_permission_set(
        self, *, InstanceArn: str, PermissionSetArn: str
    ) -> Dict[str, Any]:
        """
        Deletes the inline policy from a specified permission set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.delete_inline_policy_from_permission_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#delete_inline_policy_from_permission_set)
        """

    async def delete_instance_access_control_attribute_configuration(
        self, *, InstanceArn: str
    ) -> Dict[str, Any]:
        """
        Disables the attributes-based access control (ABAC) feature for the specified
        IAM Identity Center instance and deletes all of the attribute mappings that
        have been
        configured.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.delete_instance_access_control_attribute_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#delete_instance_access_control_attribute_configuration)
        """

    async def delete_permission_set(
        self, *, InstanceArn: str, PermissionSetArn: str
    ) -> Dict[str, Any]:
        """
        Deletes the specified permission set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.delete_permission_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#delete_permission_set)
        """

    async def delete_permissions_boundary_from_permission_set(
        self, *, InstanceArn: str, PermissionSetArn: str
    ) -> Dict[str, Any]:
        """
        Deletes the permissions boundary from a specified  PermissionSet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.delete_permissions_boundary_from_permission_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#delete_permissions_boundary_from_permission_set)
        """

    async def describe_account_assignment_creation_status(
        self, *, AccountAssignmentCreationRequestId: str, InstanceArn: str
    ) -> DescribeAccountAssignmentCreationStatusResponseTypeDef:
        """
        Describes the status of the assignment creation request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.describe_account_assignment_creation_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#describe_account_assignment_creation_status)
        """

    async def describe_account_assignment_deletion_status(
        self, *, AccountAssignmentDeletionRequestId: str, InstanceArn: str
    ) -> DescribeAccountAssignmentDeletionStatusResponseTypeDef:
        """
        Describes the status of the assignment deletion request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.describe_account_assignment_deletion_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#describe_account_assignment_deletion_status)
        """

    async def describe_instance_access_control_attribute_configuration(
        self, *, InstanceArn: str
    ) -> DescribeInstanceAccessControlAttributeConfigurationResponseTypeDef:
        """
        Returns the list of IAM Identity Center identity store attributes that have
        been configured to work with attributes-based access control (ABAC) for the
        specified IAM Identity Center
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.describe_instance_access_control_attribute_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#describe_instance_access_control_attribute_configuration)
        """

    async def describe_permission_set(
        self, *, InstanceArn: str, PermissionSetArn: str
    ) -> DescribePermissionSetResponseTypeDef:
        """
        Gets the details of the permission set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.describe_permission_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#describe_permission_set)
        """

    async def describe_permission_set_provisioning_status(
        self, *, InstanceArn: str, ProvisionPermissionSetRequestId: str
    ) -> DescribePermissionSetProvisioningStatusResponseTypeDef:
        """
        Describes the status for the given permission set provisioning request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.describe_permission_set_provisioning_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#describe_permission_set_provisioning_status)
        """

    async def detach_customer_managed_policy_reference_from_permission_set(
        self,
        *,
        CustomerManagedPolicyReference: CustomerManagedPolicyReferenceTypeDef,
        InstanceArn: str,
        PermissionSetArn: str
    ) -> Dict[str, Any]:
        """
        Detaches the specified customer managed policy from the specified
        PermissionSet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.detach_customer_managed_policy_reference_from_permission_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#detach_customer_managed_policy_reference_from_permission_set)
        """

    async def detach_managed_policy_from_permission_set(
        self, *, InstanceArn: str, ManagedPolicyArn: str, PermissionSetArn: str
    ) -> Dict[str, Any]:
        """
        Detaches the attached Amazon Web Services managed policy ARN from the specified
        permission
        set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.detach_managed_policy_from_permission_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#detach_managed_policy_from_permission_set)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#generate_presigned_url)
        """

    async def get_inline_policy_for_permission_set(
        self, *, InstanceArn: str, PermissionSetArn: str
    ) -> GetInlinePolicyForPermissionSetResponseTypeDef:
        """
        Obtains the inline policy assigned to the permission set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.get_inline_policy_for_permission_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#get_inline_policy_for_permission_set)
        """

    async def get_permissions_boundary_for_permission_set(
        self, *, InstanceArn: str, PermissionSetArn: str
    ) -> GetPermissionsBoundaryForPermissionSetResponseTypeDef:
        """
        Obtains the permissions boundary for a specified  PermissionSet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.get_permissions_boundary_for_permission_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#get_permissions_boundary_for_permission_set)
        """

    async def list_account_assignment_creation_status(
        self,
        *,
        InstanceArn: str,
        Filter: OperationStatusFilterTypeDef = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> ListAccountAssignmentCreationStatusResponseTypeDef:
        """
        Lists the status of the Amazon Web Services account assignment creation
        requests for a specified IAM Identity Center
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.list_account_assignment_creation_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#list_account_assignment_creation_status)
        """

    async def list_account_assignment_deletion_status(
        self,
        *,
        InstanceArn: str,
        Filter: OperationStatusFilterTypeDef = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> ListAccountAssignmentDeletionStatusResponseTypeDef:
        """
        Lists the status of the Amazon Web Services account assignment deletion
        requests for a specified IAM Identity Center
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.list_account_assignment_deletion_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#list_account_assignment_deletion_status)
        """

    async def list_account_assignments(
        self,
        *,
        AccountId: str,
        InstanceArn: str,
        PermissionSetArn: str,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> ListAccountAssignmentsResponseTypeDef:
        """
        Lists the assignee of the specified Amazon Web Services account with the
        specified permission
        set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.list_account_assignments)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#list_account_assignments)
        """

    async def list_accounts_for_provisioned_permission_set(
        self,
        *,
        InstanceArn: str,
        PermissionSetArn: str,
        MaxResults: int = ...,
        NextToken: str = ...,
        ProvisioningStatus: ProvisioningStatusType = ...
    ) -> ListAccountsForProvisionedPermissionSetResponseTypeDef:
        """
        Lists all the Amazon Web Services accounts where the specified permission set
        is
        provisioned.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.list_accounts_for_provisioned_permission_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#list_accounts_for_provisioned_permission_set)
        """

    async def list_customer_managed_policy_references_in_permission_set(
        self,
        *,
        InstanceArn: str,
        PermissionSetArn: str,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> ListCustomerManagedPolicyReferencesInPermissionSetResponseTypeDef:
        """
        Lists all customer managed policies attached to a specified  PermissionSet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.list_customer_managed_policy_references_in_permission_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#list_customer_managed_policy_references_in_permission_set)
        """

    async def list_instances(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListInstancesResponseTypeDef:
        """
        Lists the IAM Identity Center instances that the caller has access to.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.list_instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#list_instances)
        """

    async def list_managed_policies_in_permission_set(
        self,
        *,
        InstanceArn: str,
        PermissionSetArn: str,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> ListManagedPoliciesInPermissionSetResponseTypeDef:
        """
        Lists the Amazon Web Services managed policy that is attached to a specified
        permission
        set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.list_managed_policies_in_permission_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#list_managed_policies_in_permission_set)
        """

    async def list_permission_set_provisioning_status(
        self,
        *,
        InstanceArn: str,
        Filter: OperationStatusFilterTypeDef = ...,
        MaxResults: int = ...,
        NextToken: str = ...
    ) -> ListPermissionSetProvisioningStatusResponseTypeDef:
        """
        Lists the status of the permission set provisioning requests for a specified
        IAM Identity Center
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.list_permission_set_provisioning_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#list_permission_set_provisioning_status)
        """

    async def list_permission_sets(
        self, *, InstanceArn: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListPermissionSetsResponseTypeDef:
        """
        Lists the  PermissionSets in an IAM Identity Center instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.list_permission_sets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#list_permission_sets)
        """

    async def list_permission_sets_provisioned_to_account(
        self,
        *,
        AccountId: str,
        InstanceArn: str,
        MaxResults: int = ...,
        NextToken: str = ...,
        ProvisioningStatus: ProvisioningStatusType = ...
    ) -> ListPermissionSetsProvisionedToAccountResponseTypeDef:
        """
        Lists all the permission sets that are provisioned to a specified Amazon Web
        Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.list_permission_sets_provisioned_to_account)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#list_permission_sets_provisioned_to_account)
        """

    async def list_tags_for_resource(
        self, *, InstanceArn: str, ResourceArn: str, NextToken: str = ...
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags that are attached to a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#list_tags_for_resource)
        """

    async def provision_permission_set(
        self,
        *,
        InstanceArn: str,
        PermissionSetArn: str,
        TargetType: ProvisionTargetTypeType,
        TargetId: str = ...
    ) -> ProvisionPermissionSetResponseTypeDef:
        """
        The process by which a specified permission set is provisioned to the specified
        target.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.provision_permission_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#provision_permission_set)
        """

    async def put_inline_policy_to_permission_set(
        self, *, InlinePolicy: str, InstanceArn: str, PermissionSetArn: str
    ) -> Dict[str, Any]:
        """
        Attaches an inline policy to a permission set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.put_inline_policy_to_permission_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#put_inline_policy_to_permission_set)
        """

    async def put_permissions_boundary_to_permission_set(
        self,
        *,
        InstanceArn: str,
        PermissionSetArn: str,
        PermissionsBoundary: PermissionsBoundaryTypeDef
    ) -> Dict[str, Any]:
        """
        Attaches an Amazon Web Services managed or customer managed policy to the
        specified  PermissionSet as a permissions
        boundary.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.put_permissions_boundary_to_permission_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#put_permissions_boundary_to_permission_set)
        """

    async def tag_resource(
        self, *, InstanceArn: str, ResourceArn: str, Tags: Sequence[TagTypeDef]
    ) -> Dict[str, Any]:
        """
        Associates a set of tags with a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#tag_resource)
        """

    async def untag_resource(
        self, *, InstanceArn: str, ResourceArn: str, TagKeys: Sequence[str]
    ) -> Dict[str, Any]:
        """
        Disassociates a set of tags from a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#untag_resource)
        """

    async def update_instance_access_control_attribute_configuration(
        self,
        *,
        InstanceAccessControlAttributeConfiguration: InstanceAccessControlAttributeConfigurationTypeDef,
        InstanceArn: str
    ) -> Dict[str, Any]:
        """
        Updates the IAM Identity Center identity store attributes that you can use with
        the IAM Identity Center instance for attributes-based access control
        (ABAC).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.update_instance_access_control_attribute_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#update_instance_access_control_attribute_configuration)
        """

    async def update_permission_set(
        self,
        *,
        InstanceArn: str,
        PermissionSetArn: str,
        Description: str = ...,
        RelayState: str = ...,
        SessionDuration: str = ...
    ) -> Dict[str, Any]:
        """
        Updates an existing permission set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.update_permission_set)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#update_permission_set)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_account_assignment_creation_status"]
    ) -> ListAccountAssignmentCreationStatusPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_account_assignment_deletion_status"]
    ) -> ListAccountAssignmentDeletionStatusPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_account_assignments"]
    ) -> ListAccountAssignmentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_accounts_for_provisioned_permission_set"]
    ) -> ListAccountsForProvisionedPermissionSetPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_customer_managed_policy_references_in_permission_set"]
    ) -> ListCustomerManagedPolicyReferencesInPermissionSetPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_instances"]) -> ListInstancesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_managed_policies_in_permission_set"]
    ) -> ListManagedPoliciesInPermissionSetPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_permission_set_provisioning_status"]
    ) -> ListPermissionSetProvisioningStatusPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_permission_sets"]
    ) -> ListPermissionSetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_permission_sets_provisioned_to_account"]
    ) -> ListPermissionSetsProvisionedToAccountPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/#get_paginator)
        """

    async def __aenter__(self) -> "SSOAdminClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html#SSOAdmin.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sso_admin/client/)
        """
