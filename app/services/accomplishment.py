from app.infra.postgres.crud.accomplishment import crud_accomplishment
from app.schemas.accomplishment import UpdateAccomplishment
from app.services.base import BaseService


class ServiceAccomplishment(BaseService):
    async def complete_accomplishment(
        self, _id: int, accomplishment: UpdateAccomplishment
    ) -> bool:
        return await crud_accomplishment.complete_accomplishment(
            _id=_id, accomplishment=accomplishment
        )

    async def cancel_accomplishment(self, _id: int) -> bool:
        return await crud_accomplishment.cancel_accomplishment(_id=_id)


service_accomplishment = ServiceAccomplishment(crud=crud_accomplishment)
