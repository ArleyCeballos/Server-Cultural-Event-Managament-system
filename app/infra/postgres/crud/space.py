from app.infra.postgres.crud.base import CRUDBase
from app.infra.postgres.models.space import Space
from app.schemas.space import CreateSpace, UpdateSpace


class CRUDSpace(CRUDBase[Space, CreateSpace, UpdateSpace]):
    async def active(self, *, _id: int, active: bool) -> bool:
        return await self.model.filter(id=_id).update(active=active)


crud_space = CRUDSpace(model=Space)
