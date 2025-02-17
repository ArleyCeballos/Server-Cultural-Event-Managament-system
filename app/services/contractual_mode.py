from app.infra.postgres.crud.contractual_mode import crud_contractual_mode
from app.services.base import BaseService


class ServiceContractualMode(BaseService):
    async def active(self, *, _id: int, active: bool) -> bool:
        return await crud_contractual_mode.active(_id=_id, active=active)


service_contractual_mode = ServiceContractualMode(crud=crud_contractual_mode)
