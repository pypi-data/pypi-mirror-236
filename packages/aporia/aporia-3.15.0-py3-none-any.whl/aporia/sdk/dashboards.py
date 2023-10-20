from enum import Enum
from typing import Any, Dict, Type

from pydantic import BaseModel, validator


class WidgetType(Enum):
    METRIC = "metric"
    TIMESERIES = "timeseries"
    DISTRIBUTION = "distribution"
    TABLE = "datahealthtable"
    TEXT = "text"


class BaseWidgetData(BaseModel):
    pass


class MetricWidgetData(BaseWidgetData):
    pass


class TimeseriesWidgetData(BaseWidgetData):
    pass


class TableWidgetData(BaseWidgetData):
    pass


class DistributionWidgetData(BaseWidgetData):
    pass


class TextWidgetData(BaseWidgetData):
    text: str


WIDGET_TYPE_TO_WIDGET_DATA_CLASS: Dict[WidgetType, Type[BaseWidgetData]] = {
    WidgetType.METRIC: MetricWidgetData,
    WidgetType.TIMESERIES: TimeseriesWidgetData,
    WidgetType.DISTRIBUTION: DistributionWidgetData,
    WidgetType.TABLE: TableWidgetData,
    WidgetType.TEXT: TextWidgetData,
}


class Widget(BaseModel):
    loc_x: int
    loc_y: int
    type: WidgetType
    data: BaseWidgetData

    @validator("data", pre=True)
    @classmethod
    def _parse_data(cls, value: Any, values: Dict[str, Any]) -> BaseWidgetData:
        """Validates data matches the widget type.

        Args:
            value: data dict to validate
            values: other attributes of Widget (type)

        Returns:
            BaseWidgetData: WidgetData object
        """
        # Parsing `data` requires `type` to be parsed
        if "type" not in values:
            return value

        if values["type"] not in WIDGET_TYPE_TO_WIDGET_DATA_CLASS:
            raise ValueError(f"Unsupported widget type {values['type']}")

        if not isinstance(value, dict):
            raise ValueError("expected a dict containing widget data")

        parameters_cls = WIDGET_TYPE_TO_WIDGET_DATA_CLASS[values["type"]]
        return parameters_cls(**value)
