from typing import Optional

from pydantic import BaseModel, Field


class CreateEvent(BaseModel):
    user_email: str = Field(...)
    parent_event_id: Optional[int] = Field(None)
    event_type_id: int = Field(...)
    general_name: str = Field(...)
    specific_name: Optional[str] = Field(None)
    date_start: str = Field(...)
    date_finishing: str = Field(...)
    hour_start: str = Field(...)
    hour_finishing: str = Field(...)
    place_id: int = Field(...)
    user_name: str = Field(...)
    phone: Optional[str] = Field(None)
    identification_type: str = Field(...)
    identification_value: str = Field(...)
    email: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    observation: Optional[str] = Field(None)
    duration: Optional[str] = Field(None)
    mounting_date: Optional[str] = Field(None)
    mounting_start_hour: Optional[str] = Field(None)
    mounting_finishing_hour: Optional[str] = Field(None)
    technic_contact: Optional[str] = Field(None)
    rider: Optional[str] = Field(None)
    min_to_min: Optional[str] = Field(None)
    communication_contact: Optional[str] = Field(None)
    pulep: Optional[str] = Field(None)
    access_data: Optional[str] = Field(None)
    ticket_company: Optional[str] = Field(None)
    age_restriction: Optional[str] = Field(None)
    agreement: Optional[str] = Field(None)


class EventDB(CreateEvent):
    id: int = Field(...)

    class Config:
        from_attributes = True


class UpdateEvent(BaseModel):
    event_type_id: Optional[int] = None
    state: Optional[str] = None
    date_state: Optional[str] = None
    general_name: Optional[str] = None
    specific_name: Optional[str] = None
    date_start: Optional[str] = None
    date_finishing: Optional[str] = None
    hour_start: Optional[str] = None
    hour_finishing: Optional[str] = None
    place_id: Optional[int] = None
    user_name: Optional[str] = None
    phone: Optional[str] = None
    identification_type: Optional[str] = None
    identification_value: Optional[str] = None
    email: Optional[str] = None
    description: Optional[str] = None
    observation: Optional[str] = None
    duration: Optional[str] = None
    mounting_date: Optional[str] = None
    mounting_start_hour: Optional[str] = None
    mounting_finishing_hour: Optional[str] = None
    technic_contact: Optional[str] = None
    rider: Optional[str] = None
    min_tomin: Optional[str] = None
    communication_contact: Optional[str] = None
    pulep: Optional[str] = None
    access_data: Optional[str] = None
    ticket_company: Optional[str] = None
    age_restriction: Optional[str] = None
    agreement: Optional[str] = None


class StatusAccomplishment(BaseModel):
    total: int
    not_complete: int
    complete: int
