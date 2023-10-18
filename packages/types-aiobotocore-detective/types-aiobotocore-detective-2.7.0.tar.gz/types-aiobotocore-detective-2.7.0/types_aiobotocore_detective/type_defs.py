"""
Type annotations for detective service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_detective/type_defs/)

Usage::

    ```python
    from types_aiobotocore_detective.type_defs import AcceptInvitationRequestRequestTypeDef

    data: AcceptInvitationRequestRequestTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    DatasourcePackageIngestStateType,
    DatasourcePackageType,
    InvitationTypeType,
    MemberDisabledReasonType,
    MemberStatusType,
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
    "AcceptInvitationRequestRequestTypeDef",
    "AccountTypeDef",
    "AdministratorTypeDef",
    "BatchGetGraphMemberDatasourcesRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "UnprocessedAccountTypeDef",
    "BatchGetMembershipDatasourcesRequestRequestTypeDef",
    "UnprocessedGraphTypeDef",
    "CreateGraphRequestRequestTypeDef",
    "TimestampForCollectionTypeDef",
    "DatasourcePackageUsageInfoTypeDef",
    "DeleteGraphRequestRequestTypeDef",
    "DeleteMembersRequestRequestTypeDef",
    "DescribeOrganizationConfigurationRequestRequestTypeDef",
    "DisassociateMembershipRequestRequestTypeDef",
    "EnableOrganizationAdminAccountRequestRequestTypeDef",
    "GetMembersRequestRequestTypeDef",
    "GraphTypeDef",
    "ListDatasourcePackagesRequestRequestTypeDef",
    "ListGraphsRequestRequestTypeDef",
    "ListInvitationsRequestRequestTypeDef",
    "ListMembersRequestRequestTypeDef",
    "ListOrganizationAdminAccountsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "RejectInvitationRequestRequestTypeDef",
    "StartMonitoringMemberRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateDatasourcePackagesRequestRequestTypeDef",
    "UpdateOrganizationConfigurationRequestRequestTypeDef",
    "CreateMembersRequestRequestTypeDef",
    "CreateGraphResponseTypeDef",
    "DescribeOrganizationConfigurationResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ListOrganizationAdminAccountsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "DeleteMembersResponseTypeDef",
    "DatasourcePackageIngestDetailTypeDef",
    "MembershipDatasourcesTypeDef",
    "MemberDetailTypeDef",
    "ListGraphsResponseTypeDef",
    "ListDatasourcePackagesResponseTypeDef",
    "BatchGetGraphMemberDatasourcesResponseTypeDef",
    "BatchGetMembershipDatasourcesResponseTypeDef",
    "CreateMembersResponseTypeDef",
    "GetMembersResponseTypeDef",
    "ListInvitationsResponseTypeDef",
    "ListMembersResponseTypeDef",
)

AcceptInvitationRequestRequestTypeDef = TypedDict(
    "AcceptInvitationRequestRequestTypeDef",
    {
        "GraphArn": str,
    },
)

AccountTypeDef = TypedDict(
    "AccountTypeDef",
    {
        "AccountId": str,
        "EmailAddress": str,
    },
)

AdministratorTypeDef = TypedDict(
    "AdministratorTypeDef",
    {
        "AccountId": NotRequired[str],
        "GraphArn": NotRequired[str],
        "DelegationTime": NotRequired[datetime],
    },
)

BatchGetGraphMemberDatasourcesRequestRequestTypeDef = TypedDict(
    "BatchGetGraphMemberDatasourcesRequestRequestTypeDef",
    {
        "GraphArn": str,
        "AccountIds": Sequence[str],
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

UnprocessedAccountTypeDef = TypedDict(
    "UnprocessedAccountTypeDef",
    {
        "AccountId": NotRequired[str],
        "Reason": NotRequired[str],
    },
)

BatchGetMembershipDatasourcesRequestRequestTypeDef = TypedDict(
    "BatchGetMembershipDatasourcesRequestRequestTypeDef",
    {
        "GraphArns": Sequence[str],
    },
)

UnprocessedGraphTypeDef = TypedDict(
    "UnprocessedGraphTypeDef",
    {
        "GraphArn": NotRequired[str],
        "Reason": NotRequired[str],
    },
)

CreateGraphRequestRequestTypeDef = TypedDict(
    "CreateGraphRequestRequestTypeDef",
    {
        "Tags": NotRequired[Mapping[str, str]],
    },
)

TimestampForCollectionTypeDef = TypedDict(
    "TimestampForCollectionTypeDef",
    {
        "Timestamp": NotRequired[datetime],
    },
)

DatasourcePackageUsageInfoTypeDef = TypedDict(
    "DatasourcePackageUsageInfoTypeDef",
    {
        "VolumeUsageInBytes": NotRequired[int],
        "VolumeUsageUpdateTime": NotRequired[datetime],
    },
)

DeleteGraphRequestRequestTypeDef = TypedDict(
    "DeleteGraphRequestRequestTypeDef",
    {
        "GraphArn": str,
    },
)

DeleteMembersRequestRequestTypeDef = TypedDict(
    "DeleteMembersRequestRequestTypeDef",
    {
        "GraphArn": str,
        "AccountIds": Sequence[str],
    },
)

DescribeOrganizationConfigurationRequestRequestTypeDef = TypedDict(
    "DescribeOrganizationConfigurationRequestRequestTypeDef",
    {
        "GraphArn": str,
    },
)

DisassociateMembershipRequestRequestTypeDef = TypedDict(
    "DisassociateMembershipRequestRequestTypeDef",
    {
        "GraphArn": str,
    },
)

EnableOrganizationAdminAccountRequestRequestTypeDef = TypedDict(
    "EnableOrganizationAdminAccountRequestRequestTypeDef",
    {
        "AccountId": str,
    },
)

GetMembersRequestRequestTypeDef = TypedDict(
    "GetMembersRequestRequestTypeDef",
    {
        "GraphArn": str,
        "AccountIds": Sequence[str],
    },
)

GraphTypeDef = TypedDict(
    "GraphTypeDef",
    {
        "Arn": NotRequired[str],
        "CreatedTime": NotRequired[datetime],
    },
)

ListDatasourcePackagesRequestRequestTypeDef = TypedDict(
    "ListDatasourcePackagesRequestRequestTypeDef",
    {
        "GraphArn": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ListGraphsRequestRequestTypeDef = TypedDict(
    "ListGraphsRequestRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ListInvitationsRequestRequestTypeDef = TypedDict(
    "ListInvitationsRequestRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ListMembersRequestRequestTypeDef = TypedDict(
    "ListMembersRequestRequestTypeDef",
    {
        "GraphArn": str,
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ListOrganizationAdminAccountsRequestRequestTypeDef = TypedDict(
    "ListOrganizationAdminAccountsRequestRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

RejectInvitationRequestRequestTypeDef = TypedDict(
    "RejectInvitationRequestRequestTypeDef",
    {
        "GraphArn": str,
    },
)

StartMonitoringMemberRequestRequestTypeDef = TypedDict(
    "StartMonitoringMemberRequestRequestTypeDef",
    {
        "GraphArn": str,
        "AccountId": str,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

UpdateDatasourcePackagesRequestRequestTypeDef = TypedDict(
    "UpdateDatasourcePackagesRequestRequestTypeDef",
    {
        "GraphArn": str,
        "DatasourcePackages": Sequence[DatasourcePackageType],
    },
)

UpdateOrganizationConfigurationRequestRequestTypeDef = TypedDict(
    "UpdateOrganizationConfigurationRequestRequestTypeDef",
    {
        "GraphArn": str,
        "AutoEnable": NotRequired[bool],
    },
)

CreateMembersRequestRequestTypeDef = TypedDict(
    "CreateMembersRequestRequestTypeDef",
    {
        "GraphArn": str,
        "Accounts": Sequence[AccountTypeDef],
        "Message": NotRequired[str],
        "DisableEmailNotification": NotRequired[bool],
    },
)

CreateGraphResponseTypeDef = TypedDict(
    "CreateGraphResponseTypeDef",
    {
        "GraphArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeOrganizationConfigurationResponseTypeDef = TypedDict(
    "DescribeOrganizationConfigurationResponseTypeDef",
    {
        "AutoEnable": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListOrganizationAdminAccountsResponseTypeDef = TypedDict(
    "ListOrganizationAdminAccountsResponseTypeDef",
    {
        "Administrators": List[AdministratorTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteMembersResponseTypeDef = TypedDict(
    "DeleteMembersResponseTypeDef",
    {
        "AccountIds": List[str],
        "UnprocessedAccounts": List[UnprocessedAccountTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DatasourcePackageIngestDetailTypeDef = TypedDict(
    "DatasourcePackageIngestDetailTypeDef",
    {
        "DatasourcePackageIngestState": NotRequired[DatasourcePackageIngestStateType],
        "LastIngestStateChange": NotRequired[
            Dict[DatasourcePackageIngestStateType, TimestampForCollectionTypeDef]
        ],
    },
)

MembershipDatasourcesTypeDef = TypedDict(
    "MembershipDatasourcesTypeDef",
    {
        "AccountId": NotRequired[str],
        "GraphArn": NotRequired[str],
        "DatasourcePackageIngestHistory": NotRequired[
            Dict[
                DatasourcePackageType,
                Dict[DatasourcePackageIngestStateType, TimestampForCollectionTypeDef],
            ]
        ],
    },
)

MemberDetailTypeDef = TypedDict(
    "MemberDetailTypeDef",
    {
        "AccountId": NotRequired[str],
        "EmailAddress": NotRequired[str],
        "GraphArn": NotRequired[str],
        "MasterId": NotRequired[str],
        "AdministratorId": NotRequired[str],
        "Status": NotRequired[MemberStatusType],
        "DisabledReason": NotRequired[MemberDisabledReasonType],
        "InvitedTime": NotRequired[datetime],
        "UpdatedTime": NotRequired[datetime],
        "VolumeUsageInBytes": NotRequired[int],
        "VolumeUsageUpdatedTime": NotRequired[datetime],
        "PercentOfGraphUtilization": NotRequired[float],
        "PercentOfGraphUtilizationUpdatedTime": NotRequired[datetime],
        "InvitationType": NotRequired[InvitationTypeType],
        "VolumeUsageByDatasourcePackage": NotRequired[
            Dict[DatasourcePackageType, DatasourcePackageUsageInfoTypeDef]
        ],
        "DatasourcePackageIngestStates": NotRequired[
            Dict[DatasourcePackageType, DatasourcePackageIngestStateType]
        ],
    },
)

ListGraphsResponseTypeDef = TypedDict(
    "ListGraphsResponseTypeDef",
    {
        "GraphList": List[GraphTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListDatasourcePackagesResponseTypeDef = TypedDict(
    "ListDatasourcePackagesResponseTypeDef",
    {
        "DatasourcePackages": Dict[DatasourcePackageType, DatasourcePackageIngestDetailTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchGetGraphMemberDatasourcesResponseTypeDef = TypedDict(
    "BatchGetGraphMemberDatasourcesResponseTypeDef",
    {
        "MemberDatasources": List[MembershipDatasourcesTypeDef],
        "UnprocessedAccounts": List[UnprocessedAccountTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchGetMembershipDatasourcesResponseTypeDef = TypedDict(
    "BatchGetMembershipDatasourcesResponseTypeDef",
    {
        "MembershipDatasources": List[MembershipDatasourcesTypeDef],
        "UnprocessedGraphs": List[UnprocessedGraphTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateMembersResponseTypeDef = TypedDict(
    "CreateMembersResponseTypeDef",
    {
        "Members": List[MemberDetailTypeDef],
        "UnprocessedAccounts": List[UnprocessedAccountTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetMembersResponseTypeDef = TypedDict(
    "GetMembersResponseTypeDef",
    {
        "MemberDetails": List[MemberDetailTypeDef],
        "UnprocessedAccounts": List[UnprocessedAccountTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListInvitationsResponseTypeDef = TypedDict(
    "ListInvitationsResponseTypeDef",
    {
        "Invitations": List[MemberDetailTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListMembersResponseTypeDef = TypedDict(
    "ListMembersResponseTypeDef",
    {
        "MemberDetails": List[MemberDetailTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
