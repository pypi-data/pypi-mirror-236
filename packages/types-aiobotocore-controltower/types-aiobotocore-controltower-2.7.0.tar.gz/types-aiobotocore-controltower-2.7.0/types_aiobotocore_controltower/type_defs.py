"""
Type annotations for controltower service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_controltower/type_defs/)

Usage::

    ```python
    from types_aiobotocore_controltower.type_defs import ControlOperationTypeDef

    data: ControlOperationTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Dict, List

from .literals import (
    ControlOperationStatusType,
    ControlOperationTypeType,
    DriftStatusType,
    EnablementStatusType,
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
    "ControlOperationTypeDef",
    "DisableControlInputRequestTypeDef",
    "ResponseMetadataTypeDef",
    "DriftStatusSummaryTypeDef",
    "EnableControlInputRequestTypeDef",
    "EnablementStatusSummaryTypeDef",
    "RegionTypeDef",
    "GetControlOperationInputRequestTypeDef",
    "GetEnabledControlInputRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ListEnabledControlsInputRequestTypeDef",
    "DisableControlOutputTypeDef",
    "EnableControlOutputTypeDef",
    "GetControlOperationOutputTypeDef",
    "EnabledControlSummaryTypeDef",
    "EnabledControlDetailsTypeDef",
    "ListEnabledControlsInputListEnabledControlsPaginateTypeDef",
    "ListEnabledControlsOutputTypeDef",
    "GetEnabledControlOutputTypeDef",
)

ControlOperationTypeDef = TypedDict(
    "ControlOperationTypeDef",
    {
        "endTime": NotRequired[datetime],
        "operationType": NotRequired[ControlOperationTypeType],
        "startTime": NotRequired[datetime],
        "status": NotRequired[ControlOperationStatusType],
        "statusMessage": NotRequired[str],
    },
)

DisableControlInputRequestTypeDef = TypedDict(
    "DisableControlInputRequestTypeDef",
    {
        "controlIdentifier": str,
        "targetIdentifier": str,
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

DriftStatusSummaryTypeDef = TypedDict(
    "DriftStatusSummaryTypeDef",
    {
        "driftStatus": NotRequired[DriftStatusType],
    },
)

EnableControlInputRequestTypeDef = TypedDict(
    "EnableControlInputRequestTypeDef",
    {
        "controlIdentifier": str,
        "targetIdentifier": str,
    },
)

EnablementStatusSummaryTypeDef = TypedDict(
    "EnablementStatusSummaryTypeDef",
    {
        "lastOperationIdentifier": NotRequired[str],
        "status": NotRequired[EnablementStatusType],
    },
)

RegionTypeDef = TypedDict(
    "RegionTypeDef",
    {
        "name": NotRequired[str],
    },
)

GetControlOperationInputRequestTypeDef = TypedDict(
    "GetControlOperationInputRequestTypeDef",
    {
        "operationIdentifier": str,
    },
)

GetEnabledControlInputRequestTypeDef = TypedDict(
    "GetEnabledControlInputRequestTypeDef",
    {
        "enabledControlIdentifier": str,
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

ListEnabledControlsInputRequestTypeDef = TypedDict(
    "ListEnabledControlsInputRequestTypeDef",
    {
        "targetIdentifier": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

DisableControlOutputTypeDef = TypedDict(
    "DisableControlOutputTypeDef",
    {
        "operationIdentifier": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EnableControlOutputTypeDef = TypedDict(
    "EnableControlOutputTypeDef",
    {
        "operationIdentifier": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetControlOperationOutputTypeDef = TypedDict(
    "GetControlOperationOutputTypeDef",
    {
        "controlOperation": ControlOperationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EnabledControlSummaryTypeDef = TypedDict(
    "EnabledControlSummaryTypeDef",
    {
        "arn": NotRequired[str],
        "controlIdentifier": NotRequired[str],
        "driftStatusSummary": NotRequired[DriftStatusSummaryTypeDef],
        "statusSummary": NotRequired[EnablementStatusSummaryTypeDef],
        "targetIdentifier": NotRequired[str],
    },
)

EnabledControlDetailsTypeDef = TypedDict(
    "EnabledControlDetailsTypeDef",
    {
        "arn": NotRequired[str],
        "controlIdentifier": NotRequired[str],
        "driftStatusSummary": NotRequired[DriftStatusSummaryTypeDef],
        "statusSummary": NotRequired[EnablementStatusSummaryTypeDef],
        "targetIdentifier": NotRequired[str],
        "targetRegions": NotRequired[List[RegionTypeDef]],
    },
)

ListEnabledControlsInputListEnabledControlsPaginateTypeDef = TypedDict(
    "ListEnabledControlsInputListEnabledControlsPaginateTypeDef",
    {
        "targetIdentifier": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListEnabledControlsOutputTypeDef = TypedDict(
    "ListEnabledControlsOutputTypeDef",
    {
        "enabledControls": List[EnabledControlSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetEnabledControlOutputTypeDef = TypedDict(
    "GetEnabledControlOutputTypeDef",
    {
        "enabledControlDetails": EnabledControlDetailsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
