from datetime import date as date_type, time as time_type
from typing import Optional

from pydantic import BaseModel


class Event(BaseModel):
    title: str
    date: str
    start_time: str

    end_time: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    organizer: Optional[str] = None
    registration_url: Optional[str] = None
    registration_deadline: Optional[str] = None


class NormalizedEvent(BaseModel):
    title: str
    date: date_type
    start_time: time_type

    end_time: Optional[time_type] = None
    location: Optional[str] = None
    description: Optional[str] = None
    organizer: Optional[str] = None
    registration_url: Optional[str] = None
    registration_deadline: Optional[date_type] = None