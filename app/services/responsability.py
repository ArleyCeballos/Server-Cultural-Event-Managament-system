from app.infra.postgres.crud.responsability import crud_responsability
from app.services.base import BaseService


class Serviceresponsability(BaseService):
    async def active(self, *, _id: int, active: bool) -> bool:
        return await crud_responsability.active(_id=_id, active=active)


service_responsability = Serviceresponsability(crud=crud_responsability)
