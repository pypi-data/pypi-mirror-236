"""
Type annotations for codestar-connections service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar_connections/type_defs/)

Usage::

    ```python
    from types_aiobotocore_codestar_connections.type_defs import ConnectionTypeDef

    data: ConnectionTypeDef = ...
    ```
"""

import sys
from typing import Dict, List, Sequence

from .literals import ConnectionStatusType, ProviderTypeType

if sys.version_info >= (3, 12):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired
if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "ConnectionTypeDef",
    "TagTypeDef",
    "ResponseMetadataTypeDef",
    "VpcConfigurationTypeDef",
    "DeleteConnectionInputRequestTypeDef",
    "DeleteHostInputRequestTypeDef",
    "GetConnectionInputRequestTypeDef",
    "GetHostInputRequestTypeDef",
    "ListConnectionsInputRequestTypeDef",
    "ListHostsInputRequestTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "UntagResourceInputRequestTypeDef",
    "CreateConnectionInputRequestTypeDef",
    "TagResourceInputRequestTypeDef",
    "CreateConnectionOutputTypeDef",
    "CreateHostOutputTypeDef",
    "GetConnectionOutputTypeDef",
    "ListConnectionsOutputTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "CreateHostInputRequestTypeDef",
    "GetHostOutputTypeDef",
    "HostTypeDef",
    "UpdateHostInputRequestTypeDef",
    "ListHostsOutputTypeDef",
)

ConnectionTypeDef = TypedDict(
    "ConnectionTypeDef",
    {
        "ConnectionName": NotRequired[str],
        "ConnectionArn": NotRequired[str],
        "ProviderType": NotRequired[ProviderTypeType],
        "OwnerAccountId": NotRequired[str],
        "ConnectionStatus": NotRequired[ConnectionStatusType],
        "HostArn": NotRequired[str],
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
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

VpcConfigurationTypeDef = TypedDict(
    "VpcConfigurationTypeDef",
    {
        "VpcId": str,
        "SubnetIds": Sequence[str],
        "SecurityGroupIds": Sequence[str],
        "TlsCertificate": NotRequired[str],
    },
)

DeleteConnectionInputRequestTypeDef = TypedDict(
    "DeleteConnectionInputRequestTypeDef",
    {
        "ConnectionArn": str,
    },
)

DeleteHostInputRequestTypeDef = TypedDict(
    "DeleteHostInputRequestTypeDef",
    {
        "HostArn": str,
    },
)

GetConnectionInputRequestTypeDef = TypedDict(
    "GetConnectionInputRequestTypeDef",
    {
        "ConnectionArn": str,
    },
)

GetHostInputRequestTypeDef = TypedDict(
    "GetHostInputRequestTypeDef",
    {
        "HostArn": str,
    },
)

ListConnectionsInputRequestTypeDef = TypedDict(
    "ListConnectionsInputRequestTypeDef",
    {
        "ProviderTypeFilter": NotRequired[ProviderTypeType],
        "HostArnFilter": NotRequired[str],
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

ListHostsInputRequestTypeDef = TypedDict(
    "ListHostsInputRequestTypeDef",
    {
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

ListTagsForResourceInputRequestTypeDef = TypedDict(
    "ListTagsForResourceInputRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

UntagResourceInputRequestTypeDef = TypedDict(
    "UntagResourceInputRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

CreateConnectionInputRequestTypeDef = TypedDict(
    "CreateConnectionInputRequestTypeDef",
    {
        "ConnectionName": str,
        "ProviderType": NotRequired[ProviderTypeType],
        "Tags": NotRequired[Sequence[TagTypeDef]],
        "HostArn": NotRequired[str],
    },
)

TagResourceInputRequestTypeDef = TypedDict(
    "TagResourceInputRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Sequence[TagTypeDef],
    },
)

CreateConnectionOutputTypeDef = TypedDict(
    "CreateConnectionOutputTypeDef",
    {
        "ConnectionArn": str,
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateHostOutputTypeDef = TypedDict(
    "CreateHostOutputTypeDef",
    {
        "HostArn": str,
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetConnectionOutputTypeDef = TypedDict(
    "GetConnectionOutputTypeDef",
    {
        "Connection": ConnectionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListConnectionsOutputTypeDef = TypedDict(
    "ListConnectionsOutputTypeDef",
    {
        "Connections": List[ConnectionTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceOutputTypeDef = TypedDict(
    "ListTagsForResourceOutputTypeDef",
    {
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateHostInputRequestTypeDef = TypedDict(
    "CreateHostInputRequestTypeDef",
    {
        "Name": str,
        "ProviderType": ProviderTypeType,
        "ProviderEndpoint": str,
        "VpcConfiguration": NotRequired[VpcConfigurationTypeDef],
        "Tags": NotRequired[Sequence[TagTypeDef]],
    },
)

GetHostOutputTypeDef = TypedDict(
    "GetHostOutputTypeDef",
    {
        "Name": str,
        "Status": str,
        "ProviderType": ProviderTypeType,
        "ProviderEndpoint": str,
        "VpcConfiguration": VpcConfigurationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

HostTypeDef = TypedDict(
    "HostTypeDef",
    {
        "Name": NotRequired[str],
        "HostArn": NotRequired[str],
        "ProviderType": NotRequired[ProviderTypeType],
        "ProviderEndpoint": NotRequired[str],
        "VpcConfiguration": NotRequired[VpcConfigurationTypeDef],
        "Status": NotRequired[str],
        "StatusMessage": NotRequired[str],
    },
)

UpdateHostInputRequestTypeDef = TypedDict(
    "UpdateHostInputRequestTypeDef",
    {
        "HostArn": str,
        "ProviderEndpoint": NotRequired[str],
        "VpcConfiguration": NotRequired[VpcConfigurationTypeDef],
    },
)

ListHostsOutputTypeDef = TypedDict(
    "ListHostsOutputTypeDef",
    {
        "Hosts": List[HostTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
