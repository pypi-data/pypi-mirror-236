from abc import ABC
from datetime import datetime

from rhino_health.lib.metrics import Count
from rhino_health.lib.metrics.aggregatable_metric import CountBasedMetric
from rhino_health.lib.metrics.base_metric import BaseMetric, DataFilter
from rhino_health.lib.metrics.filter_variable import FilterVariableTypeOrColumnName


class TimeRangeBasedMetric(CountBasedMetric, ABC):
    """
    Abstract class for metrics that are based on a time range
    """

    variable: FilterVariableTypeOrColumnName
    detected_column_name: FilterVariableTypeOrColumnName
    time_column_name: FilterVariableTypeOrColumnName
    start_time: datetime
    end_time: datetime

    def __init__(self, start_time: str, end_time: str, **kwargs):
        # Assuming time_string is in UTC format (e.g., "2023-09-05T12:00:00Z")
        super().__init__(
            start_time=datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ"),
            end_time=datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%SZ"),
            **kwargs,
        )


class Prevalence(TimeRangeBasedMetric):
    """
    Returns the prevalence of entries for a specified VARIABLE
    """

    @classmethod
    def metric_name(cls):
        return "prevalence"

    def get_count_configuration(self):
        self.user_groupings = self.group_by.groupings if self.group_by else []
        self.user_data_filters = self.data_filters if self.data_filters else []
        return Count(
            variable=self.variable,
            group_by={"groupings": [self.detected_column_name, *self.user_groupings]},
            data_filters=[
                DataFilter(
                    filter_column=self.time_column_name,
                    filter_value=self.end_time,
                    filter_type="<=",
                ),
                *self.user_data_filters,
            ],
        )


class Incidence(TimeRangeBasedMetric):
    """
    Returns the incidence of entries for a specified VARIABLE
    """

    @classmethod
    def metric_name(cls):
        return "incidence"

    def get_count_configuration(self):
        self.user_groupings = self.group_by.groupings if self.group_by else []
        self.user_data_filters = self.data_filters if self.data_filters else []

        return Count(
            variable=self.variable,
            group_by={"groupings": [self.detected_column_name, *self.user_groupings]},
            data_filters=[
                DataFilter(
                    filter_column=self.time_column_name,
                    filter_value=self.start_time,
                    filter_type=">=",
                ),
                DataFilter(
                    filter_column=self.time_column_name,
                    filter_value=self.end_time,
                    filter_type="<=",
                ),
                *self.user_data_filters,
            ],
        )
