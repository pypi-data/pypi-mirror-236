from abc import ABC
from typing import Callable, Optional

from rhino_health.lib.metrics.aggregate_metrics.aggregation_data_fetchers import (
    DefaultMetricFetcher,
)
from rhino_health.lib.metrics.aggregate_metrics.aggregation_methods import weighted_average
from rhino_health.lib.metrics.base_metric import BaseMetric


class AggregatableMetric(BaseMetric, ABC):
    """
    A parent class for metrics that can be aggregated across multiple cohorts
    """

    aggregation_method: Callable = weighted_average
    fetcher: DefaultMetricFetcher
    count_variable_name: str = "variable"

    def data(self):
        data = {
            "metric": self.metric_name(),
            "arguments": self.json(
                exclude_none=True, exclude={"timeout_seconds", "aggregation_method", "fetcher"}
            ),
        }
        if self.timeout_seconds is not None:
            data["timeout_seconds"] = self.timeout_seconds
        return data

    @property
    def fetcher(self):
        return DefaultMetricFetcher()


class CountBasedMetric(AggregatableMetric, ABC):
    """
    A parent class for metrics that requires calculation of the Count metrics first, before the actual metric can be
    calculated
    """

    user_groupings: Optional[
        list
    ] = None  # As the inner count metric is calculated with internal groupings needed
    # for the specific metric, allow the user to specify additional groupings for the outer metric
    user_data_filters: Optional[
        list
    ] = None  # As some inner count metrics are calculated with internal
    # groupings needed for the specific metric, allow the user to specify additional groupings for the outer metric

    def get_count_configuration(self):
        raise NotImplementedError
