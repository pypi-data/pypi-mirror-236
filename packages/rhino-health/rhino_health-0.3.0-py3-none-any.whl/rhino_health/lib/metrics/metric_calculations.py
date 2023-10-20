"""
@autoapi False
"""
from collections import OrderedDict
from itertools import chain
from typing import Callable, List, TypedDict

from rhino_health.lib.metrics.aggregatable_metric import AggregatableMetric, CountBasedMetric
from rhino_health.lib.metrics.aggregate_metrics.aggregation_service import (
    calculate_aggregate_metric,
)
from rhino_health.lib.metrics.base_metric import MetricResponse, TwoByTwoTableMetricResponse


class MetricCalculation:
    # TODO: Split up this file
    @staticmethod
    def get_basic_metric(
        session,
        cohort_uids: List[str],
        data_cache: dict,
        metric_configuration: AggregatableMetric,
        **kwargs,
    ):
        """
        Fetches the basic metric from each cohort, aggregates the results according to the aggregation type
        configured in the metric configuration, and stores the result in the data cache.
        """
        if isinstance(metric_configuration, CountBasedMetric):
            basic_metric_configuration = metric_configuration.get_count_configuration()
        else:
            basic_metric_configuration = metric_configuration
        fetcher = basic_metric_configuration.fetcher
        fetched_metrics = fetcher.fetch_metrics(session, cohort_uids, basic_metric_configuration)
        aggregated_metrics = calculate_aggregate_metric(
            basic_metric_configuration, [r.output for r in fetched_metrics]
        )
        aggregated_metrics = MetricCalculation._groupings_handler(
            aggregated_metrics, metric_configuration
        )
        data_cache["result"] = metric_configuration.metric_response(output=aggregated_metrics)

    @staticmethod
    def _groupings_handler(aggregated_metrics, metric_configuration):
        """
        Handles the groupings for the metric calculation.
        As many metrics are based on the count metric that is calculated using internal groupings,
        handle the user inserted groupings here.
        """
        if hasattr(metric_configuration, "user_groupings"):
            user_groupings = metric_configuration.user_groupings
            if user_groupings:
                # if the metric contains groupings, we want to distinguish those from the inner calculations groupings
                return MetricCalculation._extract_groupings(aggregated_metrics, user_groupings)
        return aggregated_metrics

    @staticmethod
    def calculate_two_by_two_table(data_cache: dict, metric_configuration, **kwargs):
        """
        As the two by two table is equivalent to the (inner grouped) count metric, just return the count metric results under
         the two_by_two metric name.
        """
        if metric_configuration.group_by:
            data_cache["result"] = metric_configuration.metric_response(
                output={
                    group: {"two_by_two_table": v}
                    for group, v in data_cache["result"].output.items()
                }
            )
        else:
            data_cache["result"] = metric_configuration.metric_response(
                output={"two_by_two_table": data_cache["result"].output}
            )

    @staticmethod
    def calculate_odds_ratio(data_cache: dict, metric_configuration, **kwargs):
        def _calculate_odds_ratio(table):
            # Ger the table as an ordered dict representing the actual table in a 2X2 table format
            table_as_dict = TwoByTwoTableMetricResponse.get_ordered_dict_table(table)
            return (
                MetricCalculation._get_item_in_table_dict(0, 0, table_as_dict)
                * MetricCalculation._get_item_in_table_dict(1, 1, table_as_dict)
                / (
                    MetricCalculation._get_item_in_table_dict(0, 1, table_as_dict)
                    * MetricCalculation._get_item_in_table_dict(1, 0, table_as_dict)
                )
            )

        try:
            data_cache["result"] = metric_configuration.metric_response(
                output=MetricCalculation._calculate_per_group(
                    metric_configuration, data_cache, _calculate_odds_ratio
                )
            )
        except IndexError:
            raise ValueError(
                "Can not calculate odds ratio as either the expected data or exposed data has less"
                " than 2 categories"
            )

    @staticmethod
    def calculate_odds(data_cache: dict, metric_configuration, **kwargs):
        def _calculate_odds(count_dict):
            total_positive_cases = count_dict.get("True").get("count")
            total_negative_cases = count_dict.get("False").get("count")
            return total_positive_cases / total_negative_cases

        data_cache["result"] = metric_configuration.metric_response(
            output={
                metric_configuration.metric_name(): MetricCalculation._calculate_per_group(
                    metric_configuration, data_cache, _calculate_odds
                )
            }
        )

    @staticmethod
    def calculate_risk(data_cache: dict, metric_configuration, **kwargs):
        def _calculate_r_plus(table):
            table_as_dict = TwoByTwoTableMetricResponse.get_ordered_dict_table(table)
            return MetricCalculation._get_item_in_table_dict(0, 0, table_as_dict) / (
                MetricCalculation._get_item_in_table_dict(0, 0, table_as_dict)
                + MetricCalculation._get_item_in_table_dict(0, 1, table_as_dict)
            )

        def _calculate_r_minus(table):
            table_as_dict = TwoByTwoTableMetricResponse.get_ordered_dict_table(table)
            return MetricCalculation._get_item_in_table_dict(1, 0, table_as_dict) / (
                MetricCalculation._get_item_in_table_dict(1, 0, table_as_dict)
                + MetricCalculation._get_item_in_table_dict(1, 1, table_as_dict)
            )

        try:
            r_plus = MetricCalculation._calculate_per_group(
                metric_configuration, data_cache, _calculate_r_plus, "r_plus"
            )
            r_minus = MetricCalculation._calculate_per_group(
                metric_configuration, data_cache, _calculate_r_minus, "r_minus"
            )

            if metric_configuration.group_by:
                # as this metric returns two values, need to mind the groupings again
                output = {k: {**r_plus[k], **r_minus[k]} for k in r_plus.keys()}
            else:
                output = {**r_plus, **r_minus}
            data_cache["result"] = metric_configuration.metric_response(output=output)

        except IndexError:
            raise ValueError(
                "Can not calculate risk as either the expected data or exposed data has less"
                " than 2 categories"
            )

    @staticmethod
    def calculate_risk_ratio(data_cache: dict, metric_configuration, **kwargs):
        if metric_configuration.group_by:
            risk_ratio_results = {
                group: {metric_configuration.metric_name(): v["r_plus"] / v["r_minus"]}
                for group, v in data_cache["result"].output.items()
            }
        else:
            risk_ratio_results = {
                metric_configuration.metric_name(): data_cache["result"].output["r_plus"]
                / data_cache["result"].output["r_minus"]
            }
        data_cache["result"] = metric_configuration.metric_response(output=risk_ratio_results)

    @staticmethod
    def calculate_positive_ratio(data_cache: dict, metric_configuration, **kwargs):
        def _calculate_positive_ratio(data):
            return data.get("True").get("count") / (
                data.get("True").get("count") + data.get("False").get("count")
            )

        data_cache["result"] = metric_configuration.metric_response(
            output=MetricCalculation._calculate_per_group(
                metric_configuration, data_cache, _calculate_positive_ratio
            )
        )

    @staticmethod
    def _extract_groupings(aggregated_metrics: dict, groupings, base_metric="count"):
        """
        Extracts the user inserted groupings from the aggregated metrics and returns a new dict with those groupings as keys.
        """

        def str_tuple(t):
            return str(t[0]) if len(t) == 1 else str(t)

        grouped_results = {}
        # Currently the groups list contains the initial groupings that are user for the basic metric calculation as
        # well as the groupings that were set by the user. We want to get only the groupings that were set by the user,
        # hence we take the len(groupings) last items from each item (group) in the groupings list.
        for key, value in aggregated_metrics.items():
            basic_groups = eval(key)[: -len(groupings)]
            user_groups = eval(key)[-len(groupings) :]
            grouped_results.setdefault(str_tuple(user_groups), {})[str_tuple(basic_groups)] = value
        return grouped_results

    @staticmethod
    def _calculate_per_group(metric_configuration, data_cache, calc_func, metric_name=None):
        metric_name = metric_name or metric_configuration.metric_name()
        if metric_configuration.group_by:
            results = {}
            for group in data_cache["result"].output:
                results[group] = {metric_name: calc_func(data_cache["result"].output[group])}
        else:
            results = {metric_name: calc_func(data_cache["result"].output)}
        return results

    @staticmethod
    def _get_item_in_table_dict(row, col, table):
        # As we store the table data in an ordered dict representing the actual table,
        # extract the values according to their position in the table
        return list(list(table.items())[row][1].items())[col][1]

    @staticmethod
    def _rotate_dict(input_dict):
        output_dict = {}
        for outer_key, inner_dict in input_dict.items():
            for inner_key, value in inner_dict.items():
                if inner_key not in output_dict:
                    output_dict[inner_key] = {}
                output_dict[inner_key][outer_key] = value
        return output_dict


