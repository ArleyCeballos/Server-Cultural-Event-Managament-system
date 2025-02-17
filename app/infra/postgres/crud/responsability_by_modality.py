from typing import Any, Dict, List, Optional

from app.infra.postgres.crud.base import CRUDBase
from app.infra.postgres.models.responsability_by_modality import ResponsabilityByMode
from app.schemas.responsability_by_modality import (
    CreateResponsabilityByMode,
    UpdateResponsabilityByMode,
)


class CRUDresponsabilityByMode(
    CRUDBase[
        ResponsabilityByMode, CreateResponsabilityByMode, UpdateResponsabilityByMode
    ]
):
    async def get_applies_by_mode_and_space(self, *, mode: int, space: int) -> list:
        model = await self.model.filter(
            applies=True,
            mode_id=mode,
            space_id=space,
            mode__active=True,
            space__active=True,
            responsability__active=True,
        ).all()
        if model is None:
            return []
        return model

    async def get_all(
        self,
        *,
        payload: Dict[str, Any] = {},
        skip: Optional[int],
        limit: Optional[int],
    ) -> List[Dict[str, Any]]:
        query = self.model.filter(**payload) if payload else self.model
        model = query.all().order_by("id")
        if skip is not None:
            model = model.offset(skip)
        if limit is not None:
            model = model.limit(limit)

        model = await model.prefetch_related(
            "mode",
            "responsability",
            "space",
        ).values(
            id="id",
            applies="applies",
            responsability_id="responsability_id",
            space_id="space_id",
            mode_id="mode_id",
            mode_name="mode__name",
            responsability_name="responsability__name",
            space_name="space__name",
        )
        return model

    async def get_by_id(self, *, _id: int) -> Optional[Dict[str, Any]]:
        if _id:
            model = (
                await self.model.filter(id=_id)
                .first()
                .values(
                    "id",
                    "applies",
                    "responsability_id",
                    "space_id",
                    "mode_id",
                    "mode__name",
                    "responsability__name",
                    "space__name",
                )
            )
            if model:
                return model
        return None


crud_responsability_by_mode = CRUDresponsabilityByMode(model=ResponsabilityByMode)
