"""
Type annotations for logs service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_logs.client import CloudWatchLogsClient

    session = get_session()
    async with session.create_client("logs") as client:
        client: CloudWatchLogsClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import DistributionType, ExportTaskStatusCodeType, OrderByType, QueryStatusType
from .paginator import (
    DescribeDestinationsPaginator,
    DescribeExportTasksPaginator,
    DescribeLogGroupsPaginator,
    DescribeLogStreamsPaginator,
    DescribeMetricFiltersPaginator,
    DescribeQueriesPaginator,
    DescribeResourcePoliciesPaginator,
    DescribeSubscriptionFiltersPaginator,
    FilterLogEventsPaginator,
)
from .type_defs import (
    CreateExportTaskResponseTypeDef,
    DeleteQueryDefinitionResponseTypeDef,
    DescribeAccountPoliciesResponseTypeDef,
    DescribeDestinationsResponseTypeDef,
    DescribeExportTasksResponseTypeDef,
    DescribeLogGroupsResponseTypeDef,
    DescribeLogStreamsResponseTypeDef,
    DescribeMetricFiltersResponseTypeDef,
    DescribeQueriesResponseTypeDef,
    DescribeQueryDefinitionsResponseTypeDef,
    DescribeResourcePoliciesResponseTypeDef,
    DescribeSubscriptionFiltersResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    FilterLogEventsResponseTypeDef,
    GetDataProtectionPolicyResponseTypeDef,
    GetLogEventsResponseTypeDef,
    GetLogGroupFieldsResponseTypeDef,
    GetLogRecordResponseTypeDef,
    GetQueryResultsResponseTypeDef,
    InputLogEventTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTagsLogGroupResponseTypeDef,
    MetricTransformationTypeDef,
    PutAccountPolicyResponseTypeDef,
    PutDataProtectionPolicyResponseTypeDef,
    PutDestinationResponseTypeDef,
    PutLogEventsResponseTypeDef,
    PutQueryDefinitionResponseTypeDef,
    PutResourcePolicyResponseTypeDef,
    StartQueryResponseTypeDef,
    StopQueryResponseTypeDef,
    TestMetricFilterResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("CloudWatchLogsClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    DataAlreadyAcceptedException: Type[BotocoreClientError]
    InvalidOperationException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    InvalidSequenceTokenException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    MalformedQueryException: Type[BotocoreClientError]
    OperationAbortedException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    UnrecognizedClientException: Type[BotocoreClientError]

class CloudWatchLogsClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CloudWatchLogsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#exceptions)
        """

    async def associate_kms_key(
        self, *, kmsKeyId: str, logGroupName: str = ..., resourceIdentifier: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Associates the specified KMS key with either one log group in the account, or
        with all stored CloudWatch Logs query insights results in the
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.associate_kms_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#associate_kms_key)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#can_paginate)
        """

    async def cancel_export_task(self, *, taskId: str) -> EmptyResponseMetadataTypeDef:
        """
        Cancels the specified export task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.cancel_export_task)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#cancel_export_task)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#close)
        """

    async def create_export_task(
        self,
        *,
        logGroupName: str,
        fromTime: int,
        to: int,
        destination: str,
        taskName: str = ...,
        logStreamNamePrefix: str = ...,
        destinationPrefix: str = ...
    ) -> CreateExportTaskResponseTypeDef:
        """
        Creates an export task so that you can efficiently export data from a log group
        to an Amazon S3
        bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.create_export_task)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#create_export_task)
        """

    async def create_log_group(
        self, *, logGroupName: str, kmsKeyId: str = ..., tags: Mapping[str, str] = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates a log group with the specified name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.create_log_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#create_log_group)
        """

    async def create_log_stream(
        self, *, logGroupName: str, logStreamName: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates a log stream for the specified log group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.create_log_stream)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#create_log_stream)
        """

    async def delete_account_policy(
        self, *, policyName: str, policyType: Literal["DATA_PROTECTION_POLICY"]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a CloudWatch Logs account policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.delete_account_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#delete_account_policy)
        """

    async def delete_data_protection_policy(
        self, *, logGroupIdentifier: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the data protection policy from the specified log group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.delete_data_protection_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#delete_data_protection_policy)
        """

    async def delete_destination(self, *, destinationName: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified destination, and eventually disables all the subscription
        filters that publish to
        it.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.delete_destination)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#delete_destination)
        """

    async def delete_log_group(self, *, logGroupName: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified log group and permanently deletes all the archived log
        events associated with the log
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.delete_log_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#delete_log_group)
        """

    async def delete_log_stream(
        self, *, logGroupName: str, logStreamName: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified log stream and permanently deletes all the archived log
        events associated with the log
        stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.delete_log_stream)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#delete_log_stream)
        """

    async def delete_metric_filter(
        self, *, logGroupName: str, filterName: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified metric filter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.delete_metric_filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#delete_metric_filter)
        """

    async def delete_query_definition(
        self, *, queryDefinitionId: str
    ) -> DeleteQueryDefinitionResponseTypeDef:
        """
        Deletes a saved CloudWatch Logs Insights query definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.delete_query_definition)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#delete_query_definition)
        """

    async def delete_resource_policy(
        self, *, policyName: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a resource policy from this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.delete_resource_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#delete_resource_policy)
        """

    async def delete_retention_policy(self, *, logGroupName: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified retention policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.delete_retention_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#delete_retention_policy)
        """

    async def delete_subscription_filter(
        self, *, logGroupName: str, filterName: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified subscription filter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.delete_subscription_filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#delete_subscription_filter)
        """

    async def describe_account_policies(
        self,
        *,
        policyType: Literal["DATA_PROTECTION_POLICY"],
        policyName: str = ...,
        accountIdentifiers: Sequence[str] = ...
    ) -> DescribeAccountPoliciesResponseTypeDef:
        """
        Returns a list of all CloudWatch Logs account policies in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.describe_account_policies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#describe_account_policies)
        """

    async def describe_destinations(
        self, *, DestinationNamePrefix: str = ..., nextToken: str = ..., limit: int = ...
    ) -> DescribeDestinationsResponseTypeDef:
        """
        Lists all your destinations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.describe_destinations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#describe_destinations)
        """

    async def describe_export_tasks(
        self,
        *,
        taskId: str = ...,
        statusCode: ExportTaskStatusCodeType = ...,
        nextToken: str = ...,
        limit: int = ...
    ) -> DescribeExportTasksResponseTypeDef:
        """
        Lists the specified export tasks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.describe_export_tasks)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#describe_export_tasks)
        """

    async def describe_log_groups(
        self,
        *,
        accountIdentifiers: Sequence[str] = ...,
        logGroupNamePrefix: str = ...,
        logGroupNamePattern: str = ...,
        nextToken: str = ...,
        limit: int = ...,
        includeLinkedAccounts: bool = ...
    ) -> DescribeLogGroupsResponseTypeDef:
        """
        Lists the specified log groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.describe_log_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#describe_log_groups)
        """

    async def describe_log_streams(
        self,
        *,
        logGroupName: str = ...,
        logGroupIdentifier: str = ...,
        logStreamNamePrefix: str = ...,
        orderBy: OrderByType = ...,
        descending: bool = ...,
        nextToken: str = ...,
        limit: int = ...
    ) -> DescribeLogStreamsResponseTypeDef:
        """
        Lists the log streams for the specified log group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.describe_log_streams)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#describe_log_streams)
        """

    async def describe_metric_filters(
        self,
        *,
        logGroupName: str = ...,
        filterNamePrefix: str = ...,
        nextToken: str = ...,
        limit: int = ...,
        metricName: str = ...,
        metricNamespace: str = ...
    ) -> DescribeMetricFiltersResponseTypeDef:
        """
        Lists the specified metric filters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.describe_metric_filters)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#describe_metric_filters)
        """

    async def describe_queries(
        self,
        *,
        logGroupName: str = ...,
        status: QueryStatusType = ...,
        maxResults: int = ...,
        nextToken: str = ...
    ) -> DescribeQueriesResponseTypeDef:
        """
        Returns a list of CloudWatch Logs Insights queries that are scheduled, running,
        or have been run recently in this
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.describe_queries)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#describe_queries)
        """

    async def describe_query_definitions(
        self, *, queryDefinitionNamePrefix: str = ..., maxResults: int = ..., nextToken: str = ...
    ) -> DescribeQueryDefinitionsResponseTypeDef:
        """
        This operation returns a paginated list of your saved CloudWatch Logs Insights
        query
        definitions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.describe_query_definitions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#describe_query_definitions)
        """

    async def describe_resource_policies(
        self, *, nextToken: str = ..., limit: int = ...
    ) -> DescribeResourcePoliciesResponseTypeDef:
        """
        Lists the resource policies in this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.describe_resource_policies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#describe_resource_policies)
        """

    async def describe_subscription_filters(
        self,
        *,
        logGroupName: str,
        filterNamePrefix: str = ...,
        nextToken: str = ...,
        limit: int = ...
    ) -> DescribeSubscriptionFiltersResponseTypeDef:
        """
        Lists the subscription filters for the specified log group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.describe_subscription_filters)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#describe_subscription_filters)
        """

    async def disassociate_kms_key(
        self, *, logGroupName: str = ..., resourceIdentifier: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Disassociates the specified KMS key from the specified log group or from all
        CloudWatch Logs Insights query results in the
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.disassociate_kms_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#disassociate_kms_key)
        """

    async def filter_log_events(
        self,
        *,
        logGroupName: str = ...,
        logGroupIdentifier: str = ...,
        logStreamNames: Sequence[str] = ...,
        logStreamNamePrefix: str = ...,
        startTime: int = ...,
        endTime: int = ...,
        filterPattern: str = ...,
        nextToken: str = ...,
        limit: int = ...,
        interleaved: bool = ...,
        unmask: bool = ...
    ) -> FilterLogEventsResponseTypeDef:
        """
        Lists log events from the specified log group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.filter_log_events)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#filter_log_events)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#generate_presigned_url)
        """

    async def get_data_protection_policy(
        self, *, logGroupIdentifier: str
    ) -> GetDataProtectionPolicyResponseTypeDef:
        """
        Returns information about a log group data protection policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.get_data_protection_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#get_data_protection_policy)
        """

    async def get_log_events(
        self,
        *,
        logStreamName: str,
        logGroupName: str = ...,
        logGroupIdentifier: str = ...,
        startTime: int = ...,
        endTime: int = ...,
        nextToken: str = ...,
        limit: int = ...,
        startFromHead: bool = ...,
        unmask: bool = ...
    ) -> GetLogEventsResponseTypeDef:
        """
        Lists log events from the specified log stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.get_log_events)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#get_log_events)
        """

    async def get_log_group_fields(
        self, *, logGroupName: str = ..., time: int = ..., logGroupIdentifier: str = ...
    ) -> GetLogGroupFieldsResponseTypeDef:
        """
        Returns a list of the fields that are included in log events in the specified
        log
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.get_log_group_fields)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#get_log_group_fields)
        """

    async def get_log_record(
        self, *, logRecordPointer: str, unmask: bool = ...
    ) -> GetLogRecordResponseTypeDef:
        """
        Retrieves all of the fields and values of a single log event.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.get_log_record)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#get_log_record)
        """

    async def get_query_results(self, *, queryId: str) -> GetQueryResultsResponseTypeDef:
        """
        Returns the results from the specified query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.get_query_results)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#get_query_results)
        """

    async def list_tags_for_resource(
        self, *, resourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Displays the tags associated with a CloudWatch Logs resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#list_tags_for_resource)
        """

    async def list_tags_log_group(self, *, logGroupName: str) -> ListTagsLogGroupResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.list_tags_log_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#list_tags_log_group)
        """

    async def put_account_policy(
        self,
        *,
        policyName: str,
        policyDocument: str,
        policyType: Literal["DATA_PROTECTION_POLICY"],
        scope: Literal["ALL"] = ...
    ) -> PutAccountPolicyResponseTypeDef:
        """
        Creates an account-level data protection policy that applies to all log groups
        in the
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.put_account_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#put_account_policy)
        """

    async def put_data_protection_policy(
        self, *, logGroupIdentifier: str, policyDocument: str
    ) -> PutDataProtectionPolicyResponseTypeDef:
        """
        Creates a data protection policy for the specified log group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.put_data_protection_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#put_data_protection_policy)
        """

    async def put_destination(
        self, *, destinationName: str, targetArn: str, roleArn: str, tags: Mapping[str, str] = ...
    ) -> PutDestinationResponseTypeDef:
        """
        Creates or updates a destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.put_destination)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#put_destination)
        """

    async def put_destination_policy(
        self, *, destinationName: str, accessPolicy: str, forceUpdate: bool = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates or updates an access policy associated with an existing destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.put_destination_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#put_destination_policy)
        """

    async def put_log_events(
        self,
        *,
        logGroupName: str,
        logStreamName: str,
        logEvents: Sequence[InputLogEventTypeDef],
        sequenceToken: str = ...
    ) -> PutLogEventsResponseTypeDef:
        """
        Uploads a batch of log events to the specified log stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.put_log_events)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#put_log_events)
        """

    async def put_metric_filter(
        self,
        *,
        logGroupName: str,
        filterName: str,
        filterPattern: str,
        metricTransformations: Sequence[MetricTransformationTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates or updates a metric filter and associates it with the specified log
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.put_metric_filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#put_metric_filter)
        """

    async def put_query_definition(
        self,
        *,
        name: str,
        queryString: str,
        queryDefinitionId: str = ...,
        logGroupNames: Sequence[str] = ...,
        clientToken: str = ...
    ) -> PutQueryDefinitionResponseTypeDef:
        """
        Creates or updates a query definition for CloudWatch Logs Insights.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.put_query_definition)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#put_query_definition)
        """

    async def put_resource_policy(
        self, *, policyName: str = ..., policyDocument: str = ...
    ) -> PutResourcePolicyResponseTypeDef:
        """
        Creates or updates a resource policy allowing other Amazon Web Services
        services to put log events to this account, such as Amazon Route
        53.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.put_resource_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#put_resource_policy)
        """

    async def put_retention_policy(
        self, *, logGroupName: str, retentionInDays: int
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets the retention of the specified log group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.put_retention_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#put_retention_policy)
        """

    async def put_subscription_filter(
        self,
        *,
        logGroupName: str,
        filterName: str,
        filterPattern: str,
        destinationArn: str,
        roleArn: str = ...,
        distribution: DistributionType = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates or updates a subscription filter and associates it with the specified
        log
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.put_subscription_filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#put_subscription_filter)
        """

    async def start_query(
        self,
        *,
        startTime: int,
        endTime: int,
        queryString: str,
        logGroupName: str = ...,
        logGroupNames: Sequence[str] = ...,
        logGroupIdentifiers: Sequence[str] = ...,
        limit: int = ...
    ) -> StartQueryResponseTypeDef:
        """
        Schedules a query of a log group using CloudWatch Logs Insights.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.start_query)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#start_query)
        """

    async def stop_query(self, *, queryId: str) -> StopQueryResponseTypeDef:
        """
        Stops a CloudWatch Logs Insights query that is in progress.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.stop_query)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#stop_query)
        """

    async def tag_log_group(
        self, *, logGroupName: str, tags: Mapping[str, str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.tag_log_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#tag_log_group)
        """

    async def tag_resource(
        self, *, resourceArn: str, tags: Mapping[str, str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Assigns one or more tags (key-value pairs) to the specified CloudWatch Logs
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#tag_resource)
        """

    async def test_metric_filter(
        self, *, filterPattern: str, logEventMessages: Sequence[str]
    ) -> TestMetricFilterResponseTypeDef:
        """
        Tests the filter pattern of a metric filter against a sample of log event
        messages.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.test_metric_filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#test_metric_filter)
        """

    async def untag_log_group(
        self, *, logGroupName: str, tags: Sequence[str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.untag_log_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#untag_log_group)
        """

    async def untag_resource(
        self, *, resourceArn: str, tagKeys: Sequence[str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes one or more tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#untag_resource)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_destinations"]
    ) -> DescribeDestinationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_export_tasks"]
    ) -> DescribeExportTasksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_log_groups"]
    ) -> DescribeLogGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_log_streams"]
    ) -> DescribeLogStreamsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_metric_filters"]
    ) -> DescribeMetricFiltersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_queries"]
    ) -> DescribeQueriesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_resource_policies"]
    ) -> DescribeResourcePoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_subscription_filters"]
    ) -> DescribeSubscriptionFiltersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["filter_log_events"]
    ) -> FilterLogEventsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/#get_paginator)
        """

    async def __aenter__(self) -> "CloudWatchLogsClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html#CloudWatchLogs.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_logs/client/)
        """
