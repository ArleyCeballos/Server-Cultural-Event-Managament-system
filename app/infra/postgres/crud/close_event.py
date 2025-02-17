from app.infra.postgres.crud.base import CRUDBase
from app.infra.postgres.models.close_event import CloseEvent
from app.schemas.close_event import CreateCloseEvent, UpdateCloseEvent


class CRUDCloseEvent(CRUDBase[CloseEvent, CreateCloseEvent, UpdateCloseEvent]):
    ...


crud_close_event = CRUDCloseEvent(model=CloseEvent)
