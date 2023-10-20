import json
from itertools import chain
from typing import TYPE_CHECKING, Callable, List, Optional

from funcy import compact

from rhino_health.lib.metrics.aggregatable_metric import AggregatableMetric

if TYPE_CHECKING:
    from rhino_health.lib.rhino_session import RhinoSession

from rhino_health.lib.metrics.base_metric import BaseMetric, MetricResponse, MetricResultDataType


def calculate_aggregate_metric(
    metric_configuration: BaseMetric,
    metric_results: List[MetricResultDataType],
    aggregation_method_override: Optional[Callable] = None,
) -> MetricResultDataType:
    """
    Aggregates the results from the individual cohorts into one. # TODO: maybe move to metric calculation
    """
    if not isinstance(metric_configuration, AggregatableMetric):
        raise ValueError("Unsupported metric for aggregation")
    metric = metric_configuration.metric_name()
    aggregation_method = aggregation_method_override or metric_configuration.aggregation_method
    count_variable = metric_configuration.count_variable_name
    if metric_configuration.group_by is None:
        return aggregation_method(metric, metric_results, count_variable=count_variable)
    else:
        # We get the unique group names from the data to iterate over since not all sites have all groups
        groups = set(chain.from_iterable(metric_result.keys() for metric_result in metric_results))
        grouped_results = {}
        for group in groups:
            group_result = compact(
                [metric_result.get(group, None) for metric_result in metric_results]
            )
            grouped_results[group] = aggregation_method(
                metric, group_result, count_variable=count_variable
            )
        return grouped_results


def get_cloud_aggregated_metric_data(
    session: "RhinoSession",
    cohort_uids: List[str],
    metric_configuration: BaseMetric,
) -> MetricResponse:
    metric_configuration_dict = metric_configuration.data()
    timeout_seconds = metric_configuration_dict.pop("timeout_seconds", None)

    metric_response = session.post(
        f"/projects/calculate_aggregate_metric/",
        data={
            "cohort_uids": cohort_uids,
            "metric_configuration": json.dumps(metric_configuration_dict),
            "timeout_seconds": timeout_seconds,
        },
    )
    parsed_response = metric_response.raw_response.json()
    response_status = parsed_response.pop("status")
    response_data = parsed_response.pop("data", None)
    response_output = parsed_response.pop("output", None)
    if parsed_response:
        raise ValueError(f"Unexpected fields in response: {', '.join(parsed_response.keys())}")
    return metric_configuration.metric_response(
        status=response_status,
        data=response_data,
        output=response_output,
        metric_configuration_dict=metric_configuration_dict,
    )
