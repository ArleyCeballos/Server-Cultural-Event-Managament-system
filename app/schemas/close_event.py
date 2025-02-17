from pydantic import BaseModel


class CloseEventDB(BaseModel):
    id: int
    event_id: int
    assistant_total: int
    started_on_time: bool
    finished_on_time: bool
    situations_with_the_organizer: str
    situations_with_the_public: str
    situations_with_ambulance: str
    inspections: str
    logistical_situations: str


class CreateCloseEvent(BaseModel):
    event_id: int
    assistant_total: int
    started_on_time: bool
    finished_on_time: bool
    situations_with_the_organizer: str
    situations_with_the_public: str
    situations_with_ambulance: str
    inspections: str
    logistical_situations: str


class UpdateCloseEvent(BaseModel):
    ...
