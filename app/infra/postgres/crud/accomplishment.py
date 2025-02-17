from datetime import datetime

from app.infra.postgres.crud.base import CRUDBase
from app.infra.postgres.models.accomplishment import Accomplishment
from app.schemas.accomplishment import CreateAccomplishment, UpdateAccomplishment


class CRUDAccomplishment(
    CRUDBase[
        Accomplishment,
        CreateAccomplishment,
        UpdateAccomplishment,
    ]
):
    async def complete_accomplishment(
        self, _id: int, accomplishment: UpdateAccomplishment
    ) -> bool:
        payload = accomplishment.model_dump(exclude_unset=True)
        payload["check"] = True
        payload["compliment_date"] = datetime.now()
        await self.model.filter(id=_id).update(**payload)
        return True

    async def cancel_accomplishment(self, _id: int) -> bool:
        payload = {
            "check": False,
            "compliment_date": None,
            "file_url": None,
            "text": None,
        }
        await self.model.filter(id=_id).update(**payload)
        return True


crud_accomplishment = CRUDAccomplishment(model=Accomplishment)
