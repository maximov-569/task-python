from datetime import datetime

from pydantic import BaseModel

from src.service_state.models import StateChoice


class SHService(BaseModel):
    name: str
    state: StateChoice
    description: str


class SHServiceStateHistory(BaseModel):
    description: str
    state: StateChoice
    time_in: datetime
    time_out: datetime | None


class ServiceSlaInput(BaseModel):
    interval_start: datetime
    interval_end: datetime
