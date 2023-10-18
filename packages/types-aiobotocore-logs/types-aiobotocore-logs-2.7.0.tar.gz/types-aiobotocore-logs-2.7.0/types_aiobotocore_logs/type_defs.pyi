"""
Type annotations for logs service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/type_defs/)

Usage::

    ```python
    from types_aiobotocore_logs.type_defs import AccountPolicyTypeDef

    data: AccountPolicyTypeDef = ...
    ```
"""

import sys
from typing import Dict, List, Mapping, Sequence

from .literals import (
    DataProtectionStatusType,
    DistributionType,
    ExportTaskStatusCodeType,
    OrderByType,
    QueryStatusType,
    StandardUnitType,
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
    "AccountPolicyTypeDef",
    "AssociateKmsKeyRequestRequestTypeDef",
    "CancelExportTaskRequestRequestTypeDef",
    "CreateExportTaskRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "CreateLogGroupRequestRequestTypeDef",
    "CreateLogStreamRequestRequestTypeDef",
    "DeleteAccountPolicyRequestRequestTypeDef",
    "DeleteDataProtectionPolicyRequestRequestTypeDef",
    "DeleteDestinationRequestRequestTypeDef",
    "DeleteLogGroupRequestRequestTypeDef",
    "DeleteLogStreamRequestRequestTypeDef",
    "DeleteMetricFilterRequestRequestTypeDef",
    "DeleteQueryDefinitionRequestRequestTypeDef",
    "DeleteResourcePolicyRequestRequestTypeDef",
    "DeleteRetentionPolicyRequestRequestTypeDef",
    "DeleteSubscriptionFilterRequestRequestTypeDef",
    "DescribeAccountPoliciesRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeDestinationsRequestRequestTypeDef",
    "DestinationTypeDef",
    "DescribeExportTasksRequestRequestTypeDef",
    "DescribeLogGroupsRequestRequestTypeDef",
    "LogGroupTypeDef",
    "DescribeLogStreamsRequestRequestTypeDef",
    "LogStreamTypeDef",
    "DescribeMetricFiltersRequestRequestTypeDef",
    "DescribeQueriesRequestRequestTypeDef",
    "QueryInfoTypeDef",
    "DescribeQueryDefinitionsRequestRequestTypeDef",
    "QueryDefinitionTypeDef",
    "DescribeResourcePoliciesRequestRequestTypeDef",
    "ResourcePolicyTypeDef",
    "DescribeSubscriptionFiltersRequestRequestTypeDef",
    "SubscriptionFilterTypeDef",
    "DisassociateKmsKeyRequestRequestTypeDef",
    "ExportTaskExecutionInfoTypeDef",
    "ExportTaskStatusTypeDef",
    "FilterLogEventsRequestRequestTypeDef",
    "FilteredLogEventTypeDef",
    "SearchedLogStreamTypeDef",
    "GetDataProtectionPolicyRequestRequestTypeDef",
    "GetLogEventsRequestRequestTypeDef",
    "OutputLogEventTypeDef",
    "GetLogGroupFieldsRequestRequestTypeDef",
    "LogGroupFieldTypeDef",
    "GetLogRecordRequestRequestTypeDef",
    "GetQueryResultsRequestRequestTypeDef",
    "QueryStatisticsTypeDef",
    "ResultFieldTypeDef",
    "InputLogEventTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsLogGroupRequestRequestTypeDef",
    "MetricFilterMatchRecordTypeDef",
    "MetricTransformationTypeDef",
    "PutAccountPolicyRequestRequestTypeDef",
    "PutDataProtectionPolicyRequestRequestTypeDef",
    "PutDestinationPolicyRequestRequestTypeDef",
    "PutDestinationRequestRequestTypeDef",
    "RejectedLogEventsInfoTypeDef",
    "PutQueryDefinitionRequestRequestTypeDef",
    "PutResourcePolicyRequestRequestTypeDef",
    "PutRetentionPolicyRequestRequestTypeDef",
    "PutSubscriptionFilterRequestRequestTypeDef",
    "StartQueryRequestRequestTypeDef",
    "StopQueryRequestRequestTypeDef",
    "TagLogGroupRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TestMetricFilterRequestRequestTypeDef",
    "UntagLogGroupRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "CreateExportTaskResponseTypeDef",
    "DeleteQueryDefinitionResponseTypeDef",
    "DescribeAccountPoliciesResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "GetDataProtectionPolicyResponseTypeDef",
    "GetLogRecordResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTagsLogGroupResponseTypeDef",
    "PutAccountPolicyResponseTypeDef",
    "PutDataProtectionPolicyResponseTypeDef",
    "PutQueryDefinitionResponseTypeDef",
    "StartQueryResponseTypeDef",
    "StopQueryResponseTypeDef",
    "DescribeDestinationsRequestDescribeDestinationsPaginateTypeDef",
    "DescribeExportTasksRequestDescribeExportTasksPaginateTypeDef",
    "DescribeLogGroupsRequestDescribeLogGroupsPaginateTypeDef",
    "DescribeLogStreamsRequestDescribeLogStreamsPaginateTypeDef",
    "DescribeMetricFiltersRequestDescribeMetricFiltersPaginateTypeDef",
    "DescribeQueriesRequestDescribeQueriesPaginateTypeDef",
    "DescribeResourcePoliciesRequestDescribeResourcePoliciesPaginateTypeDef",
    "DescribeSubscriptionFiltersRequestDescribeSubscriptionFiltersPaginateTypeDef",
    "FilterLogEventsRequestFilterLogEventsPaginateTypeDef",
    "DescribeDestinationsResponseTypeDef",
    "PutDestinationResponseTypeDef",
    "DescribeLogGroupsResponseTypeDef",
    "DescribeLogStreamsResponseTypeDef",
    "DescribeQueriesResponseTypeDef",
    "DescribeQueryDefinitionsResponseTypeDef",
    "DescribeResourcePoliciesResponseTypeDef",
    "PutResourcePolicyResponseTypeDef",
    "DescribeSubscriptionFiltersResponseTypeDef",
    "ExportTaskTypeDef",
    "FilterLogEventsResponseTypeDef",
    "GetLogEventsResponseTypeDef",
    "GetLogGroupFieldsResponseTypeDef",
    "GetQueryResultsResponseTypeDef",
    "PutLogEventsRequestRequestTypeDef",
    "TestMetricFilterResponseTypeDef",
    "MetricFilterTypeDef",
    "PutMetricFilterRequestRequestTypeDef",
    "PutLogEventsResponseTypeDef",
    "DescribeExportTasksResponseTypeDef",
    "DescribeMetricFiltersResponseTypeDef",
)

