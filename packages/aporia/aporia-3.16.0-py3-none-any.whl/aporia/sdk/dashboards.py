from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, validator

from aporia.sdk.base import BaseAporiaResource
from aporia.sdk.client import Client
from aporia.sdk.widgets import BaseWidget
from aporia.sdk.widgets.base import FixedTimeframe, WidgetType
from aporia.sdk.widgets.data_health_table_widget import DataHealthTableWidget
from aporia.sdk.widgets.distribution_widget import DistributionWidget
from aporia.sdk.widgets.histogram_over_time_widget import HistogramOverTimeWidget
from aporia.sdk.widgets.metric_widget import MetricWidget
from aporia.sdk.widgets.text_widget import TextWidget
from aporia.sdk.widgets.timeseries_widget import TimeSeriesWidget


class DashboardGlobalFilters(BaseModel):
    timeframe: Union[str, FixedTimeframe]


Widget = Union[
    TextWidget,
    DataHealthTableWidget,
    DistributionWidget,
    HistogramOverTimeWidget,
    MetricWidget,
    TimeSeriesWidget,
]

WIDGET_TYPE_TO_CONFIG_CLASS = {
    WidgetType.TEXT: TextWidget,
    WidgetType.DISTRIBUTION: DistributionWidget,
    WidgetType.METRIC: MetricWidget,
    WidgetType.TIME_SERIES: TimeSeriesWidget,
    WidgetType.TIME_SERIES_HISTOGRAM: HistogramOverTimeWidget,
    WidgetType.ANOMALY_TABLE: DataHealthTableWidget,
}


class DashboardConfiguration(BaseModel):
    widgets: List[Widget]
    global_filters: DashboardGlobalFilters

    @validator("widgets", pre=True)
    @classmethod
    def _parse_connection(cls, value: Any, values: Dict[str, Any]) -> List[Widget]:
        return dashboard_widgets_pre_validator(value, values)


def dashboard_widgets_pre_validator(value: Any, values: Dict[str, Any]) -> List[Widget]:
    """Reads data of a dataset.

    Args:
        value: connection dict to validate
        values: other attributes of DataSource (type)

    Returns:
        List[Widget] object
    """
    # Parsing `widget` requires `type` to be parsed
    widgets = []

    if not isinstance(value, list):
        raise ValueError("expected a list containing widget configurations")

    for widget_configuration in value:
        if isinstance(widget_configuration, BaseWidget):
            widgets.append(widget_configuration)
            continue

        if "type" not in widget_configuration:
            raise ValueError("Received widget with no type")

        if widget_configuration["type"] not in WIDGET_TYPE_TO_CONFIG_CLASS:
            raise ValueError(f"Unsupported widget type {values['type']}")

        if not isinstance(widget_configuration, dict):
            raise ValueError("expected a dict containing data source configuration")

        config_cls = WIDGET_TYPE_TO_CONFIG_CLASS[widget_configuration["type"]]
        widgets.append(config_cls(**widget_configuration))

    return widgets


class Dashboard(BaseAporiaResource):
    def __init__(self, client: Client, data: Dict):
        self.client = client
        self.__update_members(data)

    def __update_members(self, data: Dict):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.definition = DashboardConfiguration(**data["definition"])
        self.raw_data = data

    @classmethod
    def get_all(cls, client: Client, model_id: Optional[str] = None) -> List["Dashboard"]:
        response = client.send_request(
            f"/dashboards",
            "GET",
            params={"model_id": model_id} if model_id is not None else None,
            url_search_replace=("/api/v1/", "/v1/crud-service/"),
        )

        client.assert_response(response)

        return [cls(client=client, data=entry) for entry in response.json()]

    @classmethod
    def create(
        cls,
        client: Client,
        name: str,
        description: str,
        model_id: Optional[str],
        definition: DashboardConfiguration,
        owner: Optional[str] = None,
    ) -> "Dashboard":
        response = client.send_request(
            "/dashboards",
            "POST",
            {
                "name": name,
                "description": description,
                "model_id": model_id,
                "definition": definition.dict(),
                "owner": owner,
            },
            url_search_replace=("/api/v1/", "/v1/crud-service/"),
        )

        client.assert_response(response)

        return cls(client=client, data=response.json())

    @classmethod
    def read(cls, client: Client, id: str) -> "Dashboard":
        response = client.send_request(
            f"/dashboards/{id}",
            "GET",
            url_search_replace=("/api/v1/", "/v1/crud-service/"),
        )
        client.assert_response(response)
        return cls(client=client, data=response.json())

    def update(self, **kwargs):
        args = {}

        if "name" in kwargs:
            args["name"] = kwargs["name"]

        if "description" in kwargs:
            args["description"] = kwargs["description"]

        if "owner" in kwargs:
            args["owner"] = kwargs["owner"]

        if "definition" in kwargs:
            args["definition"] = kwargs["definition"].dict()

        response = self.client.send_request(
            f"/dashboards/{self.id}",
            "PUT",
            args,
            url_search_replace=("/api/v1/", "/v1/crud-service/"),
        )
        self.client.assert_response(response)
        self.__update_members(response.json())

    def delete(self):
        response = self.client.send_request(f"/dashboards/{self.id}", "DELETE")
        self.client.assert_response(response)

    @staticmethod
    def delete_by_id(client: Client, id: str):
        response = client.send_request(f"/dashboards/{id}", "DELETE")
        client.assert_response(response)
