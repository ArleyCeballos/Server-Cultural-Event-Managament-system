from typing import Any, Dict, List, Optional

from app.infra.postgres.crud.base import CRUDBase
from app.infra.postgres.models.historyeventstate import HistoryEventState
from app.schemas.historyeventstate import (
    CreateHistoryEventState,
    UpdateHistoryEventState,
)


class CRUDHistoryEventState(
    CRUDBase[HistoryEventState, CreateHistoryEventState, UpdateHistoryEventState]
):
    async def get_by_event_id(self, *, event_id: int) -> List[HistoryEventState]:
        objs_db = (
            await self.model.filter(event_id=event_id)
            .all()
            .prefetch_related("event", "state")
            .order_by("-created_at")
            .values(
                id="id",
                justification="justification",
                created_date="created_at",
                event_id="event__id",
                event_name="event__general_name",
                state_id="state__id",
                state_name="state__name",
            )
        )
        return objs_db

    async def get_all(
        self,
        skip: Optional[int] = None,
        limit: Optional[int] = None,
        payload: Dict[str, Any] = {},
    ) -> List[Dict[str, Any]]:
        query = self.model.filter(**payload) if payload else self.model
        model = query.all().order_by("-created_at")
        if skip is not None:
            model = model.offset(skip)
        if limit is not None:
            model = model.limit(limit)
        objs_db = (
            await model.prefetch_related("event", "state")
            .order_by("-created_at")
            .values(
                id="id",
                justification="justification",
                created_date="created_at",
                user_email="user_email",
                event_id="event__id",
                event_name="event__general_name",
                state_id="state__id",
                state_name="state__name",
            )
        )
        return objs_db

    async def get_by_state_id(self, *, state_id: int) -> List[HistoryEventState]:
        objs_db = (
            await self.model.filter(state_id=state_id)
            .all()
            .prefetch_related("event", "state")
            .order_by("-created_at")
            .values(
                id="id",
                justification="justification",
                created_date="created_at",
                event_id="event__id",
                event_name="event__general_name",
                state_id="state__id",
                state_name="state__name",
            )
        )
        return objs_db


crud_history_event_state = CRUDHistoryEventState(model=HistoryEventState)
