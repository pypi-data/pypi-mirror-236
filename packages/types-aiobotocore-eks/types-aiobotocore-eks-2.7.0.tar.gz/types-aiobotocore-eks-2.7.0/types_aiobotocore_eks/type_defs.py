"""
Type annotations for eks service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_eks/type_defs/)

Usage::

    ```python
    from types_aiobotocore_eks.type_defs import AddonIssueTypeDef

    data: AddonIssueTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    AddonIssueCodeType,
    AddonStatusType,
    AMITypesType,
    CapacityTypesType,
    ClusterIssueCodeType,
    ClusterStatusType,
    ConnectorConfigProviderType,
    ErrorCodeType,
    FargateProfileStatusType,
    IpFamilyType,
    LogTypeType,
    NodegroupIssueCodeType,
    NodegroupStatusType,
    ResolveConflictsType,
    TaintEffectType,
    UpdateParamTypeType,
    UpdateStatusType,
    UpdateTypeType,
    configStatusType,
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
    "AddonIssueTypeDef",
    "MarketplaceInformationTypeDef",
    "CompatibilityTypeDef",
    "ResponseMetadataTypeDef",
    "OidcIdentityProviderConfigRequestTypeDef",
    "AutoScalingGroupTypeDef",
    "CertificateTypeDef",
    "ClusterIssueTypeDef",
    "ConnectorConfigResponseTypeDef",
    "KubernetesNetworkConfigResponseTypeDef",
    "VpcConfigResponseTypeDef",
    "ConnectorConfigRequestTypeDef",
    "ControlPlanePlacementRequestTypeDef",
    "ControlPlanePlacementResponseTypeDef",
    "CreateAddonRequestRequestTypeDef",
    "KubernetesNetworkConfigRequestTypeDef",
    "VpcConfigRequestTypeDef",
    "FargateProfileSelectorTypeDef",
    "LaunchTemplateSpecificationTypeDef",
    "NodegroupScalingConfigTypeDef",
    "NodegroupUpdateConfigTypeDef",
    "RemoteAccessConfigTypeDef",
    "TaintTypeDef",
    "DeleteAddonRequestRequestTypeDef",
    "DeleteClusterRequestRequestTypeDef",
    "DeleteFargateProfileRequestRequestTypeDef",
    "DeleteNodegroupRequestRequestTypeDef",
    "DeregisterClusterRequestRequestTypeDef",
    "DescribeAddonConfigurationRequestRequestTypeDef",
    "WaiterConfigTypeDef",
    "DescribeAddonRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeAddonVersionsRequestRequestTypeDef",
    "DescribeClusterRequestRequestTypeDef",
    "DescribeFargateProfileRequestRequestTypeDef",
    "IdentityProviderConfigTypeDef",
    "DescribeNodegroupRequestRequestTypeDef",
    "DescribeUpdateRequestRequestTypeDef",
    "ProviderTypeDef",
    "ErrorDetailTypeDef",
    "OidcIdentityProviderConfigTypeDef",
    "OIDCTypeDef",
    "IssueTypeDef",
    "ListAddonsRequestRequestTypeDef",
    "ListClustersRequestRequestTypeDef",
    "ListFargateProfilesRequestRequestTypeDef",
    "ListIdentityProviderConfigsRequestRequestTypeDef",
    "ListNodegroupsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListUpdatesRequestRequestTypeDef",
    "LogSetupTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAddonRequestRequestTypeDef",
    "UpdateClusterVersionRequestRequestTypeDef",
    "UpdateLabelsPayloadTypeDef",
    "UpdateParamTypeDef",
    "AddonHealthTypeDef",
    "AddonVersionInfoTypeDef",
    "DescribeAddonConfigurationResponseTypeDef",
    "ListAddonsResponseTypeDef",
    "ListClustersResponseTypeDef",
    "ListFargateProfilesResponseTypeDef",
    "ListNodegroupsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListUpdatesResponseTypeDef",
    "AssociateIdentityProviderConfigRequestRequestTypeDef",
    "NodegroupResourcesTypeDef",
    "ClusterHealthTypeDef",
    "RegisterClusterRequestRequestTypeDef",
    "OutpostConfigRequestTypeDef",
    "OutpostConfigResponseTypeDef",
    "CreateFargateProfileRequestRequestTypeDef",
    "FargateProfileTypeDef",
    "UpdateNodegroupVersionRequestRequestTypeDef",
    "CreateNodegroupRequestRequestTypeDef",
    "UpdateTaintsPayloadTypeDef",
    "DescribeAddonRequestAddonActiveWaitTypeDef",
    "DescribeAddonRequestAddonDeletedWaitTypeDef",
    "DescribeClusterRequestClusterActiveWaitTypeDef",
    "DescribeClusterRequestClusterDeletedWaitTypeDef",
    "DescribeFargateProfileRequestFargateProfileActiveWaitTypeDef",
    "DescribeFargateProfileRequestFargateProfileDeletedWaitTypeDef",
    "DescribeNodegroupRequestNodegroupActiveWaitTypeDef",
    "DescribeNodegroupRequestNodegroupDeletedWaitTypeDef",
    "DescribeAddonVersionsRequestDescribeAddonVersionsPaginateTypeDef",
    "ListAddonsRequestListAddonsPaginateTypeDef",
    "ListClustersRequestListClustersPaginateTypeDef",
    "ListFargateProfilesRequestListFargateProfilesPaginateTypeDef",
    "ListIdentityProviderConfigsRequestListIdentityProviderConfigsPaginateTypeDef",
    "ListNodegroupsRequestListNodegroupsPaginateTypeDef",
    "ListUpdatesRequestListUpdatesPaginateTypeDef",
    "DescribeIdentityProviderConfigRequestRequestTypeDef",
    "DisassociateIdentityProviderConfigRequestRequestTypeDef",
    "ListIdentityProviderConfigsResponseTypeDef",
    "EncryptionConfigTypeDef",
    "IdentityProviderConfigResponseTypeDef",
    "IdentityTypeDef",
    "NodegroupHealthTypeDef",
    "LoggingTypeDef",
    "UpdateTypeDef",
    "AddonTypeDef",
    "AddonInfoTypeDef",
    "CreateFargateProfileResponseTypeDef",
    "DeleteFargateProfileResponseTypeDef",
    "DescribeFargateProfileResponseTypeDef",
    "UpdateNodegroupConfigRequestRequestTypeDef",
    "AssociateEncryptionConfigRequestRequestTypeDef",
    "DescribeIdentityProviderConfigResponseTypeDef",
    "NodegroupTypeDef",
    "ClusterTypeDef",
    "CreateClusterRequestRequestTypeDef",
    "UpdateClusterConfigRequestRequestTypeDef",
    "AssociateEncryptionConfigResponseTypeDef",
    "AssociateIdentityProviderConfigResponseTypeDef",
    "DescribeUpdateResponseTypeDef",
    "DisassociateIdentityProviderConfigResponseTypeDef",
    "UpdateAddonResponseTypeDef",
    "UpdateClusterConfigResponseTypeDef",
    "UpdateClusterVersionResponseTypeDef",
    "UpdateNodegroupConfigResponseTypeDef",
    "UpdateNodegroupVersionResponseTypeDef",
    "CreateAddonResponseTypeDef",
    "DeleteAddonResponseTypeDef",
    "DescribeAddonResponseTypeDef",
    "DescribeAddonVersionsResponseTypeDef",
    "CreateNodegroupResponseTypeDef",
    "DeleteNodegroupResponseTypeDef",
    "DescribeNodegroupResponseTypeDef",
    "CreateClusterResponseTypeDef",
    "DeleteClusterResponseTypeDef",
    "DeregisterClusterResponseTypeDef",
    "DescribeClusterResponseTypeDef",
    "RegisterClusterResponseTypeDef",
)

AddonIssueTypeDef = TypedDict(
    "AddonIssueTypeDef",
    {
        "code": NotRequired[AddonIssueCodeType],
        "message": NotRequired[str],
        "resourceIds": NotRequired[List[str]],
    },
)

MarketplaceInformationTypeDef = TypedDict(
    "MarketplaceInformationTypeDef",
    {
        "productId": NotRequired[str],
        "productUrl": NotRequired[str],
    },
)

CompatibilityTypeDef = TypedDict(
    "CompatibilityTypeDef",
    {
        "clusterVersion": NotRequired[str],
        "platformVersions": NotRequired[List[str]],
        "defaultVersion": NotRequired[bool],
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

OidcIdentityProviderConfigRequestTypeDef = TypedDict(
    "OidcIdentityProviderConfigRequestTypeDef",
    {
        "identityProviderConfigName": str,
        "issuerUrl": str,
        "clientId": str,
        "usernameClaim": NotRequired[str],
        "usernamePrefix": NotRequired[str],
        "groupsClaim": NotRequired[str],
        "groupsPrefix": NotRequired[str],
        "requiredClaims": NotRequired[Mapping[str, str]],
    },
)

AutoScalingGroupTypeDef = TypedDict(
    "AutoScalingGroupTypeDef",
    {
        "name": NotRequired[str],
    },
)

CertificateTypeDef = TypedDict(
    "CertificateTypeDef",
    {
        "data": NotRequired[str],
    },
)

ClusterIssueTypeDef = TypedDict(
    "ClusterIssueTypeDef",
    {
        "code": NotRequired[ClusterIssueCodeType],
        "message": NotRequired[str],
        "resourceIds": NotRequired[List[str]],
    },
)

ConnectorConfigResponseTypeDef = TypedDict(
    "ConnectorConfigResponseTypeDef",
    {
        "activationId": NotRequired[str],
        "activationCode": NotRequired[str],
        "activationExpiry": NotRequired[datetime],
        "provider": NotRequired[str],
        "roleArn": NotRequired[str],
    },
)

KubernetesNetworkConfigResponseTypeDef = TypedDict(
    "KubernetesNetworkConfigResponseTypeDef",
    {
        "serviceIpv4Cidr": NotRequired[str],
        "serviceIpv6Cidr": NotRequired[str],
        "ipFamily": NotRequired[IpFamilyType],
    },
)

VpcConfigResponseTypeDef = TypedDict(
    "VpcConfigResponseTypeDef",
    {
        "subnetIds": NotRequired[List[str]],
        "securityGroupIds": NotRequired[List[str]],
        "clusterSecurityGroupId": NotRequired[str],
        "vpcId": NotRequired[str],
        "endpointPublicAccess": NotRequired[bool],
        "endpointPrivateAccess": NotRequired[bool],
        "publicAccessCidrs": NotRequired[List[str]],
    },
)

ConnectorConfigRequestTypeDef = TypedDict(
    "ConnectorConfigRequestTypeDef",
    {
        "roleArn": str,
        "provider": ConnectorConfigProviderType,
    },
)

ControlPlanePlacementRequestTypeDef = TypedDict(
    "ControlPlanePlacementRequestTypeDef",
    {
        "groupName": NotRequired[str],
    },
)

ControlPlanePlacementResponseTypeDef = TypedDict(
    "ControlPlanePlacementResponseTypeDef",
    {
        "groupName": NotRequired[str],
    },
)

CreateAddonRequestRequestTypeDef = TypedDict(
    "CreateAddonRequestRequestTypeDef",
    {
        "clusterName": str,
        "addonName": str,
        "addonVersion": NotRequired[str],
        "serviceAccountRoleArn": NotRequired[str],
        "resolveConflicts": NotRequired[ResolveConflictsType],
        "clientRequestToken": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
        "configurationValues": NotRequired[str],
    },
)

KubernetesNetworkConfigRequestTypeDef = TypedDict(
    "KubernetesNetworkConfigRequestTypeDef",
    {
        "serviceIpv4Cidr": NotRequired[str],
        "ipFamily": NotRequired[IpFamilyType],
    },
)

VpcConfigRequestTypeDef = TypedDict(
    "VpcConfigRequestTypeDef",
    {
        "subnetIds": NotRequired[Sequence[str]],
        "securityGroupIds": NotRequired[Sequence[str]],
        "endpointPublicAccess": NotRequired[bool],
        "endpointPrivateAccess": NotRequired[bool],
        "publicAccessCidrs": NotRequired[Sequence[str]],
    },
)

FargateProfileSelectorTypeDef = TypedDict(
    "FargateProfileSelectorTypeDef",
    {
        "namespace": NotRequired[str],
        "labels": NotRequired[Mapping[str, str]],
    },
)

LaunchTemplateSpecificationTypeDef = TypedDict(
    "LaunchTemplateSpecificationTypeDef",
    {
        "name": NotRequired[str],
        "version": NotRequired[str],
        "id": NotRequired[str],
    },
)

NodegroupScalingConfigTypeDef = TypedDict(
    "NodegroupScalingConfigTypeDef",
    {
        "minSize": NotRequired[int],
        "maxSize": NotRequired[int],
        "desiredSize": NotRequired[int],
    },
)

NodegroupUpdateConfigTypeDef = TypedDict(
    "NodegroupUpdateConfigTypeDef",
    {
        "maxUnavailable": NotRequired[int],
        "maxUnavailablePercentage": NotRequired[int],
    },
)

RemoteAccessConfigTypeDef = TypedDict(
    "RemoteAccessConfigTypeDef",
    {
        "ec2SshKey": NotRequired[str],
        "sourceSecurityGroups": NotRequired[Sequence[str]],
    },
)

TaintTypeDef = TypedDict(
    "TaintTypeDef",
    {
        "key": NotRequired[str],
        "value": NotRequired[str],
        "effect": NotRequired[TaintEffectType],
    },
)

DeleteAddonRequestRequestTypeDef = TypedDict(
    "DeleteAddonRequestRequestTypeDef",
    {
        "clusterName": str,
        "addonName": str,
        "preserve": NotRequired[bool],
    },
)

DeleteClusterRequestRequestTypeDef = TypedDict(
    "DeleteClusterRequestRequestTypeDef",
    {
        "name": str,
    },
)

DeleteFargateProfileRequestRequestTypeDef = TypedDict(
    "DeleteFargateProfileRequestRequestTypeDef",
    {
        "clusterName": str,
        "fargateProfileName": str,
    },
)

DeleteNodegroupRequestRequestTypeDef = TypedDict(
    "DeleteNodegroupRequestRequestTypeDef",
    {
        "clusterName": str,
        "nodegroupName": str,
    },
)

DeregisterClusterRequestRequestTypeDef = TypedDict(
    "DeregisterClusterRequestRequestTypeDef",
    {
        "name": str,
    },
)

DescribeAddonConfigurationRequestRequestTypeDef = TypedDict(
    "DescribeAddonConfigurationRequestRequestTypeDef",
    {
        "addonName": str,
        "addonVersion": str,
    },
)

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": NotRequired[int],
        "MaxAttempts": NotRequired[int],
    },
)

DescribeAddonRequestRequestTypeDef = TypedDict(
    "DescribeAddonRequestRequestTypeDef",
    {
        "clusterName": str,
        "addonName": str,
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

DescribeAddonVersionsRequestRequestTypeDef = TypedDict(
    "DescribeAddonVersionsRequestRequestTypeDef",
    {
        "kubernetesVersion": NotRequired[str],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "addonName": NotRequired[str],
        "types": NotRequired[Sequence[str]],
        "publishers": NotRequired[Sequence[str]],
        "owners": NotRequired[Sequence[str]],
    },
)

DescribeClusterRequestRequestTypeDef = TypedDict(
    "DescribeClusterRequestRequestTypeDef",
    {
        "name": str,
    },
)

DescribeFargateProfileRequestRequestTypeDef = TypedDict(
    "DescribeFargateProfileRequestRequestTypeDef",
    {
        "clusterName": str,
        "fargateProfileName": str,
    },
)

IdentityProviderConfigTypeDef = TypedDict(
    "IdentityProviderConfigTypeDef",
    {
        "type": str,
        "name": str,
    },
)

DescribeNodegroupRequestRequestTypeDef = TypedDict(
    "DescribeNodegroupRequestRequestTypeDef",
    {
        "clusterName": str,
        "nodegroupName": str,
    },
)

DescribeUpdateRequestRequestTypeDef = TypedDict(
    "DescribeUpdateRequestRequestTypeDef",
    {
        "name": str,
        "updateId": str,
        "nodegroupName": NotRequired[str],
        "addonName": NotRequired[str],
    },
)

ProviderTypeDef = TypedDict(
    "ProviderTypeDef",
    {
        "keyArn": NotRequired[str],
    },
)

ErrorDetailTypeDef = TypedDict(
    "ErrorDetailTypeDef",
    {
        "errorCode": NotRequired[ErrorCodeType],
        "errorMessage": NotRequired[str],
        "resourceIds": NotRequired[List[str]],
    },
)

OidcIdentityProviderConfigTypeDef = TypedDict(
    "OidcIdentityProviderConfigTypeDef",
    {
        "identityProviderConfigName": NotRequired[str],
        "identityProviderConfigArn": NotRequired[str],
        "clusterName": NotRequired[str],
        "issuerUrl": NotRequired[str],
        "clientId": NotRequired[str],
        "usernameClaim": NotRequired[str],
        "usernamePrefix": NotRequired[str],
        "groupsClaim": NotRequired[str],
        "groupsPrefix": NotRequired[str],
        "requiredClaims": NotRequired[Dict[str, str]],
        "tags": NotRequired[Dict[str, str]],
        "status": NotRequired[configStatusType],
    },
)

OIDCTypeDef = TypedDict(
    "OIDCTypeDef",
    {
        "issuer": NotRequired[str],
    },
)

IssueTypeDef = TypedDict(
    "IssueTypeDef",
    {
        "code": NotRequired[NodegroupIssueCodeType],
        "message": NotRequired[str],
        "resourceIds": NotRequired[List[str]],
    },
)

ListAddonsRequestRequestTypeDef = TypedDict(
    "ListAddonsRequestRequestTypeDef",
    {
        "clusterName": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

ListClustersRequestRequestTypeDef = TypedDict(
    "ListClustersRequestRequestTypeDef",
    {
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "include": NotRequired[Sequence[str]],
    },
)

ListFargateProfilesRequestRequestTypeDef = TypedDict(
    "ListFargateProfilesRequestRequestTypeDef",
    {
        "clusterName": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

ListIdentityProviderConfigsRequestRequestTypeDef = TypedDict(
    "ListIdentityProviderConfigsRequestRequestTypeDef",
    {
        "clusterName": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

ListNodegroupsRequestRequestTypeDef = TypedDict(
    "ListNodegroupsRequestRequestTypeDef",
    {
        "clusterName": str,
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

ListUpdatesRequestRequestTypeDef = TypedDict(
    "ListUpdatesRequestRequestTypeDef",
    {
        "name": str,
        "nodegroupName": NotRequired[str],
        "addonName": NotRequired[str],
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)

LogSetupTypeDef = TypedDict(
    "LogSetupTypeDef",
    {
        "types": NotRequired[Sequence[LogTypeType]],
        "enabled": NotRequired[bool],
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

UpdateAddonRequestRequestTypeDef = TypedDict(
    "UpdateAddonRequestRequestTypeDef",
    {
        "clusterName": str,
        "addonName": str,
        "addonVersion": NotRequired[str],
        "serviceAccountRoleArn": NotRequired[str],
        "resolveConflicts": NotRequired[ResolveConflictsType],
        "clientRequestToken": NotRequired[str],
        "configurationValues": NotRequired[str],
    },
)

UpdateClusterVersionRequestRequestTypeDef = TypedDict(
    "UpdateClusterVersionRequestRequestTypeDef",
    {
        "name": str,
        "version": str,
        "clientRequestToken": NotRequired[str],
    },
)

UpdateLabelsPayloadTypeDef = TypedDict(
    "UpdateLabelsPayloadTypeDef",
    {
        "addOrUpdateLabels": NotRequired[Mapping[str, str]],
        "removeLabels": NotRequired[Sequence[str]],
    },
)

UpdateParamTypeDef = TypedDict(
    "UpdateParamTypeDef",
    {
        "type": NotRequired[UpdateParamTypeType],
        "value": NotRequired[str],
    },
)

AddonHealthTypeDef = TypedDict(
    "AddonHealthTypeDef",
    {
        "issues": NotRequired[List[AddonIssueTypeDef]],
    },
)

AddonVersionInfoTypeDef = TypedDict(
    "AddonVersionInfoTypeDef",
    {
        "addonVersion": NotRequired[str],
        "architecture": NotRequired[List[str]],
        "compatibilities": NotRequired[List[CompatibilityTypeDef]],
        "requiresConfiguration": NotRequired[bool],
    },
)

DescribeAddonConfigurationResponseTypeDef = TypedDict(
    "DescribeAddonConfigurationResponseTypeDef",
    {
        "addonName": str,
        "addonVersion": str,
        "configurationSchema": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListAddonsResponseTypeDef = TypedDict(
    "ListAddonsResponseTypeDef",
    {
        "addons": List[str],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListClustersResponseTypeDef = TypedDict(
    "ListClustersResponseTypeDef",
    {
        "clusters": List[str],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListFargateProfilesResponseTypeDef = TypedDict(
    "ListFargateProfilesResponseTypeDef",
    {
        "fargateProfileNames": List[str],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListNodegroupsResponseTypeDef = TypedDict(
    "ListNodegroupsResponseTypeDef",
    {
        "nodegroups": List[str],
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

ListUpdatesResponseTypeDef = TypedDict(
    "ListUpdatesResponseTypeDef",
    {
        "updateIds": List[str],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssociateIdentityProviderConfigRequestRequestTypeDef = TypedDict(
    "AssociateIdentityProviderConfigRequestRequestTypeDef",
    {
        "clusterName": str,
        "oidc": OidcIdentityProviderConfigRequestTypeDef,
        "tags": NotRequired[Mapping[str, str]],
        "clientRequestToken": NotRequired[str],
    },
)

NodegroupResourcesTypeDef = TypedDict(
    "NodegroupResourcesTypeDef",
    {
        "autoScalingGroups": NotRequired[List[AutoScalingGroupTypeDef]],
        "remoteAccessSecurityGroup": NotRequired[str],
    },
)

ClusterHealthTypeDef = TypedDict(
    "ClusterHealthTypeDef",
    {
        "issues": NotRequired[List[ClusterIssueTypeDef]],
    },
)

RegisterClusterRequestRequestTypeDef = TypedDict(
    "RegisterClusterRequestRequestTypeDef",
    {
        "name": str,
        "connectorConfig": ConnectorConfigRequestTypeDef,
        "clientRequestToken": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)

OutpostConfigRequestTypeDef = TypedDict(
    "OutpostConfigRequestTypeDef",
    {
        "outpostArns": Sequence[str],
        "controlPlaneInstanceType": str,
        "controlPlanePlacement": NotRequired[ControlPlanePlacementRequestTypeDef],
    },
)

OutpostConfigResponseTypeDef = TypedDict(
    "OutpostConfigResponseTypeDef",
    {
        "outpostArns": List[str],
        "controlPlaneInstanceType": str,
        "controlPlanePlacement": NotRequired[ControlPlanePlacementResponseTypeDef],
    },
)

CreateFargateProfileRequestRequestTypeDef = TypedDict(
    "CreateFargateProfileRequestRequestTypeDef",
    {
        "fargateProfileName": str,
        "clusterName": str,
        "podExecutionRoleArn": str,
        "subnets": NotRequired[Sequence[str]],
        "selectors": NotRequired[Sequence[FargateProfileSelectorTypeDef]],
        "clientRequestToken": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)

FargateProfileTypeDef = TypedDict(
    "FargateProfileTypeDef",
    {
        "fargateProfileName": NotRequired[str],
        "fargateProfileArn": NotRequired[str],
        "clusterName": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "podExecutionRoleArn": NotRequired[str],
        "subnets": NotRequired[List[str]],
        "selectors": NotRequired[List[FargateProfileSelectorTypeDef]],
        "status": NotRequired[FargateProfileStatusType],
        "tags": NotRequired[Dict[str, str]],
    },
)

UpdateNodegroupVersionRequestRequestTypeDef = TypedDict(
    "UpdateNodegroupVersionRequestRequestTypeDef",
    {
        "clusterName": str,
        "nodegroupName": str,
        "version": NotRequired[str],
        "releaseVersion": NotRequired[str],
        "launchTemplate": NotRequired[LaunchTemplateSpecificationTypeDef],
        "force": NotRequired[bool],
        "clientRequestToken": NotRequired[str],
    },
)

CreateNodegroupRequestRequestTypeDef = TypedDict(
    "CreateNodegroupRequestRequestTypeDef",
    {
        "clusterName": str,
        "nodegroupName": str,
        "subnets": Sequence[str],
        "nodeRole": str,
        "scalingConfig": NotRequired[NodegroupScalingConfigTypeDef],
        "diskSize": NotRequired[int],
        "instanceTypes": NotRequired[Sequence[str]],
        "amiType": NotRequired[AMITypesType],
        "remoteAccess": NotRequired[RemoteAccessConfigTypeDef],
        "labels": NotRequired[Mapping[str, str]],
        "taints": NotRequired[Sequence[TaintTypeDef]],
        "tags": NotRequired[Mapping[str, str]],
        "clientRequestToken": NotRequired[str],
        "launchTemplate": NotRequired[LaunchTemplateSpecificationTypeDef],
        "updateConfig": NotRequired[NodegroupUpdateConfigTypeDef],
        "capacityType": NotRequired[CapacityTypesType],
        "version": NotRequired[str],
        "releaseVersion": NotRequired[str],
    },
)

UpdateTaintsPayloadTypeDef = TypedDict(
    "UpdateTaintsPayloadTypeDef",
    {
        "addOrUpdateTaints": NotRequired[Sequence[TaintTypeDef]],
        "removeTaints": NotRequired[Sequence[TaintTypeDef]],
    },
)

DescribeAddonRequestAddonActiveWaitTypeDef = TypedDict(
    "DescribeAddonRequestAddonActiveWaitTypeDef",
    {
        "clusterName": str,
        "addonName": str,
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)

DescribeAddonRequestAddonDeletedWaitTypeDef = TypedDict(
    "DescribeAddonRequestAddonDeletedWaitTypeDef",
    {
        "clusterName": str,
        "addonName": str,
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)

DescribeClusterRequestClusterActiveWaitTypeDef = TypedDict(
    "DescribeClusterRequestClusterActiveWaitTypeDef",
    {
        "name": str,
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)

DescribeClusterRequestClusterDeletedWaitTypeDef = TypedDict(
    "DescribeClusterRequestClusterDeletedWaitTypeDef",
    {
        "name": str,
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)

DescribeFargateProfileRequestFargateProfileActiveWaitTypeDef = TypedDict(
    "DescribeFargateProfileRequestFargateProfileActiveWaitTypeDef",
    {
        "clusterName": str,
        "fargateProfileName": str,
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)

DescribeFargateProfileRequestFargateProfileDeletedWaitTypeDef = TypedDict(
    "DescribeFargateProfileRequestFargateProfileDeletedWaitTypeDef",
    {
        "clusterName": str,
        "fargateProfileName": str,
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)

DescribeNodegroupRequestNodegroupActiveWaitTypeDef = TypedDict(
    "DescribeNodegroupRequestNodegroupActiveWaitTypeDef",
    {
        "clusterName": str,
        "nodegroupName": str,
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)

DescribeNodegroupRequestNodegroupDeletedWaitTypeDef = TypedDict(
    "DescribeNodegroupRequestNodegroupDeletedWaitTypeDef",
    {
        "clusterName": str,
        "nodegroupName": str,
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)

DescribeAddonVersionsRequestDescribeAddonVersionsPaginateTypeDef = TypedDict(
    "DescribeAddonVersionsRequestDescribeAddonVersionsPaginateTypeDef",
    {
        "kubernetesVersion": NotRequired[str],
        "addonName": NotRequired[str],
        "types": NotRequired[Sequence[str]],
        "publishers": NotRequired[Sequence[str]],
        "owners": NotRequired[Sequence[str]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListAddonsRequestListAddonsPaginateTypeDef = TypedDict(
    "ListAddonsRequestListAddonsPaginateTypeDef",
    {
        "clusterName": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListClustersRequestListClustersPaginateTypeDef = TypedDict(
    "ListClustersRequestListClustersPaginateTypeDef",
    {
        "include": NotRequired[Sequence[str]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListFargateProfilesRequestListFargateProfilesPaginateTypeDef = TypedDict(
    "ListFargateProfilesRequestListFargateProfilesPaginateTypeDef",
    {
        "clusterName": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListIdentityProviderConfigsRequestListIdentityProviderConfigsPaginateTypeDef = TypedDict(
    "ListIdentityProviderConfigsRequestListIdentityProviderConfigsPaginateTypeDef",
    {
        "clusterName": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListNodegroupsRequestListNodegroupsPaginateTypeDef = TypedDict(
    "ListNodegroupsRequestListNodegroupsPaginateTypeDef",
    {
        "clusterName": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListUpdatesRequestListUpdatesPaginateTypeDef = TypedDict(
    "ListUpdatesRequestListUpdatesPaginateTypeDef",
    {
        "name": str,
        "nodegroupName": NotRequired[str],
        "addonName": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

DescribeIdentityProviderConfigRequestRequestTypeDef = TypedDict(
    "DescribeIdentityProviderConfigRequestRequestTypeDef",
    {
        "clusterName": str,
        "identityProviderConfig": IdentityProviderConfigTypeDef,
    },
)

DisassociateIdentityProviderConfigRequestRequestTypeDef = TypedDict(
    "DisassociateIdentityProviderConfigRequestRequestTypeDef",
    {
        "clusterName": str,
        "identityProviderConfig": IdentityProviderConfigTypeDef,
        "clientRequestToken": NotRequired[str],
    },
)

ListIdentityProviderConfigsResponseTypeDef = TypedDict(
    "ListIdentityProviderConfigsResponseTypeDef",
    {
        "identityProviderConfigs": List[IdentityProviderConfigTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EncryptionConfigTypeDef = TypedDict(
    "EncryptionConfigTypeDef",
    {
        "resources": NotRequired[Sequence[str]],
        "provider": NotRequired[ProviderTypeDef],
    },
)

IdentityProviderConfigResponseTypeDef = TypedDict(
    "IdentityProviderConfigResponseTypeDef",
    {
        "oidc": NotRequired[OidcIdentityProviderConfigTypeDef],
    },
)

IdentityTypeDef = TypedDict(
    "IdentityTypeDef",
    {
        "oidc": NotRequired[OIDCTypeDef],
    },
)

NodegroupHealthTypeDef = TypedDict(
    "NodegroupHealthTypeDef",
    {
        "issues": NotRequired[List[IssueTypeDef]],
    },
)

LoggingTypeDef = TypedDict(
    "LoggingTypeDef",
    {
        "clusterLogging": NotRequired[Sequence[LogSetupTypeDef]],
    },
)

UpdateTypeDef = TypedDict(
    "UpdateTypeDef",
    {
        "id": NotRequired[str],
        "status": NotRequired[UpdateStatusType],
        "type": NotRequired[UpdateTypeType],
        "params": NotRequired[List[UpdateParamTypeDef]],
        "createdAt": NotRequired[datetime],
        "errors": NotRequired[List[ErrorDetailTypeDef]],
    },
)

AddonTypeDef = TypedDict(
    "AddonTypeDef",
    {
        "addonName": NotRequired[str],
        "clusterName": NotRequired[str],
        "status": NotRequired[AddonStatusType],
        "addonVersion": NotRequired[str],
        "health": NotRequired[AddonHealthTypeDef],
        "addonArn": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "modifiedAt": NotRequired[datetime],
        "serviceAccountRoleArn": NotRequired[str],
        "tags": NotRequired[Dict[str, str]],
        "publisher": NotRequired[str],
        "owner": NotRequired[str],
        "marketplaceInformation": NotRequired[MarketplaceInformationTypeDef],
        "configurationValues": NotRequired[str],
    },
)

AddonInfoTypeDef = TypedDict(
    "AddonInfoTypeDef",
    {
        "addonName": NotRequired[str],
        "type": NotRequired[str],
        "addonVersions": NotRequired[List[AddonVersionInfoTypeDef]],
        "publisher": NotRequired[str],
        "owner": NotRequired[str],
        "marketplaceInformation": NotRequired[MarketplaceInformationTypeDef],
    },
)

CreateFargateProfileResponseTypeDef = TypedDict(
    "CreateFargateProfileResponseTypeDef",
    {
        "fargateProfile": FargateProfileTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteFargateProfileResponseTypeDef = TypedDict(
    "DeleteFargateProfileResponseTypeDef",
    {
        "fargateProfile": FargateProfileTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeFargateProfileResponseTypeDef = TypedDict(
    "DescribeFargateProfileResponseTypeDef",
    {
        "fargateProfile": FargateProfileTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateNodegroupConfigRequestRequestTypeDef = TypedDict(
    "UpdateNodegroupConfigRequestRequestTypeDef",
    {
        "clusterName": str,
        "nodegroupName": str,
        "labels": NotRequired[UpdateLabelsPayloadTypeDef],
        "taints": NotRequired[UpdateTaintsPayloadTypeDef],
        "scalingConfig": NotRequired[NodegroupScalingConfigTypeDef],
        "updateConfig": NotRequired[NodegroupUpdateConfigTypeDef],
        "clientRequestToken": NotRequired[str],
    },
)

AssociateEncryptionConfigRequestRequestTypeDef = TypedDict(
    "AssociateEncryptionConfigRequestRequestTypeDef",
    {
        "clusterName": str,
        "encryptionConfig": Sequence[EncryptionConfigTypeDef],
        "clientRequestToken": NotRequired[str],
    },
)

DescribeIdentityProviderConfigResponseTypeDef = TypedDict(
    "DescribeIdentityProviderConfigResponseTypeDef",
    {
        "identityProviderConfig": IdentityProviderConfigResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

NodegroupTypeDef = TypedDict(
    "NodegroupTypeDef",
    {
        "nodegroupName": NotRequired[str],
        "nodegroupArn": NotRequired[str],
        "clusterName": NotRequired[str],
        "version": NotRequired[str],
        "releaseVersion": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "modifiedAt": NotRequired[datetime],
        "status": NotRequired[NodegroupStatusType],
        "capacityType": NotRequired[CapacityTypesType],
        "scalingConfig": NotRequired[NodegroupScalingConfigTypeDef],
        "instanceTypes": NotRequired[List[str]],
        "subnets": NotRequired[List[str]],
        "remoteAccess": NotRequired[RemoteAccessConfigTypeDef],
        "amiType": NotRequired[AMITypesType],
        "nodeRole": NotRequired[str],
        "labels": NotRequired[Dict[str, str]],
        "taints": NotRequired[List[TaintTypeDef]],
        "resources": NotRequired[NodegroupResourcesTypeDef],
        "diskSize": NotRequired[int],
        "health": NotRequired[NodegroupHealthTypeDef],
        "updateConfig": NotRequired[NodegroupUpdateConfigTypeDef],
        "launchTemplate": NotRequired[LaunchTemplateSpecificationTypeDef],
        "tags": NotRequired[Dict[str, str]],
    },
)

ClusterTypeDef = TypedDict(
    "ClusterTypeDef",
    {
        "name": NotRequired[str],
        "arn": NotRequired[str],
        "createdAt": NotRequired[datetime],
        "version": NotRequired[str],
        "endpoint": NotRequired[str],
        "roleArn": NotRequired[str],
        "resourcesVpcConfig": NotRequired[VpcConfigResponseTypeDef],
        "kubernetesNetworkConfig": NotRequired[KubernetesNetworkConfigResponseTypeDef],
        "logging": NotRequired[LoggingTypeDef],
        "identity": NotRequired[IdentityTypeDef],
        "status": NotRequired[ClusterStatusType],
        "certificateAuthority": NotRequired[CertificateTypeDef],
        "clientRequestToken": NotRequired[str],
        "platformVersion": NotRequired[str],
        "tags": NotRequired[Dict[str, str]],
        "encryptionConfig": NotRequired[List[EncryptionConfigTypeDef]],
        "connectorConfig": NotRequired[ConnectorConfigResponseTypeDef],
        "id": NotRequired[str],
        "health": NotRequired[ClusterHealthTypeDef],
        "outpostConfig": NotRequired[OutpostConfigResponseTypeDef],
    },
)

CreateClusterRequestRequestTypeDef = TypedDict(
    "CreateClusterRequestRequestTypeDef",
    {
        "name": str,
        "roleArn": str,
        "resourcesVpcConfig": VpcConfigRequestTypeDef,
        "version": NotRequired[str],
        "kubernetesNetworkConfig": NotRequired[KubernetesNetworkConfigRequestTypeDef],
        "logging": NotRequired[LoggingTypeDef],
        "clientRequestToken": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
        "encryptionConfig": NotRequired[Sequence[EncryptionConfigTypeDef]],
        "outpostConfig": NotRequired[OutpostConfigRequestTypeDef],
    },
)

UpdateClusterConfigRequestRequestTypeDef = TypedDict(
    "UpdateClusterConfigRequestRequestTypeDef",
    {
        "name": str,
        "resourcesVpcConfig": NotRequired[VpcConfigRequestTypeDef],
        "logging": NotRequired[LoggingTypeDef],
        "clientRequestToken": NotRequired[str],
    },
)

AssociateEncryptionConfigResponseTypeDef = TypedDict(
    "AssociateEncryptionConfigResponseTypeDef",
    {
        "update": UpdateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

AssociateIdentityProviderConfigResponseTypeDef = TypedDict(
    "AssociateIdentityProviderConfigResponseTypeDef",
    {
        "update": UpdateTypeDef,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeUpdateResponseTypeDef = TypedDict(
    "DescribeUpdateResponseTypeDef",
    {
        "update": UpdateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DisassociateIdentityProviderConfigResponseTypeDef = TypedDict(
    "DisassociateIdentityProviderConfigResponseTypeDef",
    {
        "update": UpdateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAddonResponseTypeDef = TypedDict(
    "UpdateAddonResponseTypeDef",
    {
        "update": UpdateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateClusterConfigResponseTypeDef = TypedDict(
    "UpdateClusterConfigResponseTypeDef",
    {
        "update": UpdateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateClusterVersionResponseTypeDef = TypedDict(
    "UpdateClusterVersionResponseTypeDef",
    {
        "update": UpdateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateNodegroupConfigResponseTypeDef = TypedDict(
    "UpdateNodegroupConfigResponseTypeDef",
    {
        "update": UpdateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateNodegroupVersionResponseTypeDef = TypedDict(
    "UpdateNodegroupVersionResponseTypeDef",
    {
        "update": UpdateTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAddonResponseTypeDef = TypedDict(
    "CreateAddonResponseTypeDef",
    {
        "addon": AddonTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteAddonResponseTypeDef = TypedDict(
    "DeleteAddonResponseTypeDef",
    {
        "addon": AddonTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAddonResponseTypeDef = TypedDict(
    "DescribeAddonResponseTypeDef",
    {
        "addon": AddonTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAddonVersionsResponseTypeDef = TypedDict(
    "DescribeAddonVersionsResponseTypeDef",
    {
        "addons": List[AddonInfoTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateNodegroupResponseTypeDef = TypedDict(
    "CreateNodegroupResponseTypeDef",
    {
        "nodegroup": NodegroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteNodegroupResponseTypeDef = TypedDict(
    "DeleteNodegroupResponseTypeDef",
    {
        "nodegroup": NodegroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeNodegroupResponseTypeDef = TypedDict(
    "DescribeNodegroupResponseTypeDef",
    {
        "nodegroup": NodegroupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateClusterResponseTypeDef = TypedDict(
    "CreateClusterResponseTypeDef",
    {
        "cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteClusterResponseTypeDef = TypedDict(
    "DeleteClusterResponseTypeDef",
    {
        "cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeregisterClusterResponseTypeDef = TypedDict(
    "DeregisterClusterResponseTypeDef",
    {
        "cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeClusterResponseTypeDef = TypedDict(
    "DescribeClusterResponseTypeDef",
    {
        "cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RegisterClusterResponseTypeDef = TypedDict(
    "RegisterClusterResponseTypeDef",
    {
        "cluster": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
