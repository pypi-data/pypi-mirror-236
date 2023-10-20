from rhino_health.lib.metrics.base_metric import BaseMetric, KaplanMeierMetricResponse
from rhino_health.lib.metrics.filter_variable import FilterVariableTypeOrColumnName


class KaplanMeier(BaseMetric):
    """
    Returns the k-percentile of entries for a specified VARIABLE
    """

    time_variable: FilterVariableTypeOrColumnName
    event_variable: FilterVariableTypeOrColumnName

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def metric_name(cls):
        return "kaplan_meier"

    @classmethod
    def uses_cloud_aggregation(cls):
        return True

    @property
    def metric_response(self):
        return KaplanMeierMetricResponse
