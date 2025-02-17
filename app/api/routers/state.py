from typing import List

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from app.schemas.state import CreateState, StateDB, UpdateState
from app.services.state import service_state

router = APIRouter()


@router.get(
    "",
    response_class=JSONResponse,
    response_model=List[StateDB],
    status_code=200,
)
async def get_all(active: bool = Query(None)):
    return await service_state.get_all(
        skip=None, limit=None, payload={"active": active} if active else {}
    )


@router.post(
    "",
    response_class=JSONResponse,
    status_code=204,
)
async def create(state: CreateState):
    await service_state.create(obj_in=state)


@router.get(
    "/{id}",
    response_class=JSONResponse,
    response_model=StateDB,
    status_code=200,
)
async def read(id: int):
    state = await service_state.get_by_id(_id=id)
    if state is None:
        raise HTTPException(status_code=404, detail="State not found")
    return state


@router.patch(
    "/{_id}",
    status_code=204,
)
async def update(_id: int, state: UpdateState):
    updated = await service_state.update(_id=_id, obj_in=state)
    if not updated:
        raise HTTPException(status_code=404, detail="State not found")


@router.patch(
    "/{_id}/desactivate",
    status_code=204,
)
async def desactivate(_id: int):
    updated = await service_state.desactivate(_id=_id)
    if not updated:
        raise HTTPException(status_code=404, detail="State not found")


@router.delete("/{id}", status_code=204, include_in_schema=False)
async def delete(id: int):
    deleted = await service_state.delete(_id=id)
    if not deleted:
        raise HTTPException(status_code=404, detail="State not found")
