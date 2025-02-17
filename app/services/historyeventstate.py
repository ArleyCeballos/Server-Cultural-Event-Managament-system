from typing import Any, Dict, List, Optional

from app.infra.postgres.crud.historyeventstate import crud_history_event_state
from app.services.base import BaseService


class ServiceHistoryEventState(BaseService):
    async def get_by_event_id(self, *, event_id: int) -> List[Dict[str, Any]]:
        objs_db = await self._crud.get_by_event_id(event_id=event_id)
        return objs_db

    async def get_all(
        self,
        *,
        skip: Optional[int] = None,
        limit: Optional[int] = None,
        payload: Dict[str, Any] = {},
    ) -> List[Dict[str, Any]]:
        objs_db = await self._crud.get_all(skip=skip, limit=limit)
        return objs_db

    async def get_by_state_id(self, *, state_id: int) -> List[Dict[str, Any]]:
        objs_db = await self._crud.get_by_state_id(state_id=state_id)
        return objs_db


service_history_event_state = ServiceHistoryEventState(crud=crud_history_event_state)
