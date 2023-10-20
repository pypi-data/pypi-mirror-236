from abc import ABC
from typing import Optional

from rhino_health.lib.metrics import Count
from rhino_health.lib.metrics.aggregatable_metric import CountBasedMetric
from rhino_health.lib.metrics.base_metric import BaseMetric, TwoByTwoTableMetricResponse
from rhino_health.lib.metrics.filter_variable import FilterVariableTypeOrColumnName


class TwoByTwoTableBasedMetric(CountBasedMetric, ABC):
    """
    Abstract class for metrics that are based on a two by two table
    """

    variable: FilterVariableTypeOrColumnName
    detected_column_name: FilterVariableTypeOrColumnName
    exposed_column_name: FilterVariableTypeOrColumnName

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.group_by:
            if (
                self.detected_column_name in self.group_by.groupings
                or self.exposed_column_name in self.group_by.groupings
            ):
                raise ValueError("Can not group by detected_column_name or exposed_column_name")


class TwoByTwoTable(TwoByTwoTableBasedMetric):
    """
    Returns the two by two table of entries for a specified VARIABLE
    """

    @classmethod
    def metric_name(cls):
        return "two_by_two_table"

    def get_count_configuration(self):
        """
        Returns the configuration for the Count metric that is required for the calculation of the two by two table.
        """
        self.user_groupings = self.group_by.groupings if self.group_by else []
        return Count(
            variable=self.variable,
            group_by={
                "groupings": [
                    self.detected_column_name,
                    self.exposed_column_name,
                    *self.user_groupings,
                ]
            },
        )

    @property
    def metric_response(self):
        """
        Returns the response class for the metric
        """
        return TwoByTwoTableMetricResponse


class OddsRatio(TwoByTwoTable):
    """
    Returns the odds ratio of entries for a specified VARIABLE
    """

    @classmethod
    def metric_name(cls):
        return "odds_ratio"


class Odds(CountBasedMetric):
    """
    Returns the odds of entries for a specified VARIABLE where the odd is calculated by the ratio of the number of true
     occurrences to the number of false occurrences.
    """

    variable: FilterVariableTypeOrColumnName
    column_name: FilterVariableTypeOrColumnName

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def metric_name(cls):
        return "odds"

    def get_count_configuration(self):
        self.user_groupings = self.group_by.groupings if self.group_by else []
        return Count(
            variable=self.variable, group_by={"groupings": [self.column_name, *self.user_groupings]}
        )


class Risk(TwoByTwoTable):
    """
    Returns the risk of entries for a specified VARIABLE
    """

    @classmethod
    def metric_name(cls):
        return "risk"


class RiskRatio(TwoByTwoTable):
    """
    Returns the risk ratio of entries for a specified VARIABLE
    """

    @classmethod
    def metric_name(cls):
        return "risk_ratio"
