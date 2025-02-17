from typing import Any, Dict, List

from app.infra.postgres.crud.base import CRUDBase
from app.infra.postgres.models.event_has_responsability import EventHasResponsability
from app.schemas.event_has_responsability import (
    CreateEventHasResponsability,
    UpdateEventHasResponsability,
)


class CRUDEventHasResponsability(
    CRUDBase[
        EventHasResponsability,
        CreateEventHasResponsability,
        UpdateEventHasResponsability,
    ]
):
    async def get_by_event_id(self, *, event_id: int) -> List[Dict[str, Any]]:
        query = self.model.filter(event_id=event_id)
        model = (
            await query.all()
            .prefetch_related(
                "event",
                "accomplishment",
                "responsability_by_mode",
                "specific_responsability",
            )
            .values(
                id="id",
                event_id="event__id",
                event_name="event__general_name",
                responsability_by_mode_id="responsability_by_mode__id",
                responsability_by_mode_name="responsability_by_mode__responsability__name",
                specific_responsability_id="specific_responsability__id",
                specific_responsability_name="specific_responsability__name",
                accomplishment_id="accomplishment__id",
                accomplishment_creation_date="accomplishment__date",
                accomplishment_compliment_date="accomplishment__compliment_date",
                accomplishment_status="accomplishment__check",
            )
        )
        return model


crud_event_has_responsability = CRUDEventHasResponsability(model=EventHasResponsability)
