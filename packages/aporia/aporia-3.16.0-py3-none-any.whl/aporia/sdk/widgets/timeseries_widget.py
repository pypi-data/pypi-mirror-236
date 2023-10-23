from typing import Any, Dict, List, Optional, Tuple, Union

from pydantic import BaseModel, Field
from typing_extensions import Literal

from aporia.sdk.custom_metrics import CustomMetric
from aporia.sdk.datasets import DatasetType
from aporia.sdk.fields import FieldGroup
from aporia.sdk.metrics import (
    is_aggregable_metric,
    is_code_based_metric,
    is_custom_metric,
    is_model_metric,
    MetricType,
)
from aporia.sdk.monitors import AverageMethod
from aporia.sdk.segments import Segment
from aporia.sdk.widgets.base import (
    BaselineConfiguration,
    BaseWidget,
    DisplayOptions,
    MetricParameters,
    VersionSelection,
    WidgetType,
)


class TimeSeriesWidgetDataOptionsAnnotations(BaseModel):
    phase: Literal[DatasetType.SERVING] = DatasetType.SERVING
    metric: Union[MetricType, str]
    version: Union[VersionSelection, List[VersionSelection]] = VersionSelection()
    field: Optional[Dict] = None
    fieldCategory: Optional[FieldGroup] = None
    granularity: Optional[
        str
    ] = None  # Optional[TimePeriod] = None # TODO: Find a way to implicitly convert a string to TimePeriod
    baseline: Optional[BaselineConfiguration] = None
    threshold: Optional[float] = None
    k: Optional[int] = None
    class_name: Optional[str] = None
    average: Optional[
        AverageMethod
    ] = None  # TODO: Move all metric-related definitions to a single, appropriate, place
    parameters: Optional[MetricParameters] = None
    isModelMetric: bool = True
    isCustomMetric: bool = False
    isAggregableMetric: bool = True
    isCodeBasedMetric: bool = False
    dataSegment: Optional[Dict] = None
    dataSegmentId: Optional[str] = None
    dataSegmentName: Optional[str] = None
    dataSegmentValue: Optional[
        Union[List[Union[int, float, str]], Union[int, float, str]]
    ] = None  # For dataSegmentValue and version, just one of them is a list
    dataSegmentBucketName: Optional[
        str
    ] = None  # This appears only when dataSegmentValue is not a list

    def dict(self, *args, **kwargs):
        return {k: v for k, v in super().dict(*args, **kwargs).items() if v is not None}


class TimeSeriesWidgetDataOptionsFilters(BaseModel):
    annotations: TimeSeriesWidgetDataOptionsAnnotations


class TimeSeriesWidgetDataOptions(BaseModel):
    display: DisplayOptions = DisplayOptions()
    filters: TimeSeriesWidgetDataOptionsFilters


