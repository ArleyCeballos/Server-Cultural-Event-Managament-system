from app.infra.postgres.crud.base import CRUDBase
from app.infra.postgres.models.state import State
from app.schemas.state import CreateState, UpdateState


class CRUDState(CRUDBase[State, CreateState, UpdateState]):
    async def desactivate(self, *, _id: int) -> bool:
        return await self.model.filter(id=_id).update(active=False)


crud_state = CRUDState(model=State)
