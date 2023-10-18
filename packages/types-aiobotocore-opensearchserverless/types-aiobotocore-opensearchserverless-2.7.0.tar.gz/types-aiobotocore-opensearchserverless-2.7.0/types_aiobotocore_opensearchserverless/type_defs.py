"""
Type annotations for opensearchserverless service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearchserverless/type_defs/)

Usage::

    ```python
    from types_aiobotocore_opensearchserverless.type_defs import AccessPolicyDetailTypeDef

    data: AccessPolicyDetailTypeDef = ...
    ```
"""

import sys
from typing import Any, Dict, List, Sequence

from .literals import (
    CollectionStatusType,
    CollectionTypeType,
    SecurityPolicyTypeType,
    VpcEndpointStatusType,
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
    "AccessPolicyDetailTypeDef",
    "AccessPolicyStatsTypeDef",
    "AccessPolicySummaryTypeDef",
    "CapacityLimitsTypeDef",
    "BatchGetCollectionRequestRequestTypeDef",
    "CollectionDetailTypeDef",
    "CollectionErrorDetailTypeDef",
    "ResponseMetadataTypeDef",
    "BatchGetVpcEndpointRequestRequestTypeDef",
    "VpcEndpointDetailTypeDef",
    "VpcEndpointErrorDetailTypeDef",
    "CollectionFiltersTypeDef",
    "CollectionSummaryTypeDef",
    "CreateAccessPolicyRequestRequestTypeDef",
    "CreateCollectionDetailTypeDef",
    "TagTypeDef",
    "SamlConfigOptionsTypeDef",
    "CreateSecurityPolicyRequestRequestTypeDef",
    "SecurityPolicyDetailTypeDef",
    "CreateVpcEndpointDetailTypeDef",
    "CreateVpcEndpointRequestRequestTypeDef",
    "DeleteAccessPolicyRequestRequestTypeDef",
    "DeleteCollectionDetailTypeDef",
    "DeleteCollectionRequestRequestTypeDef",
    "DeleteSecurityConfigRequestRequestTypeDef",
    "DeleteSecurityPolicyRequestRequestTypeDef",
    "DeleteVpcEndpointDetailTypeDef",
    "DeleteVpcEndpointRequestRequestTypeDef",
    "GetAccessPolicyRequestRequestTypeDef",
    "SecurityConfigStatsTypeDef",
    "SecurityPolicyStatsTypeDef",
    "GetSecurityConfigRequestRequestTypeDef",
    "GetSecurityPolicyRequestRequestTypeDef",
    "ListAccessPoliciesRequestRequestTypeDef",
    "ListSecurityConfigsRequestRequestTypeDef",
    "SecurityConfigSummaryTypeDef",
    "ListSecurityPoliciesRequestRequestTypeDef",
    "SecurityPolicySummaryTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "VpcEndpointFiltersTypeDef",
    "VpcEndpointSummaryTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateAccessPolicyRequestRequestTypeDef",
    "UpdateCollectionDetailTypeDef",
    "UpdateCollectionRequestRequestTypeDef",
    "UpdateSecurityPolicyRequestRequestTypeDef",
    "UpdateVpcEndpointDetailTypeDef",
    "UpdateVpcEndpointRequestRequestTypeDef",
    "AccountSettingsDetailTypeDef",
    "UpdateAccountSettingsRequestRequestTypeDef",
    "BatchGetCollectionResponseTypeDef",
    "CreateAccessPolicyResponseTypeDef",
    "GetAccessPolicyResponseTypeDef",
    "ListAccessPoliciesResponseTypeDef",
    "UpdateAccessPolicyResponseTypeDef",
    "BatchGetVpcEndpointResponseTypeDef",
    "ListCollectionsRequestRequestTypeDef",
    "ListCollectionsResponseTypeDef",
    "CreateCollectionResponseTypeDef",
    "CreateCollectionRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CreateSecurityConfigRequestRequestTypeDef",
    "SecurityConfigDetailTypeDef",
    "UpdateSecurityConfigRequestRequestTypeDef",
    "CreateSecurityPolicyResponseTypeDef",
    "GetSecurityPolicyResponseTypeDef",
    "UpdateSecurityPolicyResponseTypeDef",
    "CreateVpcEndpointResponseTypeDef",
    "DeleteCollectionResponseTypeDef",
    "DeleteVpcEndpointResponseTypeDef",
    "GetPoliciesStatsResponseTypeDef",
    "ListSecurityConfigsResponseTypeDef",
    "ListSecurityPoliciesResponseTypeDef",
    "ListVpcEndpointsRequestRequestTypeDef",
    "ListVpcEndpointsResponseTypeDef",
    "UpdateCollectionResponseTypeDef",
    "UpdateVpcEndpointResponseTypeDef",
    "GetAccountSettingsResponseTypeDef",
    "UpdateAccountSettingsResponseTypeDef",
    "CreateSecurityConfigResponseTypeDef",
    "GetSecurityConfigResponseTypeDef",
    "UpdateSecurityConfigResponseTypeDef",
)

