"""
Type annotations for personalize-events service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_personalize_events/type_defs/)

Usage::

    ```python
    from types_aiobotocore_personalize_events.type_defs import ResponseMetadataTypeDef

    data: ResponseMetadataTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Dict, Sequence, Union

if sys.version_info >= (3, 12):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired
if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "ResponseMetadataTypeDef",
    "MetricAttributionTypeDef",
    "TimestampTypeDef",
    "ItemTypeDef",
    "UserTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EventTypeDef",
    "PutItemsRequestRequestTypeDef",
    "PutUsersRequestRequestTypeDef",
    "PutEventsRequestRequestTypeDef",
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

MetricAttributionTypeDef = TypedDict(
    "MetricAttributionTypeDef",
    {
        "eventAttributionSource": str,
    },
)

TimestampTypeDef = Union[datetime, str]
ItemTypeDef = TypedDict(
    "ItemTypeDef",
    {
        "itemId": str,
        "properties": NotRequired[str],
    },
)

UserTypeDef = TypedDict(
    "UserTypeDef",
    {
        "userId": str,
        "properties": NotRequired[str],
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EventTypeDef = TypedDict(
    "EventTypeDef",
    {
        "eventType": str,
        "sentAt": TimestampTypeDef,
        "eventId": NotRequired[str],
        "eventValue": NotRequired[float],
        "itemId": NotRequired[str],
        "properties": NotRequired[str],
        "recommendationId": NotRequired[str],
        "impression": NotRequired[Sequence[str]],
        "metricAttribution": NotRequired[MetricAttributionTypeDef],
    },
)

PutItemsRequestRequestTypeDef = TypedDict(
    "PutItemsRequestRequestTypeDef",
    {
        "datasetArn": str,
        "items": Sequence[ItemTypeDef],
    },
)

PutUsersRequestRequestTypeDef = TypedDict(
    "PutUsersRequestRequestTypeDef",
    {
        "datasetArn": str,
        "users": Sequence[UserTypeDef],
    },
)

PutEventsRequestRequestTypeDef = TypedDict(
    "PutEventsRequestRequestTypeDef",
    {
        "trackingId": str,
        "sessionId": str,
        "eventList": Sequence[EventTypeDef],
        "userId": NotRequired[str],
    },
)
