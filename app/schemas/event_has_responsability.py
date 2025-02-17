from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CreateEventHasResponsability(BaseModel):
    event_id: int
    responsability_by_mode_id: Optional[int] = Field(None)
    accomplishment_id: int
    specific_responsability_id: Optional[int] = Field(None)


class UpdateEventHasResponsability(BaseModel):
    ...


class EventHasResponsabilityDB(BaseModel):
    id: int
    event_id: int
    event_name: str
    responsability_by_mode_id: Optional[int]
    responsability_by_mode_name: Optional[str]
    specific_responsability_id: Optional[int]
    specific_responsability_name: Optional[str]
    accomplishment_id: int
    accomplishment_creation_date: datetime
    accomplishment_compliment_date: Optional[datetime]
    accomplishment_status: bool

    class Config:
        from_attributes = True
