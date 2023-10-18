"""
Type annotations for kafka service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kafka/type_defs/)

Usage::

    ```python
    from types_aiobotocore_kafka.type_defs import BatchAssociateScramSecretRequestRequestTypeDef

    data: BatchAssociateScramSecretRequestRequestTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from aiobotocore.response import StreamingBody

from .literals import (
    ClientBrokerType,
    ClusterStateType,
    ClusterTypeType,
    ConfigurationStateType,
    EnhancedMonitoringType,
    KafkaVersionStatusType,
    StorageModeType,
    UserIdentityTypeType,
    VpcConnectionStateType,
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
    "BatchAssociateScramSecretRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "UnprocessedScramSecretTypeDef",
    "BatchDisassociateScramSecretRequestRequestTypeDef",
    "BlobTypeDef",
    "ProvisionedThroughputTypeDef",
    "CloudWatchLogsTypeDef",
    "FirehoseTypeDef",
    "S3TypeDef",
    "BrokerSoftwareInfoTypeDef",
    "TlsPaginatorTypeDef",
    "UnauthenticatedTypeDef",
    "TlsTypeDef",
    "ClientVpcConnectionTypeDef",
    "StateInfoTypeDef",
    "ErrorInfoTypeDef",
    "ClusterOperationStepInfoTypeDef",
    "ClusterOperationV2SummaryTypeDef",
    "CompatibleKafkaVersionTypeDef",
    "ConfigurationInfoTypeDef",
    "ConfigurationRevisionTypeDef",
    "PublicAccessTypeDef",
    "CreateVpcConnectionRequestRequestTypeDef",
    "DeleteClusterPolicyRequestRequestTypeDef",
    "DeleteClusterRequestRequestTypeDef",
    "DeleteConfigurationRequestRequestTypeDef",
    "DeleteVpcConnectionRequestRequestTypeDef",
    "DescribeClusterOperationRequestRequestTypeDef",
    "DescribeClusterOperationV2RequestRequestTypeDef",
    "DescribeClusterRequestRequestTypeDef",
    "DescribeClusterV2RequestRequestTypeDef",
    "DescribeConfigurationRequestRequestTypeDef",
    "DescribeConfigurationRevisionRequestRequestTypeDef",
    "DescribeVpcConnectionRequestRequestTypeDef",
    "EncryptionAtRestTypeDef",
    "EncryptionInTransitTypeDef",
    "GetBootstrapBrokersRequestRequestTypeDef",
    "GetClusterPolicyRequestRequestTypeDef",
    "GetCompatibleKafkaVersionsRequestRequestTypeDef",
    "IamTypeDef",
    "JmxExporterInfoTypeDef",
    "JmxExporterTypeDef",
    "KafkaVersionTypeDef",
    "PaginatorConfigTypeDef",
    "ListClientVpcConnectionsRequestRequestTypeDef",
    "ListClusterOperationsRequestRequestTypeDef",
    "ListClusterOperationsV2RequestRequestTypeDef",
    "ListClustersRequestRequestTypeDef",
    "ListClustersV2RequestRequestTypeDef",
    "ListConfigurationRevisionsRequestRequestTypeDef",
    "ListConfigurationsRequestRequestTypeDef",
    "ListKafkaVersionsRequestRequestTypeDef",
    "ListNodesRequestRequestTypeDef",
    "ListScramSecretsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListVpcConnectionsRequestRequestTypeDef",
    "VpcConnectionTypeDef",
    "NodeExporterInfoTypeDef",
    "NodeExporterTypeDef",
    "ZookeeperNodeInfoTypeDef",
    "PutClusterPolicyRequestRequestTypeDef",
    "RebootBrokerRequestRequestTypeDef",
    "RejectClientVpcConnectionRequestRequestTypeDef",
    "ScramTypeDef",
    "VpcConfigPaginatorTypeDef",
    "VpcConfigTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateBrokerCountRequestRequestTypeDef",
    "UpdateBrokerTypeRequestRequestTypeDef",
    "UserIdentityTypeDef",
    "VpcConnectivityTlsTypeDef",
    "VpcConnectivityIamTypeDef",
    "VpcConnectivityScramTypeDef",
    "CreateClusterResponseTypeDef",
    "CreateClusterV2ResponseTypeDef",
    "CreateVpcConnectionResponseTypeDef",
    "DeleteClusterResponseTypeDef",
    "DeleteConfigurationResponseTypeDef",
    "DeleteVpcConnectionResponseTypeDef",
    "DescribeConfigurationRevisionResponseTypeDef",
    "DescribeVpcConnectionResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetBootstrapBrokersResponseTypeDef",
    "GetClusterPolicyResponseTypeDef",
    "ListScramSecretsResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PutClusterPolicyResponseTypeDef",
    "RebootBrokerResponseTypeDef",
    "UpdateBrokerCountResponseTypeDef",
    "UpdateBrokerStorageResponseTypeDef",
    "UpdateBrokerTypeResponseTypeDef",
    "UpdateClusterConfigurationResponseTypeDef",
    "UpdateClusterKafkaVersionResponseTypeDef",
    "UpdateConnectivityResponseTypeDef",
    "UpdateMonitoringResponseTypeDef",
    "UpdateSecurityResponseTypeDef",
    "UpdateStorageResponseTypeDef",
    "BatchAssociateScramSecretResponseTypeDef",
    "BatchDisassociateScramSecretResponseTypeDef",
    "CreateConfigurationRequestRequestTypeDef",
    "UpdateConfigurationRequestRequestTypeDef",
    "BrokerEBSVolumeInfoTypeDef",
    "EBSStorageInfoTypeDef",
    "UpdateStorageRequestRequestTypeDef",
    "BrokerLogsTypeDef",
    "BrokerNodeInfoTypeDef",
    "ListClientVpcConnectionsResponseTypeDef",
    "ClusterOperationStepTypeDef",
    "ListClusterOperationsV2ResponseTypeDef",
    "GetCompatibleKafkaVersionsResponseTypeDef",
    "UpdateClusterConfigurationRequestRequestTypeDef",
    "UpdateClusterKafkaVersionRequestRequestTypeDef",
    "ConfigurationTypeDef",
    "CreateConfigurationResponseTypeDef",
    "DescribeConfigurationResponseTypeDef",
    "ListConfigurationRevisionsResponseTypeDef",
    "UpdateConfigurationResponseTypeDef",
    "EncryptionInfoTypeDef",
    "ServerlessSaslTypeDef",
    "ListKafkaVersionsResponseTypeDef",
    "ListClientVpcConnectionsRequestListClientVpcConnectionsPaginateTypeDef",
    "ListClusterOperationsRequestListClusterOperationsPaginateTypeDef",
    "ListClusterOperationsV2RequestListClusterOperationsV2PaginateTypeDef",
    "ListClustersRequestListClustersPaginateTypeDef",
    "ListClustersV2RequestListClustersV2PaginateTypeDef",
    "ListConfigurationRevisionsRequestListConfigurationRevisionsPaginateTypeDef",
    "ListConfigurationsRequestListConfigurationsPaginateTypeDef",
    "ListKafkaVersionsRequestListKafkaVersionsPaginateTypeDef",
    "ListNodesRequestListNodesPaginateTypeDef",
    "ListScramSecretsRequestListScramSecretsPaginateTypeDef",
    "ListVpcConnectionsRequestListVpcConnectionsPaginateTypeDef",
    "ListVpcConnectionsResponseTypeDef",
    "PrometheusInfoTypeDef",
    "PrometheusTypeDef",
    "SaslTypeDef",
    "VpcConnectionInfoServerlessTypeDef",
    "VpcConnectionInfoTypeDef",
    "VpcConnectivitySaslTypeDef",
    "UpdateBrokerStorageRequestRequestTypeDef",
    "StorageInfoTypeDef",
    "LoggingInfoTypeDef",
    "NodeInfoTypeDef",
    "ListConfigurationsResponseTypeDef",
    "ServerlessClientAuthenticationTypeDef",
    "OpenMonitoringInfoTypeDef",
    "OpenMonitoringTypeDef",
    "ClientAuthenticationPaginatorTypeDef",
    "ClientAuthenticationTypeDef",
    "ClusterOperationV2ServerlessTypeDef",
    "VpcConnectivityClientAuthenticationTypeDef",
    "ListNodesResponseTypeDef",
    "ServerlessPaginatorTypeDef",
    "ServerlessRequestTypeDef",
    "ServerlessTypeDef",
    "UpdateMonitoringRequestRequestTypeDef",
    "UpdateSecurityRequestRequestTypeDef",
    "VpcConnectivityTypeDef",
    "ConnectivityInfoTypeDef",
    "BrokerNodeGroupInfoPaginatorTypeDef",
    "BrokerNodeGroupInfoTypeDef",
    "MutableClusterInfoPaginatorTypeDef",
    "MutableClusterInfoTypeDef",
    "UpdateConnectivityRequestRequestTypeDef",
    "ClusterInfoPaginatorTypeDef",
    "ProvisionedPaginatorTypeDef",
    "ClusterInfoTypeDef",
    "CreateClusterRequestRequestTypeDef",
    "ProvisionedRequestTypeDef",
    "ProvisionedTypeDef",
    "ClusterOperationInfoPaginatorTypeDef",
    "ClusterOperationInfoTypeDef",
    "ClusterOperationV2ProvisionedTypeDef",
    "ListClustersResponsePaginatorTypeDef",
    "ClusterPaginatorTypeDef",
    "DescribeClusterResponseTypeDef",
    "ListClustersResponseTypeDef",
    "CreateClusterV2RequestRequestTypeDef",
    "ClusterTypeDef",
    "ListClusterOperationsResponsePaginatorTypeDef",
    "DescribeClusterOperationResponseTypeDef",
    "ListClusterOperationsResponseTypeDef",
    "ClusterOperationV2TypeDef",
    "ListClustersV2ResponsePaginatorTypeDef",
    "DescribeClusterV2ResponseTypeDef",
    "ListClustersV2ResponseTypeDef",
    "DescribeClusterOperationV2ResponseTypeDef",
)

BatchAssociateScramSecretRequestRequestTypeDef = TypedDict(
    "BatchAssociateScramSecretRequestRequestTypeDef",
    {
        "ClusterArn": str,
        "SecretArnList": Sequence[str],
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

UnprocessedScramSecretTypeDef = TypedDict(
    "UnprocessedScramSecretTypeDef",
    {
        "ErrorCode": NotRequired[str],
        "ErrorMessage": NotRequired[str],
        "SecretArn": NotRequired[str],
    },
)

BatchDisassociateScramSecretRequestRequestTypeDef = TypedDict(
    "BatchDisassociateScramSecretRequestRequestTypeDef",
    {
        "ClusterArn": str,
        "SecretArnList": Sequence[str],
    },
)

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]
ProvisionedThroughputTypeDef = TypedDict(
    "ProvisionedThroughputTypeDef",
    {
        "Enabled": NotRequired[bool],
        "VolumeThroughput": NotRequired[int],
    },
)

CloudWatchLogsTypeDef = TypedDict(
    "CloudWatchLogsTypeDef",
    {
        "Enabled": bool,
        "LogGroup": NotRequired[str],
    },
)

FirehoseTypeDef = TypedDict(
    "FirehoseTypeDef",
    {
        "Enabled": bool,
        "DeliveryStream": NotRequired[str],
    },
)

S3TypeDef = TypedDict(
    "S3TypeDef",
    {
        "Enabled": bool,
        "Bucket": NotRequired[str],
        "Prefix": NotRequired[str],
    },
)

BrokerSoftwareInfoTypeDef = TypedDict(
    "BrokerSoftwareInfoTypeDef",
    {
        "ConfigurationArn": NotRequired[str],
        "ConfigurationRevision": NotRequired[int],
        "KafkaVersion": NotRequired[str],
    },
)

TlsPaginatorTypeDef = TypedDict(
    "TlsPaginatorTypeDef",
    {
        "CertificateAuthorityArnList": NotRequired[List[str]],
        "Enabled": NotRequired[bool],
    },
)

UnauthenticatedTypeDef = TypedDict(
    "UnauthenticatedTypeDef",
    {
        "Enabled": NotRequired[bool],
    },
)

TlsTypeDef = TypedDict(
    "TlsTypeDef",
    {
        "CertificateAuthorityArnList": NotRequired[Sequence[str]],
        "Enabled": NotRequired[bool],
    },
)

ClientVpcConnectionTypeDef = TypedDict(
    "ClientVpcConnectionTypeDef",
    {
        "VpcConnectionArn": str,
        "Authentication": NotRequired[str],
        "CreationTime": NotRequired[datetime],
        "State": NotRequired[VpcConnectionStateType],
        "Owner": NotRequired[str],
    },
)

StateInfoTypeDef = TypedDict(
    "StateInfoTypeDef",
    {
        "Code": NotRequired[str],
        "Message": NotRequired[str],
    },
)

ErrorInfoTypeDef = TypedDict(
    "ErrorInfoTypeDef",
    {
        "ErrorCode": NotRequired[str],
        "ErrorString": NotRequired[str],
    },
)

ClusterOperationStepInfoTypeDef = TypedDict(
    "ClusterOperationStepInfoTypeDef",
    {
        "StepStatus": NotRequired[str],
    },
)

ClusterOperationV2SummaryTypeDef = TypedDict(
    "ClusterOperationV2SummaryTypeDef",
    {
        "ClusterArn": NotRequired[str],
        "ClusterType": NotRequired[ClusterTypeType],
        "StartTime": NotRequired[datetime],
        "EndTime": NotRequired[datetime],
        "OperationArn": NotRequired[str],
        "OperationState": NotRequired[str],
        "OperationType": NotRequired[str],
    },
)

CompatibleKafkaVersionTypeDef = TypedDict(
    "CompatibleKafkaVersionTypeDef",
    {
        "SourceVersion": NotRequired[str],
        "TargetVersions": NotRequired[List[str]],
    },
)

ConfigurationInfoTypeDef = TypedDict(
    "ConfigurationInfoTypeDef",
    {
        "Arn": str,
        "Revision": int,
    },
)

ConfigurationRevisionTypeDef = TypedDict(
    "ConfigurationRevisionTypeDef",
    {
        "CreationTime": datetime,
        "Revision": int,
        "Description": NotRequired[str],
    },
)

PublicAccessTypeDef = TypedDict(
    "PublicAccessTypeDef",
    {
        "Type": NotRequired[str],
    },
)

CreateVpcConnectionRequestRequestTypeDef = TypedDict(
    "CreateVpcConnectionRequestRequestTypeDef",
    {
        "TargetClusterArn": str,
        "Authentication": str,
        "VpcId": str,
        "ClientSubnets": Sequence[str],
        "SecurityGroups": Sequence[str],
        "Tags": NotRequired[Mapping[str, str]],
    },
)

DeleteClusterPolicyRequestRequestTypeDef = TypedDict(
    "DeleteClusterPolicyRequestRequestTypeDef",
    {
        "ClusterArn": str,
    },
)

DeleteClusterRequestRequestTypeDef = TypedDict(
    "DeleteClusterRequestRequestTypeDef",
    {
        "ClusterArn": str,
        "CurrentVersion": NotRequired[str],
    },
)

DeleteConfigurationRequestRequestTypeDef = TypedDict(
    "DeleteConfigurationRequestRequestTypeDef",
    {
        "Arn": str,
    },
)

DeleteVpcConnectionRequestRequestTypeDef = TypedDict(
    "DeleteVpcConnectionRequestRequestTypeDef",
    {
        "Arn": str,
    },
)

DescribeClusterOperationRequestRequestTypeDef = TypedDict(
    "DescribeClusterOperationRequestRequestTypeDef",
    {
        "ClusterOperationArn": str,
    },
)

DescribeClusterOperationV2RequestRequestTypeDef = TypedDict(
    "DescribeClusterOperationV2RequestRequestTypeDef",
    {
        "ClusterOperationArn": str,
    },
)

DescribeClusterRequestRequestTypeDef = TypedDict(
    "DescribeClusterRequestRequestTypeDef",
    {
        "ClusterArn": str,
    },
)

DescribeClusterV2RequestRequestTypeDef = TypedDict(
    "DescribeClusterV2RequestRequestTypeDef",
    {
        "ClusterArn": str,
    },
)

DescribeConfigurationRequestRequestTypeDef = TypedDict(
    "DescribeConfigurationRequestRequestTypeDef",
    {
        "Arn": str,
    },
)

DescribeConfigurationRevisionRequestRequestTypeDef = TypedDict(
    "DescribeConfigurationRevisionRequestRequestTypeDef",
    {
        "Arn": str,
        "Revision": int,
    },
)

DescribeVpcConnectionRequestRequestTypeDef = TypedDict(
    "DescribeVpcConnectionRequestRequestTypeDef",
    {
        "Arn": str,
    },
)

EncryptionAtRestTypeDef = TypedDict(
    "EncryptionAtRestTypeDef",
    {
        "DataVolumeKMSKeyId": str,
    },
)

EncryptionInTransitTypeDef = TypedDict(
    "EncryptionInTransitTypeDef",
    {
        "ClientBroker": NotRequired[ClientBrokerType],
        "InCluster": NotRequired[bool],
    },
)

GetBootstrapBrokersRequestRequestTypeDef = TypedDict(
    "GetBootstrapBrokersRequestRequestTypeDef",
    {
        "ClusterArn": str,
    },
)

GetClusterPolicyRequestRequestTypeDef = TypedDict(
    "GetClusterPolicyRequestRequestTypeDef",
    {
        "ClusterArn": str,
    },
)

GetCompatibleKafkaVersionsRequestRequestTypeDef = TypedDict(
    "GetCompatibleKafkaVersionsRequestRequestTypeDef",
    {
        "ClusterArn": NotRequired[str],
    },
)

IamTypeDef = TypedDict(
    "IamTypeDef",
    {
        "Enabled": NotRequired[bool],
    },
)

JmxExporterInfoTypeDef = TypedDict(
    "JmxExporterInfoTypeDef",
    {
        "EnabledInBroker": bool,
    },
)

JmxExporterTypeDef = TypedDict(
    "JmxExporterTypeDef",
    {
        "EnabledInBroker": bool,
    },
)

KafkaVersionTypeDef = TypedDict(
    "KafkaVersionTypeDef",
    {
        "Version": NotRequired[str],
        "Status": NotRequired[KafkaVersionStatusType],
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

ListClientVpcConnectionsRequestRequestTypeDef = TypedDict(
    "ListClientVpcConnectionsRequestRequestTypeDef",
    {
        "ClusterArn": str,
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

ListClusterOperationsRequestRequestTypeDef = TypedDict(
    "ListClusterOperationsRequestRequestTypeDef",
    {
        "ClusterArn": str,
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

ListClusterOperationsV2RequestRequestTypeDef = TypedDict(
    "ListClusterOperationsV2RequestRequestTypeDef",
    {
        "ClusterArn": str,
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

ListClustersRequestRequestTypeDef = TypedDict(
    "ListClustersRequestRequestTypeDef",
    {
        "ClusterNameFilter": NotRequired[str],
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

ListClustersV2RequestRequestTypeDef = TypedDict(
    "ListClustersV2RequestRequestTypeDef",
    {
        "ClusterNameFilter": NotRequired[str],
        "ClusterTypeFilter": NotRequired[str],
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

ListConfigurationRevisionsRequestRequestTypeDef = TypedDict(
    "ListConfigurationRevisionsRequestRequestTypeDef",
    {
        "Arn": str,
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

ListConfigurationsRequestRequestTypeDef = TypedDict(
    "ListConfigurationsRequestRequestTypeDef",
    {
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

ListKafkaVersionsRequestRequestTypeDef = TypedDict(
    "ListKafkaVersionsRequestRequestTypeDef",
    {
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

ListNodesRequestRequestTypeDef = TypedDict(
    "ListNodesRequestRequestTypeDef",
    {
        "ClusterArn": str,
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

ListScramSecretsRequestRequestTypeDef = TypedDict(
    "ListScramSecretsRequestRequestTypeDef",
    {
        "ClusterArn": str,
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

ListVpcConnectionsRequestRequestTypeDef = TypedDict(
    "ListVpcConnectionsRequestRequestTypeDef",
    {
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

VpcConnectionTypeDef = TypedDict(
    "VpcConnectionTypeDef",
    {
        "VpcConnectionArn": str,
        "TargetClusterArn": str,
        "CreationTime": NotRequired[datetime],
        "Authentication": NotRequired[str],
        "VpcId": NotRequired[str],
        "State": NotRequired[VpcConnectionStateType],
    },
)

NodeExporterInfoTypeDef = TypedDict(
    "NodeExporterInfoTypeDef",
    {
        "EnabledInBroker": bool,
    },
)

NodeExporterTypeDef = TypedDict(
    "NodeExporterTypeDef",
    {
        "EnabledInBroker": bool,
    },
)

ZookeeperNodeInfoTypeDef = TypedDict(
    "ZookeeperNodeInfoTypeDef",
    {
        "AttachedENIId": NotRequired[str],
        "ClientVpcIpAddress": NotRequired[str],
        "Endpoints": NotRequired[List[str]],
        "ZookeeperId": NotRequired[float],
        "ZookeeperVersion": NotRequired[str],
    },
)

PutClusterPolicyRequestRequestTypeDef = TypedDict(
    "PutClusterPolicyRequestRequestTypeDef",
    {
        "ClusterArn": str,
        "Policy": str,
        "CurrentVersion": NotRequired[str],
    },
)

RebootBrokerRequestRequestTypeDef = TypedDict(
    "RebootBrokerRequestRequestTypeDef",
    {
        "BrokerIds": Sequence[str],
        "ClusterArn": str,
    },
)

RejectClientVpcConnectionRequestRequestTypeDef = TypedDict(
    "RejectClientVpcConnectionRequestRequestTypeDef",
    {
        "ClusterArn": str,
        "VpcConnectionArn": str,
    },
)

ScramTypeDef = TypedDict(
    "ScramTypeDef",
    {
        "Enabled": NotRequired[bool],
    },
)

VpcConfigPaginatorTypeDef = TypedDict(
    "VpcConfigPaginatorTypeDef",
    {
        "SubnetIds": List[str],
        "SecurityGroupIds": NotRequired[List[str]],
    },
)

VpcConfigTypeDef = TypedDict(
    "VpcConfigTypeDef",
    {
        "SubnetIds": Sequence[str],
        "SecurityGroupIds": NotRequired[Sequence[str]],
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

UpdateBrokerCountRequestRequestTypeDef = TypedDict(
    "UpdateBrokerCountRequestRequestTypeDef",
    {
        "ClusterArn": str,
        "CurrentVersion": str,
        "TargetNumberOfBrokerNodes": int,
    },
)

UpdateBrokerTypeRequestRequestTypeDef = TypedDict(
    "UpdateBrokerTypeRequestRequestTypeDef",
    {
        "ClusterArn": str,
        "CurrentVersion": str,
        "TargetInstanceType": str,
    },
)

UserIdentityTypeDef = TypedDict(
    "UserIdentityTypeDef",
    {
        "Type": NotRequired[UserIdentityTypeType],
        "PrincipalId": NotRequired[str],
    },
)

VpcConnectivityTlsTypeDef = TypedDict(
    "VpcConnectivityTlsTypeDef",
    {
        "Enabled": NotRequired[bool],
    },
)

VpcConnectivityIamTypeDef = TypedDict(
    "VpcConnectivityIamTypeDef",
    {
        "Enabled": NotRequired[bool],
    },
)

VpcConnectivityScramTypeDef = TypedDict(
    "VpcConnectivityScramTypeDef",
    {
        "Enabled": NotRequired[bool],
    },
)

CreateClusterResponseTypeDef = TypedDict(
    "CreateClusterResponseTypeDef",
    {
        "ClusterArn": str,
        "ClusterName": str,
        "State": ClusterStateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateClusterV2ResponseTypeDef = TypedDict(
    "CreateClusterV2ResponseTypeDef",
    {
        "ClusterArn": str,
        "ClusterName": str,
        "State": ClusterStateType,
        "ClusterType": ClusterTypeType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateVpcConnectionResponseTypeDef = TypedDict(
    "CreateVpcConnectionResponseTypeDef",
    {
        "VpcConnectionArn": str,
        "State": VpcConnectionStateType,
        "Authentication": str,
        "VpcId": str,
        "ClientSubnets": List[str],
        "SecurityGroups": List[str],
        "CreationTime": datetime,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteClusterResponseTypeDef = TypedDict(
    "DeleteClusterResponseTypeDef",
    {
        "ClusterArn": str,
        "State": ClusterStateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteConfigurationResponseTypeDef = TypedDict(
    "DeleteConfigurationResponseTypeDef",
    {
        "Arn": str,
        "State": ConfigurationStateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteVpcConnectionResponseTypeDef = TypedDict(
    "DeleteVpcConnectionResponseTypeDef",
    {
        "VpcConnectionArn": str,
        "State": VpcConnectionStateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeConfigurationRevisionResponseTypeDef = TypedDict(
    "DescribeConfigurationRevisionResponseTypeDef",
    {
        "Arn": str,
        "CreationTime": datetime,
        "Description": str,
        "Revision": int,
        "ServerProperties": bytes,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeVpcConnectionResponseTypeDef = TypedDict(
    "DescribeVpcConnectionResponseTypeDef",
    {
        "VpcConnectionArn": str,
        "TargetClusterArn": str,
        "State": VpcConnectionStateType,
        "Authentication": str,
        "VpcId": str,
        "Subnets": List[str],
        "SecurityGroups": List[str],
        "CreationTime": datetime,
        "Tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetBootstrapBrokersResponseTypeDef = TypedDict(
    "GetBootstrapBrokersResponseTypeDef",
    {
        "BootstrapBrokerString": str,
        "BootstrapBrokerStringTls": str,
        "BootstrapBrokerStringSaslScram": str,
        "BootstrapBrokerStringSaslIam": str,
        "BootstrapBrokerStringPublicTls": str,
        "BootstrapBrokerStringPublicSaslScram": str,
        "BootstrapBrokerStringPublicSaslIam": str,
        "BootstrapBrokerStringVpcConnectivityTls": str,
        "BootstrapBrokerStringVpcConnectivitySaslScram": str,
        "BootstrapBrokerStringVpcConnectivitySaslIam": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetClusterPolicyResponseTypeDef = TypedDict(
    "GetClusterPolicyResponseTypeDef",
    {
        "CurrentVersion": str,
        "Policy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListScramSecretsResponseTypeDef = TypedDict(
    "ListScramSecretsResponseTypeDef",
    {
        "NextToken": str,
        "SecretArnList": List[str],
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

PutClusterPolicyResponseTypeDef = TypedDict(
    "PutClusterPolicyResponseTypeDef",
    {
        "CurrentVersion": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RebootBrokerResponseTypeDef = TypedDict(
    "RebootBrokerResponseTypeDef",
    {
        "ClusterArn": str,
        "ClusterOperationArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateBrokerCountResponseTypeDef = TypedDict(
    "UpdateBrokerCountResponseTypeDef",
    {
        "ClusterArn": str,
        "ClusterOperationArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateBrokerStorageResponseTypeDef = TypedDict(
    "UpdateBrokerStorageResponseTypeDef",
    {
        "ClusterArn": str,
        "ClusterOperationArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateBrokerTypeResponseTypeDef = TypedDict(
    "UpdateBrokerTypeResponseTypeDef",
    {
        "ClusterArn": str,
        "ClusterOperationArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateClusterConfigurationResponseTypeDef = TypedDict(
    "UpdateClusterConfigurationResponseTypeDef",
    {
        "ClusterArn": str,
        "ClusterOperationArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateClusterKafkaVersionResponseTypeDef = TypedDict(
    "UpdateClusterKafkaVersionResponseTypeDef",
    {
        "ClusterArn": str,
        "ClusterOperationArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateConnectivityResponseTypeDef = TypedDict(
    "UpdateConnectivityResponseTypeDef",
    {
        "ClusterArn": str,
        "ClusterOperationArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateMonitoringResponseTypeDef = TypedDict(
    "UpdateMonitoringResponseTypeDef",
    {
        "ClusterArn": str,
        "ClusterOperationArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateSecurityResponseTypeDef = TypedDict(
    "UpdateSecurityResponseTypeDef",
    {
        "ClusterArn": str,
        "ClusterOperationArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateStorageResponseTypeDef = TypedDict(
    "UpdateStorageResponseTypeDef",
    {
        "ClusterArn": str,
        "ClusterOperationArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchAssociateScramSecretResponseTypeDef = TypedDict(
    "BatchAssociateScramSecretResponseTypeDef",
    {
        "ClusterArn": str,
        "UnprocessedScramSecrets": List[UnprocessedScramSecretTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchDisassociateScramSecretResponseTypeDef = TypedDict(
    "BatchDisassociateScramSecretResponseTypeDef",
    {
        "ClusterArn": str,
        "UnprocessedScramSecrets": List[UnprocessedScramSecretTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateConfigurationRequestRequestTypeDef = TypedDict(
    "CreateConfigurationRequestRequestTypeDef",
    {
        "Name": str,
        "ServerProperties": BlobTypeDef,
        "Description": NotRequired[str],
        "KafkaVersions": NotRequired[Sequence[str]],
    },
)

UpdateConfigurationRequestRequestTypeDef = TypedDict(
    "UpdateConfigurationRequestRequestTypeDef",
    {
        "Arn": str,
        "ServerProperties": BlobTypeDef,
        "Description": NotRequired[str],
    },
)

BrokerEBSVolumeInfoTypeDef = TypedDict(
    "BrokerEBSVolumeInfoTypeDef",
    {
        "KafkaBrokerNodeId": str,
        "ProvisionedThroughput": NotRequired[ProvisionedThroughputTypeDef],
        "VolumeSizeGB": NotRequired[int],
    },
)

EBSStorageInfoTypeDef = TypedDict(
    "EBSStorageInfoTypeDef",
    {
        "ProvisionedThroughput": NotRequired[ProvisionedThroughputTypeDef],
        "VolumeSize": NotRequired[int],
    },
)

UpdateStorageRequestRequestTypeDef = TypedDict(
    "UpdateStorageRequestRequestTypeDef",
    {
        "ClusterArn": str,
        "CurrentVersion": str,
        "ProvisionedThroughput": NotRequired[ProvisionedThroughputTypeDef],
        "StorageMode": NotRequired[StorageModeType],
        "VolumeSizeGB": NotRequired[int],
    },
)

BrokerLogsTypeDef = TypedDict(
    "BrokerLogsTypeDef",
    {
        "CloudWatchLogs": NotRequired[CloudWatchLogsTypeDef],
        "Firehose": NotRequired[FirehoseTypeDef],
        "S3": NotRequired[S3TypeDef],
    },
)

BrokerNodeInfoTypeDef = TypedDict(
    "BrokerNodeInfoTypeDef",
    {
        "AttachedENIId": NotRequired[str],
        "BrokerId": NotRequired[float],
        "ClientSubnet": NotRequired[str],
        "ClientVpcIpAddress": NotRequired[str],
        "CurrentBrokerSoftwareInfo": NotRequired[BrokerSoftwareInfoTypeDef],
        "Endpoints": NotRequired[List[str]],
    },
)

ListClientVpcConnectionsResponseTypeDef = TypedDict(
    "ListClientVpcConnectionsResponseTypeDef",
    {
        "ClientVpcConnections": List[ClientVpcConnectionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ClusterOperationStepTypeDef = TypedDict(
    "ClusterOperationStepTypeDef",
    {
        "StepInfo": NotRequired[ClusterOperationStepInfoTypeDef],
        "StepName": NotRequired[str],
    },
)

ListClusterOperationsV2ResponseTypeDef = TypedDict(
    "ListClusterOperationsV2ResponseTypeDef",
    {
        "ClusterOperationInfoList": List[ClusterOperationV2SummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetCompatibleKafkaVersionsResponseTypeDef = TypedDict(
    "GetCompatibleKafkaVersionsResponseTypeDef",
    {
        "CompatibleKafkaVersions": List[CompatibleKafkaVersionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateClusterConfigurationRequestRequestTypeDef = TypedDict(
    "UpdateClusterConfigurationRequestRequestTypeDef",
    {
        "ClusterArn": str,
        "ConfigurationInfo": ConfigurationInfoTypeDef,
        "CurrentVersion": str,
    },
)

UpdateClusterKafkaVersionRequestRequestTypeDef = TypedDict(
    "UpdateClusterKafkaVersionRequestRequestTypeDef",
    {
        "ClusterArn": str,
        "CurrentVersion": str,
        "TargetKafkaVersion": str,
        "ConfigurationInfo": NotRequired[ConfigurationInfoTypeDef],
    },
)

ConfigurationTypeDef = TypedDict(
    "ConfigurationTypeDef",
    {
        "Arn": str,
        "CreationTime": datetime,
        "Description": str,
        "KafkaVersions": List[str],
        "LatestRevision": ConfigurationRevisionTypeDef,
        "Name": str,
        "State": ConfigurationStateType,
    },
)

CreateConfigurationResponseTypeDef = TypedDict(
    "CreateConfigurationResponseTypeDef",
    {
        "Arn": str,
        "CreationTime": datetime,
        "LatestRevision": ConfigurationRevisionTypeDef,
        "Name": str,
        "State": ConfigurationStateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeConfigurationResponseTypeDef = TypedDict(
    "DescribeConfigurationResponseTypeDef",
    {
        "Arn": str,
        "CreationTime": datetime,
        "Description": str,
        "KafkaVersions": List[str],
        "LatestRevision": ConfigurationRevisionTypeDef,
        "Name": str,
        "State": ConfigurationStateType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListConfigurationRevisionsResponseTypeDef = TypedDict(
    "ListConfigurationRevisionsResponseTypeDef",
    {
        "NextToken": str,
        "Revisions": List[ConfigurationRevisionTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateConfigurationResponseTypeDef = TypedDict(
    "UpdateConfigurationResponseTypeDef",
    {
        "Arn": str,
        "LatestRevision": ConfigurationRevisionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EncryptionInfoTypeDef = TypedDict(
    "EncryptionInfoTypeDef",
    {
        "EncryptionAtRest": NotRequired[EncryptionAtRestTypeDef],
        "EncryptionInTransit": NotRequired[EncryptionInTransitTypeDef],
    },
)

ServerlessSaslTypeDef = TypedDict(
    "ServerlessSaslTypeDef",
    {
        "Iam": NotRequired[IamTypeDef],
    },
)

ListKafkaVersionsResponseTypeDef = TypedDict(
    "ListKafkaVersionsResponseTypeDef",
    {
        "KafkaVersions": List[KafkaVersionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListClientVpcConnectionsRequestListClientVpcConnectionsPaginateTypeDef = TypedDict(
    "ListClientVpcConnectionsRequestListClientVpcConnectionsPaginateTypeDef",
    {
        "ClusterArn": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListClusterOperationsRequestListClusterOperationsPaginateTypeDef = TypedDict(
    "ListClusterOperationsRequestListClusterOperationsPaginateTypeDef",
    {
        "ClusterArn": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListClusterOperationsV2RequestListClusterOperationsV2PaginateTypeDef = TypedDict(
    "ListClusterOperationsV2RequestListClusterOperationsV2PaginateTypeDef",
    {
        "ClusterArn": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListClustersRequestListClustersPaginateTypeDef = TypedDict(
    "ListClustersRequestListClustersPaginateTypeDef",
    {
        "ClusterNameFilter": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListClustersV2RequestListClustersV2PaginateTypeDef = TypedDict(
    "ListClustersV2RequestListClustersV2PaginateTypeDef",
    {
        "ClusterNameFilter": NotRequired[str],
        "ClusterTypeFilter": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListConfigurationRevisionsRequestListConfigurationRevisionsPaginateTypeDef = TypedDict(
    "ListConfigurationRevisionsRequestListConfigurationRevisionsPaginateTypeDef",
    {
        "Arn": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListConfigurationsRequestListConfigurationsPaginateTypeDef = TypedDict(
    "ListConfigurationsRequestListConfigurationsPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListKafkaVersionsRequestListKafkaVersionsPaginateTypeDef = TypedDict(
    "ListKafkaVersionsRequestListKafkaVersionsPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListNodesRequestListNodesPaginateTypeDef = TypedDict(
    "ListNodesRequestListNodesPaginateTypeDef",
    {
        "ClusterArn": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListScramSecretsRequestListScramSecretsPaginateTypeDef = TypedDict(
    "ListScramSecretsRequestListScramSecretsPaginateTypeDef",
    {
        "ClusterArn": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListVpcConnectionsRequestListVpcConnectionsPaginateTypeDef = TypedDict(
    "ListVpcConnectionsRequestListVpcConnectionsPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListVpcConnectionsResponseTypeDef = TypedDict(
    "ListVpcConnectionsResponseTypeDef",
    {
        "VpcConnections": List[VpcConnectionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PrometheusInfoTypeDef = TypedDict(
    "PrometheusInfoTypeDef",
    {
        "JmxExporter": NotRequired[JmxExporterInfoTypeDef],
        "NodeExporter": NotRequired[NodeExporterInfoTypeDef],
    },
)

PrometheusTypeDef = TypedDict(
    "PrometheusTypeDef",
    {
        "JmxExporter": NotRequired[JmxExporterTypeDef],
        "NodeExporter": NotRequired[NodeExporterTypeDef],
    },
)

SaslTypeDef = TypedDict(
    "SaslTypeDef",
    {
        "Scram": NotRequired[ScramTypeDef],
        "Iam": NotRequired[IamTypeDef],
    },
)

VpcConnectionInfoServerlessTypeDef = TypedDict(
    "VpcConnectionInfoServerlessTypeDef",
    {
        "CreationTime": NotRequired[datetime],
        "Owner": NotRequired[str],
        "UserIdentity": NotRequired[UserIdentityTypeDef],
        "VpcConnectionArn": NotRequired[str],
    },
)

VpcConnectionInfoTypeDef = TypedDict(
    "VpcConnectionInfoTypeDef",
    {
        "VpcConnectionArn": NotRequired[str],
        "Owner": NotRequired[str],
        "UserIdentity": NotRequired[UserIdentityTypeDef],
        "CreationTime": NotRequired[datetime],
    },
)

VpcConnectivitySaslTypeDef = TypedDict(
    "VpcConnectivitySaslTypeDef",
    {
        "Scram": NotRequired[VpcConnectivityScramTypeDef],
        "Iam": NotRequired[VpcConnectivityIamTypeDef],
    },
)

UpdateBrokerStorageRequestRequestTypeDef = TypedDict(
    "UpdateBrokerStorageRequestRequestTypeDef",
    {
        "ClusterArn": str,
        "CurrentVersion": str,
        "TargetBrokerEBSVolumeInfo": Sequence[BrokerEBSVolumeInfoTypeDef],
    },
)

StorageInfoTypeDef = TypedDict(
    "StorageInfoTypeDef",
    {
        "EbsStorageInfo": NotRequired[EBSStorageInfoTypeDef],
    },
)

LoggingInfoTypeDef = TypedDict(
    "LoggingInfoTypeDef",
    {
        "BrokerLogs": BrokerLogsTypeDef,
    },
)

NodeInfoTypeDef = TypedDict(
    "NodeInfoTypeDef",
    {
        "AddedToClusterTime": NotRequired[str],
        "BrokerNodeInfo": NotRequired[BrokerNodeInfoTypeDef],
        "InstanceType": NotRequired[str],
        "NodeARN": NotRequired[str],
        "NodeType": NotRequired[Literal["BROKER"]],
        "ZookeeperNodeInfo": NotRequired[ZookeeperNodeInfoTypeDef],
    },
)

ListConfigurationsResponseTypeDef = TypedDict(
    "ListConfigurationsResponseTypeDef",
    {
        "Configurations": List[ConfigurationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ServerlessClientAuthenticationTypeDef = TypedDict(
    "ServerlessClientAuthenticationTypeDef",
    {
        "Sasl": NotRequired[ServerlessSaslTypeDef],
    },
)

OpenMonitoringInfoTypeDef = TypedDict(
    "OpenMonitoringInfoTypeDef",
    {
        "Prometheus": PrometheusInfoTypeDef,
    },
)

OpenMonitoringTypeDef = TypedDict(
    "OpenMonitoringTypeDef",
    {
        "Prometheus": PrometheusTypeDef,
    },
)

ClientAuthenticationPaginatorTypeDef = TypedDict(
    "ClientAuthenticationPaginatorTypeDef",
    {
        "Sasl": NotRequired[SaslTypeDef],
        "Tls": NotRequired[TlsPaginatorTypeDef],
        "Unauthenticated": NotRequired[UnauthenticatedTypeDef],
    },
)

ClientAuthenticationTypeDef = TypedDict(
    "ClientAuthenticationTypeDef",
    {
        "Sasl": NotRequired[SaslTypeDef],
        "Tls": NotRequired[TlsTypeDef],
        "Unauthenticated": NotRequired[UnauthenticatedTypeDef],
    },
)

ClusterOperationV2ServerlessTypeDef = TypedDict(
    "ClusterOperationV2ServerlessTypeDef",
    {
        "VpcConnectionInfo": NotRequired[VpcConnectionInfoServerlessTypeDef],
    },
)

VpcConnectivityClientAuthenticationTypeDef = TypedDict(
    "VpcConnectivityClientAuthenticationTypeDef",
    {
        "Sasl": NotRequired[VpcConnectivitySaslTypeDef],
        "Tls": NotRequired[VpcConnectivityTlsTypeDef],
    },
)

ListNodesResponseTypeDef = TypedDict(
    "ListNodesResponseTypeDef",
    {
        "NextToken": str,
        "NodeInfoList": List[NodeInfoTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ServerlessPaginatorTypeDef = TypedDict(
    "ServerlessPaginatorTypeDef",
    {
        "VpcConfigs": List[VpcConfigPaginatorTypeDef],
        "ClientAuthentication": NotRequired[ServerlessClientAuthenticationTypeDef],
    },
)

ServerlessRequestTypeDef = TypedDict(
    "ServerlessRequestTypeDef",
    {
        "VpcConfigs": Sequence[VpcConfigTypeDef],
        "ClientAuthentication": NotRequired[ServerlessClientAuthenticationTypeDef],
    },
)

ServerlessTypeDef = TypedDict(
    "ServerlessTypeDef",
    {
        "VpcConfigs": List[VpcConfigTypeDef],
        "ClientAuthentication": NotRequired[ServerlessClientAuthenticationTypeDef],
    },
)

UpdateMonitoringRequestRequestTypeDef = TypedDict(
    "UpdateMonitoringRequestRequestTypeDef",
    {
        "ClusterArn": str,
        "CurrentVersion": str,
        "EnhancedMonitoring": NotRequired[EnhancedMonitoringType],
        "OpenMonitoring": NotRequired[OpenMonitoringInfoTypeDef],
        "LoggingInfo": NotRequired[LoggingInfoTypeDef],
    },
)

UpdateSecurityRequestRequestTypeDef = TypedDict(
    "UpdateSecurityRequestRequestTypeDef",
    {
        "ClusterArn": str,
        "CurrentVersion": str,
        "ClientAuthentication": NotRequired[ClientAuthenticationTypeDef],
        "EncryptionInfo": NotRequired[EncryptionInfoTypeDef],
    },
)

VpcConnectivityTypeDef = TypedDict(
    "VpcConnectivityTypeDef",
    {
        "ClientAuthentication": NotRequired[VpcConnectivityClientAuthenticationTypeDef],
    },
)

ConnectivityInfoTypeDef = TypedDict(
    "ConnectivityInfoTypeDef",
    {
        "PublicAccess": NotRequired[PublicAccessTypeDef],
        "VpcConnectivity": NotRequired[VpcConnectivityTypeDef],
    },
)

BrokerNodeGroupInfoPaginatorTypeDef = TypedDict(
    "BrokerNodeGroupInfoPaginatorTypeDef",
    {
        "ClientSubnets": List[str],
        "InstanceType": str,
        "BrokerAZDistribution": NotRequired[Literal["DEFAULT"]],
        "SecurityGroups": NotRequired[List[str]],
        "StorageInfo": NotRequired[StorageInfoTypeDef],
        "ConnectivityInfo": NotRequired[ConnectivityInfoTypeDef],
        "ZoneIds": NotRequired[List[str]],
    },
)

BrokerNodeGroupInfoTypeDef = TypedDict(
    "BrokerNodeGroupInfoTypeDef",
    {
        "ClientSubnets": Sequence[str],
        "InstanceType": str,
        "BrokerAZDistribution": NotRequired[Literal["DEFAULT"]],
        "SecurityGroups": NotRequired[Sequence[str]],
        "StorageInfo": NotRequired[StorageInfoTypeDef],
        "ConnectivityInfo": NotRequired[ConnectivityInfoTypeDef],
        "ZoneIds": NotRequired[Sequence[str]],
    },
)

MutableClusterInfoPaginatorTypeDef = TypedDict(
    "MutableClusterInfoPaginatorTypeDef",
    {
        "BrokerEBSVolumeInfo": NotRequired[List[BrokerEBSVolumeInfoTypeDef]],
        "ConfigurationInfo": NotRequired[ConfigurationInfoTypeDef],
        "NumberOfBrokerNodes": NotRequired[int],
        "EnhancedMonitoring": NotRequired[EnhancedMonitoringType],
        "OpenMonitoring": NotRequired[OpenMonitoringTypeDef],
        "KafkaVersion": NotRequired[str],
        "LoggingInfo": NotRequired[LoggingInfoTypeDef],
        "InstanceType": NotRequired[str],
        "ClientAuthentication": NotRequired[ClientAuthenticationPaginatorTypeDef],
        "EncryptionInfo": NotRequired[EncryptionInfoTypeDef],
        "ConnectivityInfo": NotRequired[ConnectivityInfoTypeDef],
        "StorageMode": NotRequired[StorageModeType],
    },
)

MutableClusterInfoTypeDef = TypedDict(
    "MutableClusterInfoTypeDef",
    {
        "BrokerEBSVolumeInfo": NotRequired[List[BrokerEBSVolumeInfoTypeDef]],
        "ConfigurationInfo": NotRequired[ConfigurationInfoTypeDef],
        "NumberOfBrokerNodes": NotRequired[int],
        "EnhancedMonitoring": NotRequired[EnhancedMonitoringType],
        "OpenMonitoring": NotRequired[OpenMonitoringTypeDef],
        "KafkaVersion": NotRequired[str],
        "LoggingInfo": NotRequired[LoggingInfoTypeDef],
        "InstanceType": NotRequired[str],
        "ClientAuthentication": NotRequired[ClientAuthenticationTypeDef],
        "EncryptionInfo": NotRequired[EncryptionInfoTypeDef],
        "ConnectivityInfo": NotRequired[ConnectivityInfoTypeDef],
        "StorageMode": NotRequired[StorageModeType],
    },
)

UpdateConnectivityRequestRequestTypeDef = TypedDict(
    "UpdateConnectivityRequestRequestTypeDef",
    {
        "ClusterArn": str,
        "ConnectivityInfo": ConnectivityInfoTypeDef,
        "CurrentVersion": str,
    },
)

ClusterInfoPaginatorTypeDef = TypedDict(
    "ClusterInfoPaginatorTypeDef",
    {
        "ActiveOperationArn": NotRequired[str],
        "BrokerNodeGroupInfo": NotRequired[BrokerNodeGroupInfoPaginatorTypeDef],
        "ClientAuthentication": NotRequired[ClientAuthenticationPaginatorTypeDef],
        "ClusterArn": NotRequired[str],
        "ClusterName": NotRequired[str],
        "CreationTime": NotRequired[datetime],
        "CurrentBrokerSoftwareInfo": NotRequired[BrokerSoftwareInfoTypeDef],
        "CurrentVersion": NotRequired[str],
        "EncryptionInfo": NotRequired[EncryptionInfoTypeDef],
        "EnhancedMonitoring": NotRequired[EnhancedMonitoringType],
        "OpenMonitoring": NotRequired[OpenMonitoringTypeDef],
        "LoggingInfo": NotRequired[LoggingInfoTypeDef],
        "NumberOfBrokerNodes": NotRequired[int],
        "State": NotRequired[ClusterStateType],
        "StateInfo": NotRequired[StateInfoTypeDef],
        "Tags": NotRequired[Dict[str, str]],
        "ZookeeperConnectString": NotRequired[str],
        "ZookeeperConnectStringTls": NotRequired[str],
        "StorageMode": NotRequired[StorageModeType],
    },
)

ProvisionedPaginatorTypeDef = TypedDict(
    "ProvisionedPaginatorTypeDef",
    {
        "BrokerNodeGroupInfo": BrokerNodeGroupInfoPaginatorTypeDef,
        "NumberOfBrokerNodes": int,
        "CurrentBrokerSoftwareInfo": NotRequired[BrokerSoftwareInfoTypeDef],
        "ClientAuthentication": NotRequired[ClientAuthenticationPaginatorTypeDef],
        "EncryptionInfo": NotRequired[EncryptionInfoTypeDef],
        "EnhancedMonitoring": NotRequired[EnhancedMonitoringType],
        "OpenMonitoring": NotRequired[OpenMonitoringInfoTypeDef],
        "LoggingInfo": NotRequired[LoggingInfoTypeDef],
        "ZookeeperConnectString": NotRequired[str],
        "ZookeeperConnectStringTls": NotRequired[str],
        "StorageMode": NotRequired[StorageModeType],
    },
)

ClusterInfoTypeDef = TypedDict(
    "ClusterInfoTypeDef",
    {
        "ActiveOperationArn": NotRequired[str],
        "BrokerNodeGroupInfo": NotRequired[BrokerNodeGroupInfoTypeDef],
        "ClientAuthentication": NotRequired[ClientAuthenticationTypeDef],
        "ClusterArn": NotRequired[str],
        "ClusterName": NotRequired[str],
        "CreationTime": NotRequired[datetime],
        "CurrentBrokerSoftwareInfo": NotRequired[BrokerSoftwareInfoTypeDef],
        "CurrentVersion": NotRequired[str],
        "EncryptionInfo": NotRequired[EncryptionInfoTypeDef],
        "EnhancedMonitoring": NotRequired[EnhancedMonitoringType],
        "OpenMonitoring": NotRequired[OpenMonitoringTypeDef],
        "LoggingInfo": NotRequired[LoggingInfoTypeDef],
        "NumberOfBrokerNodes": NotRequired[int],
        "State": NotRequired[ClusterStateType],
        "StateInfo": NotRequired[StateInfoTypeDef],
        "Tags": NotRequired[Dict[str, str]],
        "ZookeeperConnectString": NotRequired[str],
        "ZookeeperConnectStringTls": NotRequired[str],
        "StorageMode": NotRequired[StorageModeType],
    },
)

CreateClusterRequestRequestTypeDef = TypedDict(
    "CreateClusterRequestRequestTypeDef",
    {
        "BrokerNodeGroupInfo": BrokerNodeGroupInfoTypeDef,
        "ClusterName": str,
        "KafkaVersion": str,
        "NumberOfBrokerNodes": int,
        "ClientAuthentication": NotRequired[ClientAuthenticationTypeDef],
        "ConfigurationInfo": NotRequired[ConfigurationInfoTypeDef],
        "EncryptionInfo": NotRequired[EncryptionInfoTypeDef],
        "EnhancedMonitoring": NotRequired[EnhancedMonitoringType],
        "OpenMonitoring": NotRequired[OpenMonitoringInfoTypeDef],
        "LoggingInfo": NotRequired[LoggingInfoTypeDef],
        "Tags": NotRequired[Mapping[str, str]],
        "StorageMode": NotRequired[StorageModeType],
    },
)

ProvisionedRequestTypeDef = TypedDict(
    "ProvisionedRequestTypeDef",
    {
        "BrokerNodeGroupInfo": BrokerNodeGroupInfoTypeDef,
        "KafkaVersion": str,
        "NumberOfBrokerNodes": int,
        "ClientAuthentication": NotRequired[ClientAuthenticationTypeDef],
        "ConfigurationInfo": NotRequired[ConfigurationInfoTypeDef],
        "EncryptionInfo": NotRequired[EncryptionInfoTypeDef],
        "EnhancedMonitoring": NotRequired[EnhancedMonitoringType],
        "OpenMonitoring": NotRequired[OpenMonitoringInfoTypeDef],
        "LoggingInfo": NotRequired[LoggingInfoTypeDef],
        "StorageMode": NotRequired[StorageModeType],
    },
)

ProvisionedTypeDef = TypedDict(
    "ProvisionedTypeDef",
    {
        "BrokerNodeGroupInfo": BrokerNodeGroupInfoTypeDef,
        "NumberOfBrokerNodes": int,
        "CurrentBrokerSoftwareInfo": NotRequired[BrokerSoftwareInfoTypeDef],
        "ClientAuthentication": NotRequired[ClientAuthenticationTypeDef],
        "EncryptionInfo": NotRequired[EncryptionInfoTypeDef],
        "EnhancedMonitoring": NotRequired[EnhancedMonitoringType],
        "OpenMonitoring": NotRequired[OpenMonitoringInfoTypeDef],
        "LoggingInfo": NotRequired[LoggingInfoTypeDef],
        "ZookeeperConnectString": NotRequired[str],
        "ZookeeperConnectStringTls": NotRequired[str],
        "StorageMode": NotRequired[StorageModeType],
    },
)

ClusterOperationInfoPaginatorTypeDef = TypedDict(
    "ClusterOperationInfoPaginatorTypeDef",
    {
        "ClientRequestId": NotRequired[str],
        "ClusterArn": NotRequired[str],
        "CreationTime": NotRequired[datetime],
        "EndTime": NotRequired[datetime],
        "ErrorInfo": NotRequired[ErrorInfoTypeDef],
        "OperationArn": NotRequired[str],
        "OperationState": NotRequired[str],
        "OperationSteps": NotRequired[List[ClusterOperationStepTypeDef]],
        "OperationType": NotRequired[str],
        "SourceClusterInfo": NotRequired[MutableClusterInfoPaginatorTypeDef],
        "TargetClusterInfo": NotRequired[MutableClusterInfoPaginatorTypeDef],
        "VpcConnectionInfo": NotRequired[VpcConnectionInfoTypeDef],
    },
)

ClusterOperationInfoTypeDef = TypedDict(
    "ClusterOperationInfoTypeDef",
    {
        "ClientRequestId": NotRequired[str],
        "ClusterArn": NotRequired[str],
        "CreationTime": NotRequired[datetime],
        "EndTime": NotRequired[datetime],
        "ErrorInfo": NotRequired[ErrorInfoTypeDef],
        "OperationArn": NotRequired[str],
        "OperationState": NotRequired[str],
        "OperationSteps": NotRequired[List[ClusterOperationStepTypeDef]],
        "OperationType": NotRequired[str],
        "SourceClusterInfo": NotRequired[MutableClusterInfoTypeDef],
        "TargetClusterInfo": NotRequired[MutableClusterInfoTypeDef],
        "VpcConnectionInfo": NotRequired[VpcConnectionInfoTypeDef],
    },
)

ClusterOperationV2ProvisionedTypeDef = TypedDict(
    "ClusterOperationV2ProvisionedTypeDef",
    {
        "OperationSteps": NotRequired[List[ClusterOperationStepTypeDef]],
        "SourceClusterInfo": NotRequired[MutableClusterInfoTypeDef],
        "TargetClusterInfo": NotRequired[MutableClusterInfoTypeDef],
        "VpcConnectionInfo": NotRequired[VpcConnectionInfoTypeDef],
    },
)

ListClustersResponsePaginatorTypeDef = TypedDict(
    "ListClustersResponsePaginatorTypeDef",
    {
        "ClusterInfoList": List[ClusterInfoPaginatorTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ClusterPaginatorTypeDef = TypedDict(
    "ClusterPaginatorTypeDef",
    {
        "ActiveOperationArn": NotRequired[str],
        "ClusterType": NotRequired[ClusterTypeType],
        "ClusterArn": NotRequired[str],
        "ClusterName": NotRequired[str],
        "CreationTime": NotRequired[datetime],
        "CurrentVersion": NotRequired[str],
        "State": NotRequired[ClusterStateType],
        "StateInfo": NotRequired[StateInfoTypeDef],
        "Tags": NotRequired[Dict[str, str]],
        "Provisioned": NotRequired[ProvisionedPaginatorTypeDef],
        "Serverless": NotRequired[ServerlessPaginatorTypeDef],
    },
)

DescribeClusterResponseTypeDef = TypedDict(
    "DescribeClusterResponseTypeDef",
    {
        "ClusterInfo": ClusterInfoTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListClustersResponseTypeDef = TypedDict(
    "ListClustersResponseTypeDef",
    {
        "ClusterInfoList": List[ClusterInfoTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateClusterV2RequestRequestTypeDef = TypedDict(
    "CreateClusterV2RequestRequestTypeDef",
    {
        "ClusterName": str,
        "Tags": NotRequired[Mapping[str, str]],
        "Provisioned": NotRequired[ProvisionedRequestTypeDef],
        "Serverless": NotRequired[ServerlessRequestTypeDef],
    },
)

ClusterTypeDef = TypedDict(
    "ClusterTypeDef",
    {
        "ActiveOperationArn": NotRequired[str],
        "ClusterType": NotRequired[ClusterTypeType],
        "ClusterArn": NotRequired[str],
        "ClusterName": NotRequired[str],
        "CreationTime": NotRequired[datetime],
        "CurrentVersion": NotRequired[str],
        "State": NotRequired[ClusterStateType],
        "StateInfo": NotRequired[StateInfoTypeDef],
        "Tags": NotRequired[Dict[str, str]],
        "Provisioned": NotRequired[ProvisionedTypeDef],
        "Serverless": NotRequired[ServerlessTypeDef],
    },
)

ListClusterOperationsResponsePaginatorTypeDef = TypedDict(
    "ListClusterOperationsResponsePaginatorTypeDef",
    {
        "ClusterOperationInfoList": List[ClusterOperationInfoPaginatorTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeClusterOperationResponseTypeDef = TypedDict(
    "DescribeClusterOperationResponseTypeDef",
    {
        "ClusterOperationInfo": ClusterOperationInfoTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListClusterOperationsResponseTypeDef = TypedDict(
    "ListClusterOperationsResponseTypeDef",
    {
        "ClusterOperationInfoList": List[ClusterOperationInfoTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ClusterOperationV2TypeDef = TypedDict(
    "ClusterOperationV2TypeDef",
    {
        "ClusterArn": NotRequired[str],
        "ClusterType": NotRequired[ClusterTypeType],
        "StartTime": NotRequired[datetime],
        "EndTime": NotRequired[datetime],
        "ErrorInfo": NotRequired[ErrorInfoTypeDef],
        "OperationArn": NotRequired[str],
        "OperationState": NotRequired[str],
        "OperationType": NotRequired[str],
        "Provisioned": NotRequired[ClusterOperationV2ProvisionedTypeDef],
        "Serverless": NotRequired[ClusterOperationV2ServerlessTypeDef],
    },
)

ListClustersV2ResponsePaginatorTypeDef = TypedDict(
    "ListClustersV2ResponsePaginatorTypeDef",
    {
        "ClusterInfoList": List[ClusterPaginatorTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeClusterV2ResponseTypeDef = TypedDict(
    "DescribeClusterV2ResponseTypeDef",
    {
        "ClusterInfo": ClusterTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListClustersV2ResponseTypeDef = TypedDict(
    "ListClustersV2ResponseTypeDef",
    {
        "ClusterInfoList": List[ClusterTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeClusterOperationV2ResponseTypeDef = TypedDict(
    "DescribeClusterOperationV2ResponseTypeDef",
    {
        "ClusterOperationInfo": ClusterOperationV2TypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