class CalculationSteps(TypedDict):
    Steps: List[Callable]


class MetricCalculationStepsMapping(TypedDict):
    metric: CalculationSteps


METRIC_CALCULATION_STEPS_MAPPING: MetricCalculationStepsMapping = {
    "default": {"Steps": [MetricCalculation.get_basic_metric]},
    "two_by_two_table": {
        "Steps": [MetricCalculation.get_basic_metric, MetricCalculation.calculate_two_by_two_table],
    },
    "odds_ratio": {
        "Steps": [MetricCalculation.get_basic_metric, MetricCalculation.calculate_odds_ratio],
    },
    "odds": {
        "Steps": [MetricCalculation.get_basic_metric, MetricCalculation.calculate_odds],
    },
    "risk": {
        "Steps": [MetricCalculation.get_basic_metric, MetricCalculation.calculate_risk],
    },
    "risk_ratio": {
        "Steps": [
            MetricCalculation.get_basic_metric,
            MetricCalculation.calculate_risk,
            MetricCalculation.calculate_risk_ratio,
        ],
    },
    "prevalence": {
        "Steps": [MetricCalculation.get_basic_metric, MetricCalculation.calculate_positive_ratio],
    },
    "incidence": {
        "Steps": [MetricCalculation.get_basic_metric, MetricCalculation.calculate_positive_ratio],
    },
}
