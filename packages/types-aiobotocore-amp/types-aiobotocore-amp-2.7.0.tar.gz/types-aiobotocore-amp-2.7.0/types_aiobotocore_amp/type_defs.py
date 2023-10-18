"""
Type annotations for amp service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amp/type_defs/)

Usage::

    ```python
    from types_aiobotocore_amp.type_defs import AlertManagerDefinitionStatusTypeDef

    data: AlertManagerDefinitionStatusTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from aiobotocore.response import StreamingBody

from .literals import (
    AlertManagerDefinitionStatusCodeType,
    LoggingConfigurationStatusCodeType,
    RuleGroupsNamespaceStatusCodeType,
    WorkspaceStatusCodeType,
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
    "AlertManagerDefinitionStatusTypeDef",
    "BlobTypeDef",
    "ResponseMetadataTypeDef",
    "CreateLoggingConfigurationRequestRequestTypeDef",
    "LoggingConfigurationStatusTypeDef",
    "RuleGroupsNamespaceStatusTypeDef",
    "CreateWorkspaceRequestRequestTypeDef",
    "WorkspaceStatusTypeDef",
    "DeleteAlertManagerDefinitionRequestRequestTypeDef",
    "DeleteLoggingConfigurationRequestRequestTypeDef",
    "DeleteRuleGroupsNamespaceRequestRequestTypeDef",
    "DeleteWorkspaceRequestRequestTypeDef",
    "DescribeAlertManagerDefinitionRequestRequestTypeDef",
    "DescribeLoggingConfigurationRequestRequestTypeDef",
    "DescribeRuleGroupsNamespaceRequestRequestTypeDef",
    "DescribeWorkspaceRequestRequestTypeDef",
    "WaiterConfigTypeDef",
    "PaginatorConfigTypeDef",
    "ListRuleGroupsNamespacesRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListWorkspacesRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateLoggingConfigurationRequestRequestTypeDef",
    "UpdateWorkspaceAliasRequestRequestTypeDef",
    "AlertManagerDefinitionDescriptionTypeDef",
    "CreateAlertManagerDefinitionRequestRequestTypeDef",
    "CreateRuleGroupsNamespaceRequestRequestTypeDef",
    "PutAlertManagerDefinitionRequestRequestTypeDef",
    "PutRuleGroupsNamespaceRequestRequestTypeDef",
    "CreateAlertManagerDefinitionResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PutAlertManagerDefinitionResponseTypeDef",
    "CreateLoggingConfigurationResponseTypeDef",
    "LoggingConfigurationMetadataTypeDef",
    "UpdateLoggingConfigurationResponseTypeDef",
    "CreateRuleGroupsNamespaceResponseTypeDef",
    "PutRuleGroupsNamespaceResponseTypeDef",
    "RuleGroupsNamespaceDescriptionTypeDef",
    "RuleGroupsNamespaceSummaryTypeDef",
    "CreateWorkspaceResponseTypeDef",
    "WorkspaceDescriptionTypeDef",
    "WorkspaceSummaryTypeDef",
    "DescribeWorkspaceRequestWorkspaceActiveWaitTypeDef",
    "DescribeWorkspaceRequestWorkspaceDeletedWaitTypeDef",
    "ListRuleGroupsNamespacesRequestListRuleGroupsNamespacesPaginateTypeDef",
    "ListWorkspacesRequestListWorkspacesPaginateTypeDef",
    "DescribeAlertManagerDefinitionResponseTypeDef",
    "DescribeLoggingConfigurationResponseTypeDef",
    "DescribeRuleGroupsNamespaceResponseTypeDef",
    "ListRuleGroupsNamespacesResponseTypeDef",
    "DescribeWorkspaceResponseTypeDef",
    "ListWorkspacesResponseTypeDef",
)

AlertManagerDefinitionStatusTypeDef = TypedDict(
    "AlertManagerDefinitionStatusTypeDef",
    {
        "statusCode": AlertManagerDefinitionStatusCodeType,
        "statusReason": NotRequired[str],
    },
)

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]
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

CreateLoggingConfigurationRequestRequestTypeDef = TypedDict(
    "CreateLoggingConfigurationRequestRequestTypeDef",
    {
        "workspaceId": str,
        "logGroupArn": str,
        "clientToken": NotRequired[str],
    },
)

LoggingConfigurationStatusTypeDef = TypedDict(
    "LoggingConfigurationStatusTypeDef",
    {
        "statusCode": LoggingConfigurationStatusCodeType,
        "statusReason": NotRequired[str],
    },
)

RuleGroupsNamespaceStatusTypeDef = TypedDict(
    "RuleGroupsNamespaceStatusTypeDef",
    {
        "statusCode": RuleGroupsNamespaceStatusCodeType,
        "statusReason": NotRequired[str],
    },
)

CreateWorkspaceRequestRequestTypeDef = TypedDict(
    "CreateWorkspaceRequestRequestTypeDef",
    {
        "alias": NotRequired[str],
        "clientToken": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)

WorkspaceStatusTypeDef = TypedDict(
    "WorkspaceStatusTypeDef",
    {
        "statusCode": WorkspaceStatusCodeType,
    },
)

DeleteAlertManagerDefinitionRequestRequestTypeDef = TypedDict(
    "DeleteAlertManagerDefinitionRequestRequestTypeDef",
    {
        "workspaceId": str,
        "clientToken": NotRequired[str],
    },
)

DeleteLoggingConfigurationRequestRequestTypeDef = TypedDict(
    "DeleteLoggingConfigurationRequestRequestTypeDef",
    {
        "workspaceId": str,
        "clientToken": NotRequired[str],
    },
)

DeleteRuleGroupsNamespaceRequestRequestTypeDef = TypedDict(
    "DeleteRuleGroupsNamespaceRequestRequestTypeDef",
    {
        "workspaceId": str,
        "name": str,
        "clientToken": NotRequired[str],
    },
)

DeleteWorkspaceRequestRequestTypeDef = TypedDict(
    "DeleteWorkspaceRequestRequestTypeDef",
    {
        "workspaceId": str,
        "clientToken": NotRequired[str],
    },
)

DescribeAlertManagerDefinitionRequestRequestTypeDef = TypedDict(
    "DescribeAlertManagerDefinitionRequestRequestTypeDef",
    {
        "workspaceId": str,
    },
)

DescribeLoggingConfigurationRequestRequestTypeDef = TypedDict(
    "DescribeLoggingConfigurationRequestRequestTypeDef",
    {
        "workspaceId": str,
    },
)

DescribeRuleGroupsNamespaceRequestRequestTypeDef = TypedDict(
    "DescribeRuleGroupsNamespaceRequestRequestTypeDef",
    {
        "workspaceId": str,
        "name": str,
    },
)

DescribeWorkspaceRequestRequestTypeDef = TypedDict(
    "DescribeWorkspaceRequestRequestTypeDef",
    {
        "workspaceId": str,
    },
)

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": NotRequired[int],
        "MaxAttempts": NotRequired[int],
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

ListRuleGroupsNamespacesRequestRequestTypeDef = TypedDict(
    "ListRuleGroupsNamespacesRequestRequestTypeDef",
    {
        "workspaceId": str,
        "name": NotRequired[str],
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

ListWorkspacesRequestRequestTypeDef = TypedDict(
    "ListWorkspacesRequestRequestTypeDef",
    {
        "nextToken": NotRequired[str],
        "alias": NotRequired[str],
        "maxResults": NotRequired[int],
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

UpdateLoggingConfigurationRequestRequestTypeDef = TypedDict(
    "UpdateLoggingConfigurationRequestRequestTypeDef",
    {
        "workspaceId": str,
        "logGroupArn": str,
        "clientToken": NotRequired[str],
    },
)

UpdateWorkspaceAliasRequestRequestTypeDef = TypedDict(
    "UpdateWorkspaceAliasRequestRequestTypeDef",
    {
        "workspaceId": str,
        "alias": NotRequired[str],
        "clientToken": NotRequired[str],
    },
)

AlertManagerDefinitionDescriptionTypeDef = TypedDict(
    "AlertManagerDefinitionDescriptionTypeDef",
    {
        "status": AlertManagerDefinitionStatusTypeDef,
        "data": bytes,
        "createdAt": datetime,
        "modifiedAt": datetime,
    },
)

CreateAlertManagerDefinitionRequestRequestTypeDef = TypedDict(
    "CreateAlertManagerDefinitionRequestRequestTypeDef",
    {
        "workspaceId": str,
        "data": BlobTypeDef,
        "clientToken": NotRequired[str],
    },
)

CreateRuleGroupsNamespaceRequestRequestTypeDef = TypedDict(
    "CreateRuleGroupsNamespaceRequestRequestTypeDef",
    {
        "workspaceId": str,
        "name": str,
        "data": BlobTypeDef,
        "clientToken": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)

PutAlertManagerDefinitionRequestRequestTypeDef = TypedDict(
    "PutAlertManagerDefinitionRequestRequestTypeDef",
    {
        "workspaceId": str,
        "data": BlobTypeDef,
        "clientToken": NotRequired[str],
    },
)

PutRuleGroupsNamespaceRequestRequestTypeDef = TypedDict(
    "PutRuleGroupsNamespaceRequestRequestTypeDef",
    {
        "workspaceId": str,
        "name": str,
        "data": BlobTypeDef,
        "clientToken": NotRequired[str],
    },
)

CreateAlertManagerDefinitionResponseTypeDef = TypedDict(
    "CreateAlertManagerDefinitionResponseTypeDef",
    {
        "status": AlertManagerDefinitionStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
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

PutAlertManagerDefinitionResponseTypeDef = TypedDict(
    "PutAlertManagerDefinitionResponseTypeDef",
    {
        "status": AlertManagerDefinitionStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateLoggingConfigurationResponseTypeDef = TypedDict(
    "CreateLoggingConfigurationResponseTypeDef",
    {
        "status": LoggingConfigurationStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

LoggingConfigurationMetadataTypeDef = TypedDict(
    "LoggingConfigurationMetadataTypeDef",
    {
        "status": LoggingConfigurationStatusTypeDef,
        "workspace": str,
        "logGroupArn": str,
        "createdAt": datetime,
        "modifiedAt": datetime,
    },
)

UpdateLoggingConfigurationResponseTypeDef = TypedDict(
    "UpdateLoggingConfigurationResponseTypeDef",
    {
        "status": LoggingConfigurationStatusTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateRuleGroupsNamespaceResponseTypeDef = TypedDict(
    "CreateRuleGroupsNamespaceResponseTypeDef",
    {
        "name": str,
        "arn": str,
        "status": RuleGroupsNamespaceStatusTypeDef,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutRuleGroupsNamespaceResponseTypeDef = TypedDict(
    "PutRuleGroupsNamespaceResponseTypeDef",
    {
        "name": str,
        "arn": str,
        "status": RuleGroupsNamespaceStatusTypeDef,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RuleGroupsNamespaceDescriptionTypeDef = TypedDict(
    "RuleGroupsNamespaceDescriptionTypeDef",
    {
        "arn": str,
        "name": str,
        "status": RuleGroupsNamespaceStatusTypeDef,
        "data": bytes,
        "createdAt": datetime,
        "modifiedAt": datetime,
        "tags": NotRequired[Dict[str, str]],
    },
)

RuleGroupsNamespaceSummaryTypeDef = TypedDict(
    "RuleGroupsNamespaceSummaryTypeDef",
    {
        "arn": str,
        "name": str,
        "status": RuleGroupsNamespaceStatusTypeDef,
        "createdAt": datetime,
        "modifiedAt": datetime,
        "tags": NotRequired[Dict[str, str]],
    },
)

CreateWorkspaceResponseTypeDef = TypedDict(
    "CreateWorkspaceResponseTypeDef",
    {
        "workspaceId": str,
        "arn": str,
        "status": WorkspaceStatusTypeDef,
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

WorkspaceDescriptionTypeDef = TypedDict(
    "WorkspaceDescriptionTypeDef",
    {
        "workspaceId": str,
        "arn": str,
        "status": WorkspaceStatusTypeDef,
        "createdAt": datetime,
        "alias": NotRequired[str],
        "prometheusEndpoint": NotRequired[str],
        "tags": NotRequired[Dict[str, str]],
    },
)

WorkspaceSummaryTypeDef = TypedDict(
    "WorkspaceSummaryTypeDef",
    {
        "workspaceId": str,
        "arn": str,
        "status": WorkspaceStatusTypeDef,
        "createdAt": datetime,
        "alias": NotRequired[str],
        "tags": NotRequired[Dict[str, str]],
    },
)

DescribeWorkspaceRequestWorkspaceActiveWaitTypeDef = TypedDict(
    "DescribeWorkspaceRequestWorkspaceActiveWaitTypeDef",
    {
        "workspaceId": str,
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)

DescribeWorkspaceRequestWorkspaceDeletedWaitTypeDef = TypedDict(
    "DescribeWorkspaceRequestWorkspaceDeletedWaitTypeDef",
    {
        "workspaceId": str,
        "WaiterConfig": NotRequired[WaiterConfigTypeDef],
    },
)

ListRuleGroupsNamespacesRequestListRuleGroupsNamespacesPaginateTypeDef = TypedDict(
    "ListRuleGroupsNamespacesRequestListRuleGroupsNamespacesPaginateTypeDef",
    {
        "workspaceId": str,
        "name": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListWorkspacesRequestListWorkspacesPaginateTypeDef = TypedDict(
    "ListWorkspacesRequestListWorkspacesPaginateTypeDef",
    {
        "alias": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

DescribeAlertManagerDefinitionResponseTypeDef = TypedDict(
    "DescribeAlertManagerDefinitionResponseTypeDef",
    {
        "alertManagerDefinition": AlertManagerDefinitionDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeLoggingConfigurationResponseTypeDef = TypedDict(
    "DescribeLoggingConfigurationResponseTypeDef",
    {
        "loggingConfiguration": LoggingConfigurationMetadataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeRuleGroupsNamespaceResponseTypeDef = TypedDict(
    "DescribeRuleGroupsNamespaceResponseTypeDef",
    {
        "ruleGroupsNamespace": RuleGroupsNamespaceDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListRuleGroupsNamespacesResponseTypeDef = TypedDict(
    "ListRuleGroupsNamespacesResponseTypeDef",
    {
        "ruleGroupsNamespaces": List[RuleGroupsNamespaceSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeWorkspaceResponseTypeDef = TypedDict(
    "DescribeWorkspaceResponseTypeDef",
    {
        "workspace": WorkspaceDescriptionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListWorkspacesResponseTypeDef = TypedDict(
    "ListWorkspacesResponseTypeDef",
    {
        "workspaces": List[WorkspaceSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
