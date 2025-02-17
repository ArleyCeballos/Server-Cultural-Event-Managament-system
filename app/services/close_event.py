from app.infra.postgres.crud.close_event import crud_close_event
from app.services.base import BaseService


class ServiceCloseEvent(BaseService):
    ...


service_close_event = ServiceCloseEvent(crud=crud_close_event)