AccessPolicyDetailTypeDef = TypedDict(
    "AccessPolicyDetailTypeDef",
    {
        "createdDate": NotRequired[int],
        "description": NotRequired[str],
        "lastModifiedDate": NotRequired[int],
        "name": NotRequired[str],
        "policy": NotRequired[Dict[str, Any]],
        "policyVersion": NotRequired[str],
        "type": NotRequired[Literal["data"]],
    },
)

AccessPolicyStatsTypeDef = TypedDict(
    "AccessPolicyStatsTypeDef",
    {
        "DataPolicyCount": NotRequired[int],
    },
)

AccessPolicySummaryTypeDef = TypedDict(
    "AccessPolicySummaryTypeDef",
    {
        "createdDate": NotRequired[int],
        "description": NotRequired[str],
        "lastModifiedDate": NotRequired[int],
        "name": NotRequired[str],
        "policyVersion": NotRequired[str],
        "type": NotRequired[Literal["data"]],
    },
)

CapacityLimitsTypeDef = TypedDict(
    "CapacityLimitsTypeDef",
    {
        "maxIndexingCapacityInOCU": NotRequired[int],
        "maxSearchCapacityInOCU": NotRequired[int],
    },
)

BatchGetCollectionRequestRequestTypeDef = TypedDict(
    "BatchGetCollectionRequestRequestTypeDef",
    {
        "ids": NotRequired[Sequence[str]],
        "names": NotRequired[Sequence[str]],
    },
)

CollectionDetailTypeDef = TypedDict(
    "CollectionDetailTypeDef",
    {
        "arn": NotRequired[str],
        "collectionEndpoint": NotRequired[str],
        "createdDate": NotRequired[int],
        "dashboardEndpoint": NotRequired[str],
        "description": NotRequired[str],
        "id": NotRequired[str],
        "kmsKeyArn": NotRequired[str],
        "lastModifiedDate": NotRequired[int],
        "name": NotRequired[str],
        "status": NotRequired[CollectionStatusType],
        "type": NotRequired[CollectionTypeType],
    },
)

