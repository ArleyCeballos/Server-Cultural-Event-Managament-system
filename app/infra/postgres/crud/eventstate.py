from app.infra.postgres.crud.base import CRUDBase
from app.infra.postgres.models.eventstate import EventState
from app.schemas.eventstate import CreateEventState, UpdateEventState


class CRUDEventState(CRUDBase[EventState, CreateEventState, UpdateEventState]):
    ...


crud_event_state = CRUDEventState(model=EventState)
