# -*- coding: UTF-8 -*-

import datetime

import pydantic
from typing import Any, Dict, List, Optional


class BranchLocation(pydantic.BaseModel):
    longitude: float
    latitude: float
    name: str
    address: str

    model_config = {"frozen": True}

    @classmethod
    @pydantic.field_validator("longitude")
    def validate_longitude(cls, value: float):
        if value < -180 or value > 180:
            raise ValueError("Longitude must be between -180 and 180")
        return value

    @classmethod
    @pydantic.field_validator("latitude")
    def validate_latitude(cls, value: float):
        if value < -90 or value > 90:
            raise ValueError("Latitude must be between -90 and 90")
        return value


class Branch(pydantic.BaseModel):
    id: str
    name: str
    gmt: str
    enabled: bool
    deleted: bool
    location: BranchLocation

    model_config = {"frozen": True}


class LineMetrics(pydantic.BaseModel):
    wait_avg: float
    wait_time: float
    min_wait_time: float
    max_wait_time: float
    serve_avg: float
    serve_time: float
    min_serve_time: float
    max_serve_time: float
    waiting_time_estimation: float

    model_config = {"frozen": True}


class AppointmentSettingsOperationRange(pydantic.BaseModel):
    howManyDays: int
    daysAhead: int


# TODO: This is incomplete
class AppointmentSettingsSetCalendars(pydantic.BaseModel):
    pass


class LineAppointmentSettings(pydantic.BaseModel):
    operationRange: AppointmentSettingsOperationRange
    setCalendars: List[AppointmentSettingsSetCalendars] = []
    cancelWindow: int
    sets: Dict[str, Any]
    enabled: bool


class Line(pydantic.BaseModel):
    id: str
    name: str
    chars: str
    waiting_tickets: int
    enabled: bool
    deleted: bool
    metrics: LineMetrics
    appointment_settings: LineAppointmentSettings
    color: Optional[str]

    model_config = {"frozen": True}


class AppointmentSlot(pydantic.BaseModel):
    index: str
    indexInsideSet: int
    duration: int
    appointment_slot_idx: int
    appointment_set: str
    attending_slot: str
    serve_as_group: bool
    status: str
    name: str


class AppointmentDaySchedule(pydantic.BaseModel):
    date_time: datetime.datetime
    slots: List[AppointmentSlot]

    model_config = {"frozen": True}
