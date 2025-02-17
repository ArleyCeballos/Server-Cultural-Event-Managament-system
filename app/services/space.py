from app.infra.postgres.crud.space import crud_space
from app.services.base import BaseService


class ServiceSpace(BaseService):
    async def active(self, *, _id: int, active: bool) -> bool:
        return await crud_space.active(_id=_id, active=active)


service_space = ServiceSpace(crud=crud_space)
