from app.infra.postgres.crud.base import CRUDBase
from app.infra.postgres.models.responsability import Responsability
from app.schemas.responsability import CreateResponsability, UpdateResponsability


class CRUDresponsability(
    CRUDBase[Responsability, CreateResponsability, UpdateResponsability]
):
    async def active(self, *, _id: int, active: bool) -> bool:
        return await self.model.filter(id=_id).update(active=active)


crud_responsability = CRUDresponsability(model=Responsability)
