from typing import List

from app.infra.postgres.crud.responsability_by_modality import (
    crud_responsability_by_mode,
)
from app.services.base import BaseService


class ServiceresponsabilityByMode(BaseService):
    async def get_applies_by_mode_and_space(self, *, mode: int, space: int) -> List:
        return await crud_responsability_by_mode.get_applies_by_mode_and_space(
            mode=mode, space=space
        )


service_responsability_by_mode = ServiceresponsabilityByMode(
    crud=crud_responsability_by_mode
)
