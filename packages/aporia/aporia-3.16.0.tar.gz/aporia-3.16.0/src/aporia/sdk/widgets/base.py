import datetime
from enum import Enum
from typing import Dict, Optional, Tuple
import uuid

from pydantic import BaseModel, Field, validator

# TODO: Check with python 3.8


class FixedTimeframe(BaseModel):
    to: datetime.datetime
    from_impl: datetime.datetime = Field(alias="from")

    @validator("to", "from_impl")
    def _validate_utc(cls, value, values):
        if value.tzinfo != datetime.timezone.utc:
            raise ValueError("Timezones must be in UTC")
        return value

    def dict(self, *args, **kwargs):
        return {"to": self.to.isoformat(), "from": self.from_impl.isoformat()}


class DisplayOptions(BaseModel):
    color: int = 0  # 1 for compare


class VersionSelection(BaseModel):
    id: str = "*"


class BaselineType(str, Enum):
    TRAINING = "training"
    RELATIVE_TIME_PERIOD = "relativeTimePeriod"


class TimeUnit(str, Enum):
    DAY = "day"
    MONTH = "month"


class BaselineConfiguration(BaseModel):
    type: BaselineType
    unit: Optional[TimeUnit] = None
    duration: Optional[int] = None

    @validator("unit")
    def _validate_unit(cls, value, values) -> Optional[TimeUnit]:
        if values["type"] == "training" and value is not None:
            raise ValueError("Unit can't be used with training baseline")
        return value

    @validator("duration")
    def _validate_duration(cls, value, values) -> Optional[int]:
        if values["type"] == "training" and value is not None:
            raise ValueError("Unit can't be used with training baseline")
        return value

    def dict(self, *args, **kwargs):
        return {k: v for k, v in super().dict(*args, **kwargs).items() if v is not None}


class MetricParameters(BaseModel):
    id: str


class WidgetType(str, Enum):
    TEXT = "text"
    ANOMALY_TABLE = "anomaly-table"
    DISTRIBUTION = "distribution"
    TIME_SERIES_HISTOGRAM = "time-series-histogram"
    METRIC = "metric"
    TIME_SERIES = "time-series"


class BaseWidget(BaseModel):
    i: str = Field(default_factory=lambda: str(uuid.uuid4()))
    h: int
    w: int  # Capped at 12
    x: int  # Capped at 11?
    y: int
    name: str
    type: WidgetType
    moved: bool = False
    resizable: bool = True
    dependencies: Optional[
        Dict
    ] = None  # TODO: Investigate this, and consider if you want to raise error if it has issues

    @validator("x")
    def _validate_x(cls, value, values):
        if value < 0:
            raise ValueError("x must be non-negative")
        if value >= 12:
            raise ValueError("The grid's x-axis is limited at 12 cells")
        return value

    @validator("y")
    def _validate_y(cls, value, values):
        if value < 0:
            raise ValueError("y must be non-negative")
        return value

    @validator("w")
    def _validate_w(cls, value, values):
        if value <= 0:
            raise ValueError("w must be positive")
        if value > 12:
            raise ValueError("The grid's x-axis is limited at 12 cells")
        return value

    @validator("h")
    def _validate_h(cls, value, values):
        if value <= 0:
            raise ValueError("h must be positive")
        return value

    @classmethod
    def create(
        cls, position: Tuple[int, int], size: Tuple[int, int], *args, **kwargs
    ) -> "BaseWidget":
        raise NotImplementedError()
