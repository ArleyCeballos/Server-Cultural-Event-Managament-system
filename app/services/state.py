from app.infra.postgres.crud.state import crud_state
from app.services.base import BaseService


class ServiceState(BaseService):
    async def desactivate(self, *, _id: int) -> bool:
        return await self._crud.desactivate(_id=_id)


service_state = ServiceState(crud=crud_state)