AccountPolicyTypeDef = TypedDict(
    "AccountPolicyTypeDef",
    {
        "policyName": NotRequired[str],
        "policyDocument": NotRequired[str],
        "lastUpdatedTime": NotRequired[int],
        "policyType": NotRequired[Literal["DATA_PROTECTION_POLICY"]],
        "scope": NotRequired[Literal["ALL"]],
        "accountId": NotRequired[str],
    },
)

AssociateKmsKeyRequestRequestTypeDef = TypedDict(
    "AssociateKmsKeyRequestRequestTypeDef",
    {
        "kmsKeyId": str,
        "logGroupName": NotRequired[str],
        "resourceIdentifier": NotRequired[str],
    },
)

CancelExportTaskRequestRequestTypeDef = TypedDict(
    "CancelExportTaskRequestRequestTypeDef",
    {
        "taskId": str,
    },
)

CreateExportTaskRequestRequestTypeDef = TypedDict(
    "CreateExportTaskRequestRequestTypeDef",
    {
        "logGroupName": str,
        "fromTime": int,
        "to": int,
        "destination": str,
        "taskName": NotRequired[str],
        "logStreamNamePrefix": NotRequired[str],
        "destinationPrefix": NotRequired[str],
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

CreateLogGroupRequestRequestTypeDef = TypedDict(
    "CreateLogGroupRequestRequestTypeDef",
    {
        "logGroupName": str,
        "kmsKeyId": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)

CreateLogStreamRequestRequestTypeDef = TypedDict(
    "CreateLogStreamRequestRequestTypeDef",
    {
        "logGroupName": str,
        "logStreamName": str,
    },
)

DeleteAccountPolicyRequestRequestTypeDef = TypedDict(
    "DeleteAccountPolicyRequestRequestTypeDef",
    {
        "policyName": str,
        "policyType": Literal["DATA_PROTECTION_POLICY"],
    },
)

DeleteDataProtectionPolicyRequestRequestTypeDef = TypedDict(
    "DeleteDataProtectionPolicyRequestRequestTypeDef",
    {
        "logGroupIdentifier": str,
    },
)

DeleteDestinationRequestRequestTypeDef = TypedDict(
    "DeleteDestinationRequestRequestTypeDef",
    {
        "destinationName": str,
    },
)

DeleteLogGroupRequestRequestTypeDef = TypedDict(
    "DeleteLogGroupRequestRequestTypeDef",
    {
        "logGroupName": str,
    },
)

DeleteLogStreamRequestRequestTypeDef = TypedDict(
    "DeleteLogStreamRequestRequestTypeDef",
    {
        "logGroupName": str,
        "logStreamName": str,
    },
)

DeleteMetricFilterRequestRequestTypeDef = TypedDict(
    "DeleteMetricFilterRequestRequestTypeDef",
    {
        "logGroupName": str,
        "filterName": str,
    },
)

DeleteQueryDefinitionRequestRequestTypeDef = TypedDict(
    "DeleteQueryDefinitionRequestRequestTypeDef",
    {
        "queryDefinitionId": str,
    },
)

DeleteResourcePolicyRequestRequestTypeDef = TypedDict(
    "DeleteResourcePolicyRequestRequestTypeDef",
    {
        "policyName": NotRequired[str],
    },
)

DeleteRetentionPolicyRequestRequestTypeDef = TypedDict(
    "DeleteRetentionPolicyRequestRequestTypeDef",
    {
        "logGroupName": str,
    },
)

DeleteSubscriptionFilterRequestRequestTypeDef = TypedDict(
    "DeleteSubscriptionFilterRequestRequestTypeDef",
    {
        "logGroupName": str,
        "filterName": str,
    },
)

DescribeAccountPoliciesRequestRequestTypeDef = TypedDict(
    "DescribeAccountPoliciesRequestRequestTypeDef",
    {
        "policyType": Literal["DATA_PROTECTION_POLICY"],
        "policyName": NotRequired[str],
        "accountIdentifiers": NotRequired[Sequence[str]],
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

DescribeDestinationsRequestRequestTypeDef = TypedDict(
    "DescribeDestinationsRequestRequestTypeDef",
    {
        "DestinationNamePrefix": NotRequired[str],
        "nextToken": NotRequired[str],
        "limit": NotRequired[int],
    },
)

DestinationTypeDef = TypedDict(
    "DestinationTypeDef",
    {
        "destinationName": NotRequired[str],
        "targetArn": NotRequired[str],
        "roleArn": NotRequired[str],
        "accessPolicy": NotRequired[str],
        "arn": NotRequired[str],
        "creationTime": NotRequired[int],
    },
)

DescribeExportTasksRequestRequestTypeDef = TypedDict(
    "DescribeExportTasksRequestRequestTypeDef",
    {
        "taskId": NotRequired[str],
        "statusCode": NotRequired[ExportTaskStatusCodeType],
        "nextToken": NotRequired[str],
        "limit": NotRequired[int],
    },
)

DescribeLogGroupsRequestRequestTypeDef = TypedDict(
    "DescribeLogGroupsRequestRequestTypeDef",
    {
        "accountIdentifiers": NotRequired[Sequence[str]],
        "logGroupNamePrefix": NotRequired[str],
        "logGroupNamePattern": NotRequired[str],
        "nextToken": NotRequired[str],
        "limit": NotRequired[int],
        "includeLinkedAccounts": NotRequired[bool],
    },
)

LogGroupTypeDef = TypedDict(
    "LogGroupTypeDef",
    {
        "logGroupName": NotRequired[str],
        "creationTime": NotRequired[int],
        "retentionInDays": NotRequired[int],
        "metricFilterCount": NotRequired[int],
        "arn": NotRequired[str],
        "storedBytes": NotRequired[int],
        "kmsKeyId": NotRequired[str],
        "dataProtectionStatus": NotRequired[DataProtectionStatusType],
        "inheritedProperties": NotRequired[List[Literal["ACCOUNT_DATA_PROTECTION"]]],
    },
)

DescribeLogStreamsRequestRequestTypeDef = TypedDict(
    "DescribeLogStreamsRequestRequestTypeDef",
    {
        "logGroupName": NotRequired[str],
        "logGroupIdentifier": NotRequired[str],
        "logStreamNamePrefix": NotRequired[str],
        "orderBy": NotRequired[OrderByType],
        "descending": NotRequired[bool],
        "nextToken": NotRequired[str],
        "limit": NotRequired[int],
    },
)

LogStreamTypeDef = TypedDict(
    "LogStreamTypeDef",
    {
        "logStreamName": NotRequired[str],
        "creationTime": NotRequired[int],
        "firstEventTimestamp": NotRequired[int],
        "lastEventTimestamp": NotRequired[int],
        "lastIngestionTime": NotRequired[int],
        "uploadSequenceToken": NotRequired[str],
        "arn": NotRequired[str],
        "storedBytes": NotRequired[int],
    },
)

DescribeMetricFiltersRequestRequestTypeDef = TypedDict(
    "DescribeMetricFiltersRequestRequestTypeDef",
    {
        "logGroupName": NotRequired[str],
        "filterNamePrefix": NotRequired[str],
        "nextToken": NotRequired[str],
        "limit": NotRequired[int],
        "metricName": NotRequired[str],
        "metricNamespace": NotRequired[str],
    },
)

DescribeQueriesRequestRequestTypeDef = TypedDict(
    "DescribeQueriesRequestRequestTypeDef",
    {
        "logGroupName": NotRequired[str],
        "status": NotRequired[QueryStatusType],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

QueryInfoTypeDef = TypedDict(
    "QueryInfoTypeDef",
    {
        "queryId": NotRequired[str],
        "queryString": NotRequired[str],
        "status": NotRequired[QueryStatusType],
        "createTime": NotRequired[int],
        "logGroupName": NotRequired[str],
    },
)

DescribeQueryDefinitionsRequestRequestTypeDef = TypedDict(
    "DescribeQueryDefinitionsRequestRequestTypeDef",
    {
        "queryDefinitionNamePrefix": NotRequired[str],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)

QueryDefinitionTypeDef = TypedDict(
    "QueryDefinitionTypeDef",
    {
        "queryDefinitionId": NotRequired[str],
        "name": NotRequired[str],
        "queryString": NotRequired[str],
        "lastModified": NotRequired[int],
        "logGroupNames": NotRequired[List[str]],
    },
)

DescribeResourcePoliciesRequestRequestTypeDef = TypedDict(
    "DescribeResourcePoliciesRequestRequestTypeDef",
    {
        "nextToken": NotRequired[str],
        "limit": NotRequired[int],
    },
)

ResourcePolicyTypeDef = TypedDict(
    "ResourcePolicyTypeDef",
    {
        "policyName": NotRequired[str],
        "policyDocument": NotRequired[str],
        "lastUpdatedTime": NotRequired[int],
    },
)

DescribeSubscriptionFiltersRequestRequestTypeDef = TypedDict(
    "DescribeSubscriptionFiltersRequestRequestTypeDef",
    {
        "logGroupName": str,
        "filterNamePrefix": NotRequired[str],
        "nextToken": NotRequired[str],
        "limit": NotRequired[int],
    },
)

SubscriptionFilterTypeDef = TypedDict(
    "SubscriptionFilterTypeDef",
    {
        "filterName": NotRequired[str],
        "logGroupName": NotRequired[str],
        "filterPattern": NotRequired[str],
        "destinationArn": NotRequired[str],
        "roleArn": NotRequired[str],
        "distribution": NotRequired[DistributionType],
        "creationTime": NotRequired[int],
    },
)

DisassociateKmsKeyRequestRequestTypeDef = TypedDict(
    "DisassociateKmsKeyRequestRequestTypeDef",
    {
        "logGroupName": NotRequired[str],
        "resourceIdentifier": NotRequired[str],
    },
)

ExportTaskExecutionInfoTypeDef = TypedDict(
    "ExportTaskExecutionInfoTypeDef",
    {
        "creationTime": NotRequired[int],
        "completionTime": NotRequired[int],
    },
)

ExportTaskStatusTypeDef = TypedDict(
    "ExportTaskStatusTypeDef",
    {
        "code": NotRequired[ExportTaskStatusCodeType],
        "message": NotRequired[str],
    },
)

FilterLogEventsRequestRequestTypeDef = TypedDict(
    "FilterLogEventsRequestRequestTypeDef",
    {
        "logGroupName": NotRequired[str],
        "logGroupIdentifier": NotRequired[str],
        "logStreamNames": NotRequired[Sequence[str]],
        "logStreamNamePrefix": NotRequired[str],
        "startTime": NotRequired[int],
        "endTime": NotRequired[int],
        "filterPattern": NotRequired[str],
        "nextToken": NotRequired[str],
        "limit": NotRequired[int],
        "interleaved": NotRequired[bool],
        "unmask": NotRequired[bool],
    },
)

FilteredLogEventTypeDef = TypedDict(
    "FilteredLogEventTypeDef",
    {
        "logStreamName": NotRequired[str],
        "timestamp": NotRequired[int],
        "message": NotRequired[str],
        "ingestionTime": NotRequired[int],
        "eventId": NotRequired[str],
    },
)

SearchedLogStreamTypeDef = TypedDict(
    "SearchedLogStreamTypeDef",
    {
        "logStreamName": NotRequired[str],
        "searchedCompletely": NotRequired[bool],
    },
)

GetDataProtectionPolicyRequestRequestTypeDef = TypedDict(
    "GetDataProtectionPolicyRequestRequestTypeDef",
    {
        "logGroupIdentifier": str,
    },
)

GetLogEventsRequestRequestTypeDef = TypedDict(
    "GetLogEventsRequestRequestTypeDef",
    {
        "logStreamName": str,
        "logGroupName": NotRequired[str],
        "logGroupIdentifier": NotRequired[str],
        "startTime": NotRequired[int],
        "endTime": NotRequired[int],
        "nextToken": NotRequired[str],
        "limit": NotRequired[int],
        "startFromHead": NotRequired[bool],
        "unmask": NotRequired[bool],
    },
)

OutputLogEventTypeDef = TypedDict(
    "OutputLogEventTypeDef",
    {
        "timestamp": NotRequired[int],
        "message": NotRequired[str],
        "ingestionTime": NotRequired[int],
    },
)

GetLogGroupFieldsRequestRequestTypeDef = TypedDict(
    "GetLogGroupFieldsRequestRequestTypeDef",
    {
        "logGroupName": NotRequired[str],
        "time": NotRequired[int],
        "logGroupIdentifier": NotRequired[str],
    },
)

LogGroupFieldTypeDef = TypedDict(
    "LogGroupFieldTypeDef",
    {
        "name": NotRequired[str],
        "percent": NotRequired[int],
    },
)

GetLogRecordRequestRequestTypeDef = TypedDict(
    "GetLogRecordRequestRequestTypeDef",
    {
        "logRecordPointer": str,
        "unmask": NotRequired[bool],
    },
)

GetQueryResultsRequestRequestTypeDef = TypedDict(
    "GetQueryResultsRequestRequestTypeDef",
    {
        "queryId": str,
    },
)

QueryStatisticsTypeDef = TypedDict(
    "QueryStatisticsTypeDef",
    {
        "recordsMatched": NotRequired[float],
        "recordsScanned": NotRequired[float],
        "bytesScanned": NotRequired[float],
    },
)

ResultFieldTypeDef = TypedDict(
    "ResultFieldTypeDef",
    {
        "field": NotRequired[str],
        "value": NotRequired[str],
    },
)

InputLogEventTypeDef = TypedDict(
    "InputLogEventTypeDef",
    {
        "timestamp": int,
        "message": str,
    },
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

ListTagsLogGroupRequestRequestTypeDef = TypedDict(
    "ListTagsLogGroupRequestRequestTypeDef",
    {
        "logGroupName": str,
    },
)

MetricFilterMatchRecordTypeDef = TypedDict(
    "MetricFilterMatchRecordTypeDef",
    {
        "eventNumber": NotRequired[int],
        "eventMessage": NotRequired[str],
        "extractedValues": NotRequired[Dict[str, str]],
    },
)

MetricTransformationTypeDef = TypedDict(
    "MetricTransformationTypeDef",
    {
        "metricName": str,
        "metricNamespace": str,
        "metricValue": str,
        "defaultValue": NotRequired[float],
        "dimensions": NotRequired[Dict[str, str]],
        "unit": NotRequired[StandardUnitType],
    },
)

PutAccountPolicyRequestRequestTypeDef = TypedDict(
    "PutAccountPolicyRequestRequestTypeDef",
    {
        "policyName": str,
        "policyDocument": str,
        "policyType": Literal["DATA_PROTECTION_POLICY"],
        "scope": NotRequired[Literal["ALL"]],
    },
)

PutDataProtectionPolicyRequestRequestTypeDef = TypedDict(
    "PutDataProtectionPolicyRequestRequestTypeDef",
    {
        "logGroupIdentifier": str,
        "policyDocument": str,
    },
)

PutDestinationPolicyRequestRequestTypeDef = TypedDict(
    "PutDestinationPolicyRequestRequestTypeDef",
    {
        "destinationName": str,
        "accessPolicy": str,
        "forceUpdate": NotRequired[bool],
    },
)

PutDestinationRequestRequestTypeDef = TypedDict(
    "PutDestinationRequestRequestTypeDef",
    {
        "destinationName": str,
        "targetArn": str,
        "roleArn": str,
        "tags": NotRequired[Mapping[str, str]],
    },
)

RejectedLogEventsInfoTypeDef = TypedDict(
    "RejectedLogEventsInfoTypeDef",
    {
        "tooNewLogEventStartIndex": NotRequired[int],
        "tooOldLogEventEndIndex": NotRequired[int],
        "expiredLogEventEndIndex": NotRequired[int],
    },
)

PutQueryDefinitionRequestRequestTypeDef = TypedDict(
    "PutQueryDefinitionRequestRequestTypeDef",
    {
        "name": str,
        "queryString": str,
        "queryDefinitionId": NotRequired[str],
        "logGroupNames": NotRequired[Sequence[str]],
        "clientToken": NotRequired[str],
    },
)

PutResourcePolicyRequestRequestTypeDef = TypedDict(
    "PutResourcePolicyRequestRequestTypeDef",
    {
        "policyName": NotRequired[str],
        "policyDocument": NotRequired[str],
    },
)

PutRetentionPolicyRequestRequestTypeDef = TypedDict(
    "PutRetentionPolicyRequestRequestTypeDef",
    {
        "logGroupName": str,
        "retentionInDays": int,
    },
)

PutSubscriptionFilterRequestRequestTypeDef = TypedDict(
    "PutSubscriptionFilterRequestRequestTypeDef",
    {
        "logGroupName": str,
        "filterName": str,
        "filterPattern": str,
        "destinationArn": str,
        "roleArn": NotRequired[str],
        "distribution": NotRequired[DistributionType],
    },
)

StartQueryRequestRequestTypeDef = TypedDict(
    "StartQueryRequestRequestTypeDef",
    {
        "startTime": int,
        "endTime": int,
        "queryString": str,
        "logGroupName": NotRequired[str],
        "logGroupNames": NotRequired[Sequence[str]],
        "logGroupIdentifiers": NotRequired[Sequence[str]],
        "limit": NotRequired[int],
    },
)

StopQueryRequestRequestTypeDef = TypedDict(
    "StopQueryRequestRequestTypeDef",
    {
        "queryId": str,
    },
)

TagLogGroupRequestRequestTypeDef = TypedDict(
    "TagLogGroupRequestRequestTypeDef",
    {
        "logGroupName": str,
        "tags": Mapping[str, str],
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)

TestMetricFilterRequestRequestTypeDef = TypedDict(
    "TestMetricFilterRequestRequestTypeDef",
    {
        "filterPattern": str,
        "logEventMessages": Sequence[str],
    },
)

UntagLogGroupRequestRequestTypeDef = TypedDict(
    "UntagLogGroupRequestRequestTypeDef",
    {
        "logGroupName": str,
        "tags": Sequence[str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

CreateExportTaskResponseTypeDef = TypedDict(
    "CreateExportTaskResponseTypeDef",
    {
        "taskId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteQueryDefinitionResponseTypeDef = TypedDict(
    "DeleteQueryDefinitionResponseTypeDef",
    {
        "success": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeAccountPoliciesResponseTypeDef = TypedDict(
    "DescribeAccountPoliciesResponseTypeDef",
    {
        "accountPolicies": List[AccountPolicyTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetDataProtectionPolicyResponseTypeDef = TypedDict(
    "GetDataProtectionPolicyResponseTypeDef",
    {
        "logGroupIdentifier": str,
        "policyDocument": str,
        "lastUpdatedTime": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetLogRecordResponseTypeDef = TypedDict(
    "GetLogRecordResponseTypeDef",
    {
        "logRecord": Dict[str, str],
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

ListTagsLogGroupResponseTypeDef = TypedDict(
    "ListTagsLogGroupResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutAccountPolicyResponseTypeDef = TypedDict(
    "PutAccountPolicyResponseTypeDef",
    {
        "accountPolicy": AccountPolicyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutDataProtectionPolicyResponseTypeDef = TypedDict(
    "PutDataProtectionPolicyResponseTypeDef",
    {
        "logGroupIdentifier": str,
        "policyDocument": str,
        "lastUpdatedTime": int,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutQueryDefinitionResponseTypeDef = TypedDict(
    "PutQueryDefinitionResponseTypeDef",
    {
        "queryDefinitionId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartQueryResponseTypeDef = TypedDict(
    "StartQueryResponseTypeDef",
    {
        "queryId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StopQueryResponseTypeDef = TypedDict(
    "StopQueryResponseTypeDef",
    {
        "success": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDestinationsRequestDescribeDestinationsPaginateTypeDef = TypedDict(
    "DescribeDestinationsRequestDescribeDestinationsPaginateTypeDef",
    {
        "DestinationNamePrefix": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

DescribeExportTasksRequestDescribeExportTasksPaginateTypeDef = TypedDict(
    "DescribeExportTasksRequestDescribeExportTasksPaginateTypeDef",
    {
        "taskId": NotRequired[str],
        "statusCode": NotRequired[ExportTaskStatusCodeType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

DescribeLogGroupsRequestDescribeLogGroupsPaginateTypeDef = TypedDict(
    "DescribeLogGroupsRequestDescribeLogGroupsPaginateTypeDef",
    {
        "accountIdentifiers": NotRequired[Sequence[str]],
        "logGroupNamePrefix": NotRequired[str],
        "logGroupNamePattern": NotRequired[str],
        "includeLinkedAccounts": NotRequired[bool],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

DescribeLogStreamsRequestDescribeLogStreamsPaginateTypeDef = TypedDict(
    "DescribeLogStreamsRequestDescribeLogStreamsPaginateTypeDef",
    {
        "logGroupName": NotRequired[str],
        "logGroupIdentifier": NotRequired[str],
        "logStreamNamePrefix": NotRequired[str],
        "orderBy": NotRequired[OrderByType],
        "descending": NotRequired[bool],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

DescribeMetricFiltersRequestDescribeMetricFiltersPaginateTypeDef = TypedDict(
    "DescribeMetricFiltersRequestDescribeMetricFiltersPaginateTypeDef",
    {
        "logGroupName": NotRequired[str],
        "filterNamePrefix": NotRequired[str],
        "metricName": NotRequired[str],
        "metricNamespace": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

DescribeQueriesRequestDescribeQueriesPaginateTypeDef = TypedDict(
    "DescribeQueriesRequestDescribeQueriesPaginateTypeDef",
    {
        "logGroupName": NotRequired[str],
        "status": NotRequired[QueryStatusType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

DescribeResourcePoliciesRequestDescribeResourcePoliciesPaginateTypeDef = TypedDict(
    "DescribeResourcePoliciesRequestDescribeResourcePoliciesPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

DescribeSubscriptionFiltersRequestDescribeSubscriptionFiltersPaginateTypeDef = TypedDict(
    "DescribeSubscriptionFiltersRequestDescribeSubscriptionFiltersPaginateTypeDef",
    {
        "logGroupName": str,
        "filterNamePrefix": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

FilterLogEventsRequestFilterLogEventsPaginateTypeDef = TypedDict(
    "FilterLogEventsRequestFilterLogEventsPaginateTypeDef",
    {
        "logGroupName": NotRequired[str],
        "logGroupIdentifier": NotRequired[str],
        "logStreamNames": NotRequired[Sequence[str]],
        "logStreamNamePrefix": NotRequired[str],
        "startTime": NotRequired[int],
        "endTime": NotRequired[int],
        "filterPattern": NotRequired[str],
        "interleaved": NotRequired[bool],
        "unmask": NotRequired[bool],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

DescribeDestinationsResponseTypeDef = TypedDict(
    "DescribeDestinationsResponseTypeDef",
    {
        "destinations": List[DestinationTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutDestinationResponseTypeDef = TypedDict(
    "PutDestinationResponseTypeDef",
    {
        "destination": DestinationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeLogGroupsResponseTypeDef = TypedDict(
    "DescribeLogGroupsResponseTypeDef",
    {
        "logGroups": List[LogGroupTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeLogStreamsResponseTypeDef = TypedDict(
    "DescribeLogStreamsResponseTypeDef",
    {
        "logStreams": List[LogStreamTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeQueriesResponseTypeDef = TypedDict(
    "DescribeQueriesResponseTypeDef",
    {
        "queries": List[QueryInfoTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeQueryDefinitionsResponseTypeDef = TypedDict(
    "DescribeQueryDefinitionsResponseTypeDef",
    {
        "queryDefinitions": List[QueryDefinitionTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeResourcePoliciesResponseTypeDef = TypedDict(
    "DescribeResourcePoliciesResponseTypeDef",
    {
        "resourcePolicies": List[ResourcePolicyTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutResourcePolicyResponseTypeDef = TypedDict(
    "PutResourcePolicyResponseTypeDef",
    {
        "resourcePolicy": ResourcePolicyTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeSubscriptionFiltersResponseTypeDef = TypedDict(
    "DescribeSubscriptionFiltersResponseTypeDef",
    {
        "subscriptionFilters": List[SubscriptionFilterTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ExportTaskTypeDef = TypedDict(
    "ExportTaskTypeDef",
    {
        "taskId": NotRequired[str],
        "taskName": NotRequired[str],
        "logGroupName": NotRequired[str],
        "from": NotRequired[int],
        "to": NotRequired[int],
        "destination": NotRequired[str],
        "destinationPrefix": NotRequired[str],
        "status": NotRequired[ExportTaskStatusTypeDef],
        "executionInfo": NotRequired[ExportTaskExecutionInfoTypeDef],
    },
)

FilterLogEventsResponseTypeDef = TypedDict(
    "FilterLogEventsResponseTypeDef",
    {
        "events": List[FilteredLogEventTypeDef],
        "searchedLogStreams": List[SearchedLogStreamTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetLogEventsResponseTypeDef = TypedDict(
    "GetLogEventsResponseTypeDef",
    {
        "events": List[OutputLogEventTypeDef],
        "nextForwardToken": str,
        "nextBackwardToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetLogGroupFieldsResponseTypeDef = TypedDict(
    "GetLogGroupFieldsResponseTypeDef",
    {
        "logGroupFields": List[LogGroupFieldTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetQueryResultsResponseTypeDef = TypedDict(
    "GetQueryResultsResponseTypeDef",
    {
        "results": List[List[ResultFieldTypeDef]],
        "statistics": QueryStatisticsTypeDef,
        "status": QueryStatusType,
        "encryptionKey": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

PutLogEventsRequestRequestTypeDef = TypedDict(
    "PutLogEventsRequestRequestTypeDef",
    {
        "logGroupName": str,
        "logStreamName": str,
        "logEvents": Sequence[InputLogEventTypeDef],
        "sequenceToken": NotRequired[str],
    },
)

TestMetricFilterResponseTypeDef = TypedDict(
    "TestMetricFilterResponseTypeDef",
    {
        "matches": List[MetricFilterMatchRecordTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

MetricFilterTypeDef = TypedDict(
    "MetricFilterTypeDef",
    {
        "filterName": NotRequired[str],
        "filterPattern": NotRequired[str],
        "metricTransformations": NotRequired[List[MetricTransformationTypeDef]],
        "creationTime": NotRequired[int],
        "logGroupName": NotRequired[str],
    },
)

PutMetricFilterRequestRequestTypeDef = TypedDict(
    "PutMetricFilterRequestRequestTypeDef",
    {
        "logGroupName": str,
        "filterName": str,
        "filterPattern": str,
        "metricTransformations": Sequence[MetricTransformationTypeDef],
    },
)

PutLogEventsResponseTypeDef = TypedDict(
    "PutLogEventsResponseTypeDef",
    {
        "nextSequenceToken": str,
        "rejectedLogEventsInfo": RejectedLogEventsInfoTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeExportTasksResponseTypeDef = TypedDict(
    "DescribeExportTasksResponseTypeDef",
    {
        "exportTasks": List[ExportTaskTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeMetricFiltersResponseTypeDef = TypedDict(
    "DescribeMetricFiltersResponseTypeDef",
    {
        "metricFilters": List[MetricFilterTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
