from datetime import datetime

from pydantic import BaseModel, Field


class CreateHistoryEventState(BaseModel):
    justification: str = Field(...)
    state_id: int = Field(...)
    event_id: int = Field(...)
    user_email: str = Field(...)


class UpdateHistoryEventState(BaseModel):
    ...


class HistoryEventStateDB(CreateHistoryEventState):
    id: int = Field(...)

    created_at: datetime = Field(...)

    class Config:
        from_attributes = True


class HistoriyEventRelation(BaseModel):
    id: int = Field(...)
    justification: str = Field(...)
    created_date: datetime = Field(...)
    user_email: str = Field(...)
    event_id: int = Field(...)
    event_name: str = Field(...)
    state_id: int = Field(...)
    state_name: str = Field(...)