CollectionErrorDetailTypeDef = TypedDict(
    "CollectionErrorDetailTypeDef",
    {
        "errorCode": NotRequired[str],
        "errorMessage": NotRequired[str],
        "id": NotRequired[str],
        "name": NotRequired[str],
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

BatchGetVpcEndpointRequestRequestTypeDef = TypedDict(
    "BatchGetVpcEndpointRequestRequestTypeDef",
    {
        "ids": Sequence[str],
    },
)

VpcEndpointDetailTypeDef = TypedDict(
    "VpcEndpointDetailTypeDef",
    {
        "createdDate": NotRequired[int],
        "id": NotRequired[str],
        "name": NotRequired[str],
        "securityGroupIds": NotRequired[List[str]],
        "status": NotRequired[VpcEndpointStatusType],
        "subnetIds": NotRequired[List[str]],
        "vpcId": NotRequired[str],
    },
)

VpcEndpointErrorDetailTypeDef = TypedDict(
    "VpcEndpointErrorDetailTypeDef",
    {
        "errorCode": NotRequired[str],
        "errorMessage": NotRequired[str],
        "id": NotRequired[str],
    },
)

CollectionFiltersTypeDef = TypedDict(
    "CollectionFiltersTypeDef",
    {
        "name": NotRequired[str],
        "status": NotRequired[CollectionStatusType],
    },
)

CollectionSummaryTypeDef = TypedDict(
    "CollectionSummaryTypeDef",
    {
        "arn": NotRequired[str],
        "id": NotRequired[str],
        "name": NotRequired[str],
        "status": NotRequired[CollectionStatusType],
    },
)

CreateAccessPolicyRequestRequestTypeDef = TypedDict(
    "CreateAccessPolicyRequestRequestTypeDef",
    {
        "name": str,
        "policy": str,
        "type": Literal["data"],
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
    },
)

CreateCollectionDetailTypeDef = TypedDict(
    "CreateCollectionDetailTypeDef",
    {
        "arn": NotRequired[str],
        "createdDate": NotRequired[int],
        "description": NotRequired[str],
        "id": NotRequired[str],
        "kmsKeyArn": NotRequired[str],
        "lastModifiedDate": NotRequired[int],
        "name": NotRequired[str],
        "status": NotRequired[CollectionStatusType],
        "type": NotRequired[CollectionTypeType],
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "key": str,
        "value": str,
    },
)

SamlConfigOptionsTypeDef = TypedDict(
    "SamlConfigOptionsTypeDef",
    {
        "metadata": str,
        "groupAttribute": NotRequired[str],
        "sessionTimeout": NotRequired[int],
        "userAttribute": NotRequired[str],
    },
)

CreateSecurityPolicyRequestRequestTypeDef = TypedDict(
    "CreateSecurityPolicyRequestRequestTypeDef",
    {
        "name": str,
        "policy": str,
        "type": SecurityPolicyTypeType,
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
    },
)

SecurityPolicyDetailTypeDef = TypedDict(
    "SecurityPolicyDetailTypeDef",
    {
        "createdDate": NotRequired[int],
        "description": NotRequired[str],
        "lastModifiedDate": NotRequired[int],
        "name": NotRequired[str],
        "policy": NotRequired[Dict[str, Any]],
        "policyVersion": NotRequired[str],
        "type": NotRequired[SecurityPolicyTypeType],
    },
)

CreateVpcEndpointDetailTypeDef = TypedDict(
    "CreateVpcEndpointDetailTypeDef",
    {
        "id": NotRequired[str],
        "name": NotRequired[str],
        "status": NotRequired[VpcEndpointStatusType],
    },
)

CreateVpcEndpointRequestRequestTypeDef = TypedDict(
    "CreateVpcEndpointRequestRequestTypeDef",
    {
        "name": str,
        "subnetIds": Sequence[str],
        "vpcId": str,
        "clientToken": NotRequired[str],
        "securityGroupIds": NotRequired[Sequence[str]],
    },
)

DeleteAccessPolicyRequestRequestTypeDef = TypedDict(
    "DeleteAccessPolicyRequestRequestTypeDef",
    {
        "name": str,
        "type": Literal["data"],
        "clientToken": NotRequired[str],
    },
)

DeleteCollectionDetailTypeDef = TypedDict(
    "DeleteCollectionDetailTypeDef",
    {
        "id": NotRequired[str],
        "name": NotRequired[str],
        "status": NotRequired[CollectionStatusType],
    },
)

DeleteCollectionRequestRequestTypeDef = TypedDict(
    "DeleteCollectionRequestRequestTypeDef",
    {
        "id": str,
        "clientToken": NotRequired[str],
    },
)

DeleteSecurityConfigRequestRequestTypeDef = TypedDict(
    "DeleteSecurityConfigRequestRequestTypeDef",
    {
        "id": str,
        "clientToken": NotRequired[str],
    },
)

DeleteSecurityPolicyRequestRequestTypeDef = TypedDict(
    "DeleteSecurityPolicyRequestRequestTypeDef",
    {
        "name": str,
        "type": SecurityPolicyTypeType,
        "clientToken": NotRequired[str],
    },
)

DeleteVpcEndpointDetailTypeDef = TypedDict(
    "DeleteVpcEndpointDetailTypeDef",
    {
        "id": NotRequired[str],
        "name": NotRequired[str],
        "status": NotRequired[VpcEndpointStatusType],
    },
)

DeleteVpcEndpointRequestRequestTypeDef = TypedDict(
    "DeleteVpcEndpointRequestRequestTypeDef",
    {
        "id": str,
        "clientToken": NotRequired[str],
    },
)

GetAccessPolicyRequestRequestTypeDef = TypedDict(
    "GetAccessPolicyRequestRequestTypeDef",
    {
        "name": str,
        "type": Literal["data"],
    },
)

SecurityConfigStatsTypeDef = TypedDict(
    "SecurityConfigStatsTypeDef",
    {
        "SamlConfigCount": NotRequired[int],
    },
)

SecurityPolicyStatsTypeDef = TypedDict(
    "SecurityPolicyStatsTypeDef",
    {
        "EncryptionPolicyCount": NotRequired[int],
        "NetworkPolicyCount": NotRequired[int],
    },
)

GetSecurityConfigRequestRequestTypeDef = TypedDict(
    "GetSecurityConfigRequestRequestTypeDef",
    {
        "id": str,
    },
)

GetSecurityPolicyRequestRequestTypeDef = TypedDict(
    "GetSecurityPolicyRequestRequestTypeDef",
    {
        "name": str,
        "type": SecurityPolicyTypeType,
    },
)

ListAccessPoliciesRequestRequestTypeDef = TypedDict(
    "ListAccessPoliciesRequestRequestTypeDef",
    {
        "type": Literal["data"],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "resource": NotRequired[Sequence[str]],
    },
)

ListSecurityConfigsRequestRequestTypeDef = TypedDict(
    "ListSecurityConfigsRequestRequestTypeDef",
    {
        "type": Literal["saml"],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

SecurityConfigSummaryTypeDef = TypedDict(
    "SecurityConfigSummaryTypeDef",
    {
        "configVersion": NotRequired[str],
        "createdDate": NotRequired[int],
        "description": NotRequired[str],
        "id": NotRequired[str],
        "lastModifiedDate": NotRequired[int],
        "type": NotRequired[Literal["saml"]],
    },
)

ListSecurityPoliciesRequestRequestTypeDef = TypedDict(
    "ListSecurityPoliciesRequestRequestTypeDef",
    {
        "type": SecurityPolicyTypeType,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "resource": NotRequired[Sequence[str]],
    },
)

SecurityPolicySummaryTypeDef = TypedDict(
    "SecurityPolicySummaryTypeDef",
    {
        "createdDate": NotRequired[int],
        "description": NotRequired[str],
        "lastModifiedDate": NotRequired[int],
        "name": NotRequired[str],
        "policyVersion": NotRequired[str],
        "type": NotRequired[SecurityPolicyTypeType],
    },
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

VpcEndpointFiltersTypeDef = TypedDict(
    "VpcEndpointFiltersTypeDef",
    {
        "status": NotRequired[VpcEndpointStatusType],
    },
)

VpcEndpointSummaryTypeDef = TypedDict(
    "VpcEndpointSummaryTypeDef",
    {
        "id": NotRequired[str],
        "name": NotRequired[str],
        "status": NotRequired[VpcEndpointStatusType],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

UpdateAccessPolicyRequestRequestTypeDef = TypedDict(
    "UpdateAccessPolicyRequestRequestTypeDef",
    {
        "name": str,
        "policyVersion": str,
        "type": Literal["data"],
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "policy": NotRequired[str],
    },
)

UpdateCollectionDetailTypeDef = TypedDict(
    "UpdateCollectionDetailTypeDef",
    {
        "arn": NotRequired[str],
        "createdDate": NotRequired[int],
        "description": NotRequired[str],
        "id": NotRequired[str],
        "lastModifiedDate": NotRequired[int],
        "name": NotRequired[str],
        "status": NotRequired[CollectionStatusType],
        "type": NotRequired[CollectionTypeType],
    },
)

UpdateCollectionRequestRequestTypeDef = TypedDict(
    "UpdateCollectionRequestRequestTypeDef",
    {
        "id": str,
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
    },
)

UpdateSecurityPolicyRequestRequestTypeDef = TypedDict(
    "UpdateSecurityPolicyRequestRequestTypeDef",
    {
        "name": str,
        "policyVersion": str,
        "type": SecurityPolicyTypeType,
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "policy": NotRequired[str],
    },
)

UpdateVpcEndpointDetailTypeDef = TypedDict(
    "UpdateVpcEndpointDetailTypeDef",
    {
        "id": NotRequired[str],
        "lastModifiedDate": NotRequired[int],
        "name": NotRequired[str],
        "securityGroupIds": NotRequired[List[str]],
        "status": NotRequired[VpcEndpointStatusType],
        "subnetIds": NotRequired[List[str]],
    },
)

UpdateVpcEndpointRequestRequestTypeDef = TypedDict(
    "UpdateVpcEndpointRequestRequestTypeDef",
    {
        "id": str,
        "addSecurityGroupIds": NotRequired[Sequence[str]],
        "addSubnetIds": NotRequired[Sequence[str]],
        "clientToken": NotRequired[str],
        "removeSecurityGroupIds": NotRequired[Sequence[str]],
        "removeSubnetIds": NotRequired[Sequence[str]],
    },
)

AccountSettingsDetailTypeDef = TypedDict(
    "AccountSettingsDetailTypeDef",
    {
        "capacityLimits": NotRequired[CapacityLimitsTypeDef],
    },
)

UpdateAccountSettingsRequestRequestTypeDef = TypedDict(
    "UpdateAccountSettingsRequestRequestTypeDef",
    {
        "capacityLimits": NotRequired[CapacityLimitsTypeDef],
    },
)

BatchGetCollectionResponseTypeDef = TypedDict(
    "BatchGetCollectionResponseTypeDef",
    {
        "collectionDetails": List[CollectionDetailTypeDef],
        "collectionErrorDetails": List[CollectionErrorDetailTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateAccessPolicyResponseTypeDef = TypedDict(
    "CreateAccessPolicyResponseTypeDef",
    {
        "accessPolicyDetail": AccessPolicyDetailTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAccessPolicyResponseTypeDef = TypedDict(
    "GetAccessPolicyResponseTypeDef",
    {
        "accessPolicyDetail": AccessPolicyDetailTypeDef,
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

UpdateAccessPolicyResponseTypeDef = TypedDict(
    "UpdateAccessPolicyResponseTypeDef",
    {
        "accessPolicyDetail": AccessPolicyDetailTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchGetVpcEndpointResponseTypeDef = TypedDict(
    "BatchGetVpcEndpointResponseTypeDef",
    {
        "vpcEndpointDetails": List[VpcEndpointDetailTypeDef],
        "vpcEndpointErrorDetails": List[VpcEndpointErrorDetailTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListCollectionsRequestRequestTypeDef = TypedDict(
    "ListCollectionsRequestRequestTypeDef",
    {
        "collectionFilters": NotRequired[CollectionFiltersTypeDef],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

ListCollectionsResponseTypeDef = TypedDict(
    "ListCollectionsResponseTypeDef",
    {
        "collectionSummaries": List[CollectionSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateCollectionResponseTypeDef = TypedDict(
    "CreateCollectionResponseTypeDef",
    {
        "createCollectionDetail": CreateCollectionDetailTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateCollectionRequestRequestTypeDef = TypedDict(
    "CreateCollectionRequestRequestTypeDef",
    {
        "name": str,
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "tags": NotRequired[Sequence[TagTypeDef]],
        "type": NotRequired[CollectionTypeType],
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Sequence[TagTypeDef],
    },
)

CreateSecurityConfigRequestRequestTypeDef = TypedDict(
    "CreateSecurityConfigRequestRequestTypeDef",
    {
        "name": str,
        "type": Literal["saml"],
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "samlOptions": NotRequired[SamlConfigOptionsTypeDef],
    },
)

SecurityConfigDetailTypeDef = TypedDict(
    "SecurityConfigDetailTypeDef",
    {
        "configVersion": NotRequired[str],
        "createdDate": NotRequired[int],
        "description": NotRequired[str],
        "id": NotRequired[str],
        "lastModifiedDate": NotRequired[int],
        "samlOptions": NotRequired[SamlConfigOptionsTypeDef],
        "type": NotRequired[Literal["saml"]],
    },
)

UpdateSecurityConfigRequestRequestTypeDef = TypedDict(
    "UpdateSecurityConfigRequestRequestTypeDef",
    {
        "configVersion": str,
        "id": str,
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "samlOptions": NotRequired[SamlConfigOptionsTypeDef],
    },
)

CreateSecurityPolicyResponseTypeDef = TypedDict(
    "CreateSecurityPolicyResponseTypeDef",
    {
        "securityPolicyDetail": SecurityPolicyDetailTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSecurityPolicyResponseTypeDef = TypedDict(
    "GetSecurityPolicyResponseTypeDef",
    {
        "securityPolicyDetail": SecurityPolicyDetailTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateSecurityPolicyResponseTypeDef = TypedDict(
    "UpdateSecurityPolicyResponseTypeDef",
    {
        "securityPolicyDetail": SecurityPolicyDetailTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateVpcEndpointResponseTypeDef = TypedDict(
    "CreateVpcEndpointResponseTypeDef",
    {
        "createVpcEndpointDetail": CreateVpcEndpointDetailTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteCollectionResponseTypeDef = TypedDict(
    "DeleteCollectionResponseTypeDef",
    {
        "deleteCollectionDetail": DeleteCollectionDetailTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteVpcEndpointResponseTypeDef = TypedDict(
    "DeleteVpcEndpointResponseTypeDef",
    {
        "deleteVpcEndpointDetail": DeleteVpcEndpointDetailTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetPoliciesStatsResponseTypeDef = TypedDict(
    "GetPoliciesStatsResponseTypeDef",
    {
        "AccessPolicyStats": AccessPolicyStatsTypeDef,
        "SecurityConfigStats": SecurityConfigStatsTypeDef,
        "SecurityPolicyStats": SecurityPolicyStatsTypeDef,
        "TotalPolicyCount": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSecurityConfigsResponseTypeDef = TypedDict(
    "ListSecurityConfigsResponseTypeDef",
    {
        "nextToken": str,
        "securityConfigSummaries": List[SecurityConfigSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListSecurityPoliciesResponseTypeDef = TypedDict(
    "ListSecurityPoliciesResponseTypeDef",
    {
        "nextToken": str,
        "securityPolicySummaries": List[SecurityPolicySummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListVpcEndpointsRequestRequestTypeDef = TypedDict(
    "ListVpcEndpointsRequestRequestTypeDef",
    {
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "vpcEndpointFilters": NotRequired[VpcEndpointFiltersTypeDef],
    },
)

ListVpcEndpointsResponseTypeDef = TypedDict(
    "ListVpcEndpointsResponseTypeDef",
    {
        "nextToken": str,
        "vpcEndpointSummaries": List[VpcEndpointSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateCollectionResponseTypeDef = TypedDict(
    "UpdateCollectionResponseTypeDef",
    {
        "updateCollectionDetail": UpdateCollectionDetailTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateVpcEndpointResponseTypeDef = TypedDict(
    "UpdateVpcEndpointResponseTypeDef",
    {
        "UpdateVpcEndpointDetail": UpdateVpcEndpointDetailTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetAccountSettingsResponseTypeDef = TypedDict(
    "GetAccountSettingsResponseTypeDef",
    {
        "accountSettingsDetail": AccountSettingsDetailTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateAccountSettingsResponseTypeDef = TypedDict(
    "UpdateAccountSettingsResponseTypeDef",
    {
        "accountSettingsDetail": AccountSettingsDetailTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateSecurityConfigResponseTypeDef = TypedDict(
    "CreateSecurityConfigResponseTypeDef",
    {
        "securityConfigDetail": SecurityConfigDetailTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetSecurityConfigResponseTypeDef = TypedDict(
    "GetSecurityConfigResponseTypeDef",
    {
        "securityConfigDetail": SecurityConfigDetailTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateSecurityConfigResponseTypeDef = TypedDict(
    "UpdateSecurityConfigResponseTypeDef",
    {
        "securityConfigDetail": SecurityConfigDetailTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
