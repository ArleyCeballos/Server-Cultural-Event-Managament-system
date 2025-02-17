from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CreateEventState(BaseModel):
    justification: str = Field(...)
    event_id: int = Field(...)
    state_id: int = Field(...)


class UpdateEventState(BaseModel):
    state_id: Optional[int] = Field(None)
    justification: Optional[str] = Field(None)


class EventStateDB(CreateEventState):
    id: int = Field(...)
    created_at: datetime = Field(...)

    class Config:
        from_attributes = True