class TimeSeriesWidget(BaseWidget):
    type: Literal[WidgetType.TIME_SERIES] = WidgetType.TIME_SERIES
    dataOptions: List[TimeSeriesWidgetDataOptions]  # Length must be at most 2?

    @classmethod
    def create(
        cls,
        position: Tuple[int, int],
        size: Tuple[int, int],
        title: str,
        metric: MetricType,
        # Mutually Exclusive
        version: Optional[VersionSelection] = None,
        versions: Optional[List[VersionSelection]] = None,
        field: Optional[Field] = None,
        baseline: Optional[BaselineConfiguration] = None,
        threshold: Optional[float] = None,
        k: Optional[int] = None,
        class_name: Optional[str] = None,
        average: Optional[AverageMethod] = None,
        custom_metric: Optional[CustomMetric] = None,
        segment: Optional[Segment] = None,
        # Mutually Exclusive
        segment_value: Optional[Any] = None,
        segment_values: Optional[List[Any]] = None,
        granularity: Optional[str] = None,
    ) -> "TimeSeriesWidget":
        if version and versions:
            raise ValueError("Can't use both version and versions arguments")

        if version is None and versions is None:
            version = VersionSelection()

        if segment_value is not None and segment_values is not None:
            raise ValueError("Can't use both segment_value and segment_values arguments")

        if segment is not None and segment_value is None and segment_values is None:
            if versions:
                raise ValueError(
                    "When using multiple versions and a segment, must specify segment_value"
                )
            segment_values = segment.values

        if segment_values is not None and versions is not None:
            raise ValueError("Can't pass segment_values when using multiple versions")

        if versions is None and segment is not None and segment_value is not None:
            segment_values = [segment_value]
            segment_value = None

        if (segment is None) != (segment_value is None and segment_values is None):
            raise ValueError(
                "For using segments, both segment and segment_value/segment_values arguments are needed"
            )

        return TimeSeriesWidget(
            x=position[0],
            y=position[1],
            w=size[0],
            h=size[1],
            name=title,
            dataOptions=[
                TimeSeriesWidgetDataOptions(
                    filters=TimeSeriesWidgetDataOptionsFilters(
                        annotations=TimeSeriesWidgetDataOptionsAnnotations(
                            metric=metric
                            if metric is not MetricType.CUSTOM_METRIC
                            else custom_metric.id,
                            version=version or versions,
                            field=field.to_widget() if field is not None else None,
                            fieldCategory=field.group if field is not None else None,
                            baseline=baseline,
                            threshold=threshold,
                            k=k,
                            class_name=class_name,
                            average=average,
                            parameters=MetricParameters(id=custom_metric.id)
                            if custom_metric is not None
                            else None,
                            isModelMetric=is_model_metric(metric),
                            isCustomMetric=is_custom_metric(metric),
                            isAggregableMetric=is_aggregable_metric(metric),
                            isCodeBasedMetric=is_code_based_metric(metric),
                            dataSegment=segment.to_widget() if segment is not None else None,
                            dataSegmentId=segment.id if segment is not None else None,
                            dataSegmentName=segment.name if segment is not None else None,
                            dataSegmentValue=(segment_value or segment_values)
                            if segment is not None
                            else None,
                            dataSegmentBucketName=[
                                bucket["name"]
                                for bucket in segment.to_widget()["buckets"]
                                if bucket["value"] == segment_value
                            ][0]
                            if segment is not None and segment_value is not None
                            else None,
                            granularity=granularity,
                        ),
                    )
                )
            ],
        )

    def compare(
        self,
        # Mutually Exclusive
        version: Optional[VersionSelection] = None,
        versions: Optional[List[VersionSelection]] = None,
        field: Optional[Field] = None,
        baseline: Optional[BaselineConfiguration] = None,
        threshold: Optional[float] = None,
        k: Optional[int] = None,
        class_name: Optional[str] = None,
        average: Optional[AverageMethod] = None,
        segment: Optional[Segment] = None,
        # Mutually Exclusive
        segment_value: Optional[Any] = None,
        segment_values: Optional[List[Any]] = None,
    ) -> "TimeSeriesWidget":
        # TODO: Consider enforcing compare limits here
        metric = self.dataOptions[0].filters.annotations.metric
        custom_metric_id = None
        # TODO: Doesn't support code-based metrics
        if not isinstance(metric, MetricType):
            metric = MetricType.CUSTOM_METRIC
            custom_metric_id = self.dataOptions[0].filters.annotations.parameters.id
        granularity = self.dataOptions[0].filters.annotations.granularity
        color = self.dataOptions[-1].display.color + 1

        self.dataOptions.append(
            TimeSeriesWidgetDataOptions(
                display=DisplayOptions(color=color),
                filters=TimeSeriesWidgetDataOptionsFilters(
                    annotations=TimeSeriesWidgetDataOptionsAnnotations(
                        metric=metric
                        if metric is not MetricType.CUSTOM_METRIC
                        else custom_metric_id,
                        version=version or versions,
                        field=field.to_widget() if field is not None else None,
                        fieldCategory=field.group if field is not None else None,
                        baseline=baseline,
                        threshold=threshold,
                        k=k,
                        class_name=class_name,
                        average=average,
                        parameters=MetricParameters(id=custom_metric_id)
                        if custom_metric_id is not None
                        else None,
                        isModelMetric=is_model_metric(metric),
                        isCustomMetric=is_custom_metric(metric),
                        isAggregableMetric=is_aggregable_metric(metric),
                        isCodeBasedMetric=is_code_based_metric(metric),
                        dataSegment=segment.to_widget() if segment is not None else None,
                        dataSegmentId=segment.id if segment is not None else None,
                        dataSegmentName=segment.name if segment is not None else None,
                        dataSegmentValue=(segment_value or segment_values)
                        if segment is not None
                        else None,
                        dataSegmentBucketName=[
                            bucket["name"]
                            for bucket in segment.to_widget()["buckets"]
                            if bucket["value"] == segment_value
                        ][0]
                        if segment is not None and segment_value is not None
                        else None,
                        granularity=granularity,
                    ),
                ),
            )
        )
        return self
