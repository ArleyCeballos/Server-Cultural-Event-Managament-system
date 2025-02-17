from app.infra.postgres.crud.eventstate import crud_event_state
from app.services.base import BaseService


class ServiceEventState(BaseService):
    ...


service_event_state = ServiceEventState(crud=crud_event_state)
