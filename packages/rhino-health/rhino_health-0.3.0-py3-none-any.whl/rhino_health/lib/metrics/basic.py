from rhino_health.lib.metrics.aggregatable_metric import AggregatableMetric
from rhino_health.lib.metrics.aggregate_metrics.aggregation_data_fetchers import (
    MultipleMetricFetcher,
)
from rhino_health.lib.metrics.aggregate_metrics.aggregation_methods import (
    standard_deviation,
    sum_aggregation,
)
from rhino_health.lib.metrics.filter_variable import FilterVariableTypeOrColumnName


class Count(AggregatableMetric):
    """
    Returns the count of entries for a specified VARIABLE
    """

    variable: FilterVariableTypeOrColumnName

    def __init__(self, aggregation_method=sum_aggregation, **kwargs):
        super().__init__(aggregation_method=aggregation_method, **kwargs)

    @classmethod
    def metric_name(cls):
        return "count"


class Mean(AggregatableMetric):
    """
    Returns the mean value of a specified VARIABLE
    """

    variable: FilterVariableTypeOrColumnName

    @classmethod
    def metric_name(cls):
        return "mean"


class StandardDeviation(AggregatableMetric):
    """
    Returns the standard deviation of a specified VARIABLE
    """

    variable: FilterVariableTypeOrColumnName

    def __init__(self, aggregation_method=standard_deviation, **kwargs):
        super().__init__(
            aggregation_method=aggregation_method,
            **kwargs,
        )

    @classmethod
    def metric_name(cls):
        return "stddev"

    @property
    def fetcher(self):
        return MultipleMetricFetcher([StandardDeviation, Mean])


class Sum(AggregatableMetric):
    """
    Returns the sum of a specified VARIABLE
    """

    variable: FilterVariableTypeOrColumnName

    def __init__(self, aggregation_method=sum_aggregation, **kwargs):
        super().__init__(aggregation_method=aggregation_method, **kwargs)

    @classmethod
    def metric_name(cls):
        return "sum"


COMMON_METRICS = [Count, Mean, StandardDeviation, Sum]
