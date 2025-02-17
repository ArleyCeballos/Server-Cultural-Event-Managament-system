from typing import Any, Dict, List

from app.infra.postgres.crud.event_has_responsability import (
    crud_event_has_responsability,
)
from app.services.base import BaseService


class ServiceEventHasResponsability(BaseService):
    def __init__(self, *, crud: Any) -> None:
        super().__init__(crud=crud)
        self.__crud = crud

    async def get_by_event_id(self, *, event_id: int) -> List[Dict[str, Any]]:
        objs_db = await self.__crud.get_by_event_id(event_id=event_id)
        return objs_db


service_event_has_responsability = ServiceEventHasResponsability(
    crud=crud_event_has_responsability
)
