from typing import Any, Dict, List, Optional, Tuple, Union

from pydantic import BaseModel
from typing_extensions import Literal

from aporia.sdk.custom_metrics import CustomMetric
from aporia.sdk.datasets import DatasetType
from aporia.sdk.fields import Field, FieldGroup
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
    FixedTimeframe,
    MetricParameters,
    VersionSelection,
    WidgetType,
)


class MetricWidgetDataOptionsAnnotations(BaseModel):
    phase: DatasetType
    metric: Union[MetricType, str]
    version: VersionSelection = VersionSelection()
    field: Optional[Dict] = None
    fieldCategory: Optional[FieldGroup] = None
    baseline: Optional[BaselineConfiguration] = None
    threshold: Optional[float] = None
    k: Optional[int] = None
    class_name: Optional[str] = None
    average: Optional[
        AverageMethod
    ] = None  # TODO: Move all metric-related definitions to a single, appropriate, place
    parameters: Optional[MetricParameters] = None
    isModelMetric: bool = True  # TODO: This depends on dataset stats vs column stats
    isCustomMetric: bool = False
    isAggregableMetric: bool = True
    isCodeBasedMetric: bool = False
    dataSegment: Optional[Dict] = None
    dataSegmentId: Optional[str] = None
    dataSegmentName: Optional[str] = None
    dataSegmentValue: Optional[
        Any
    ] = None  # TODO: For some reason, this is casting numerics to strings. Changed "Union[int, float, str]" to "Any"
    dataSegmentBucketName: Optional[str] = None

    def dict(self, *args, **kwargs):
        return {k: v for k, v in super().dict(*args, **kwargs).items() if v is not None}


class MetricWidgetDataOptionsFilters(BaseModel):
    annotations: MetricWidgetDataOptionsAnnotations
    timeframe: Optional[Union[str, FixedTimeframe]] = None

    def dict(self, *args, **kwargs):
        return {k: v for k, v in super().dict(*args, **kwargs).items() if v is not None}


class MetricWidgetDataOptions(BaseModel):
    display: DisplayOptions = DisplayOptions()
    filters: MetricWidgetDataOptionsFilters


class MetricWidget(BaseWidget):
    type: Literal[WidgetType.METRIC] = WidgetType.METRIC
    dataOptions: List[MetricWidgetDataOptions]  # Length must be at most 2?

    @classmethod
    def create(
        cls,
        position: Tuple[int, int],
        size: Tuple[int, int],
        title: str,
        metric: MetricType,
        timeframe: Optional[Union[str, FixedTimeframe]] = None,
        phase: DatasetType = DatasetType.SERVING,
        version: VersionSelection = VersionSelection(),
        field: Optional[Field] = None,
        baseline: Optional[BaselineConfiguration] = None,
        threshold: Optional[float] = None,
        k: Optional[int] = None,
        class_name: Optional[str] = None,
        average: Optional[AverageMethod] = None,
        custom_metric: Optional[CustomMetric] = None,
        segment: Optional[Segment] = None,
        segment_value: Optional[Any] = None,
    ) -> "MetricWidget":
        if (segment is None) != (segment_value is None):
            raise ValueError(
                "For using segments, both segment and segment_value arguments are needed"
            )

        return MetricWidget(
            x=position[0],
            y=position[1],
            w=size[0],
            h=size[1],
            name=title,
            dataOptions=[
                MetricWidgetDataOptions(
                    filters=MetricWidgetDataOptionsFilters(
                        timeframe=timeframe,
                        annotations=MetricWidgetDataOptionsAnnotations(
                            phase=phase,
                            metric=metric
                            if metric is not MetricType.CUSTOM_METRIC
                            else custom_metric.id,
                            version=version,
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
                            dataSegmentValue=segment_value if segment is not None else None,
                            dataSegmentBucketName=[
                                bucket["name"]
                                for bucket in segment.to_widget()["buckets"]
                                if bucket["value"] == segment_value
                            ][0]
                            if segment is not None
                            else None,
                        ),
                    )
                )
            ],
        )

    def compare(
        self,
        phase: DatasetType = DatasetType.SERVING,
        version: VersionSelection = VersionSelection(),
        timeframe: Optional[Union[str, FixedTimeframe]] = None,
        field: Optional[Field] = None,
        baseline: Optional[BaselineConfiguration] = None,
        threshold: Optional[float] = None,
        k: Optional[int] = None,
        class_name: Optional[str] = None,
        average: Optional[AverageMethod] = None,
        segment: Optional[Segment] = None,
        segment_value: Optional[Any] = None,
    ) -> "MetricWidget":
        # TODO: Consider enforcing compare limits here
        metric = self.dataOptions[0].filters.annotations.metric
        custom_metric_id = None
        if not isinstance(metric, MetricType):
            metric = MetricType.CUSTOM_METRIC
            custom_metric_id = self.dataOptions[0].filters.annotations.parameters.id
        color = self.dataOptions[-1].display.color + 1

        self.dataOptions.append(
            MetricWidgetDataOptions(
                display=DisplayOptions(color=color),
                filters=MetricWidgetDataOptionsFilters(
                    timeframe=timeframe,
                    annotations=MetricWidgetDataOptionsAnnotations(
                        phase=phase,
                        metric=metric
                        if metric is not MetricType.CUSTOM_METRIC
                        else custom_metric_id,
                        version=version,
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
                        dataSegmentValue=segment_value if segment is not None else None,
                        dataSegmentBucketName=[
                            bucket["name"]
                            for bucket in segment.to_widget()["buckets"]
                            if bucket["value"] == segment_value
                        ][0]
                        if segment is not None
                        else None,
                    ),
                ),
            ),
        )
        return self
