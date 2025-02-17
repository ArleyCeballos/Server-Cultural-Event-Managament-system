from asyncio import gather
from typing import List

from fastapi import APIRouter, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from tortoise.transactions import atomic

from app.schemas.contractual_mode import (
    ContractualModeDB,
    CreateContractualMode,
    UpdateContractualMode,
)
from app.schemas.responsability_by_modality import (
    CreateResponsabilityByMode,
    UpdateResponsabilityByMode,
)
from app.services.contractual_mode import service_contractual_mode
from app.services.responsability import service_responsability
from app.services.responsability_by_modality import service_responsability_by_mode
from app.services.space import service_space

router = APIRouter()


@router.get(
    "",
    response_class=JSONResponse,
    response_model=List[ContractualModeDB],
    status_code=200,
)
async def get_all(active: bool = Query(None)):
    return await service_contractual_mode.get_all(
        skip=None, limit=None, payload={"active": active} if active else {}
    )


@router.post(
    "",
    response_class=JSONResponse,
    status_code=204,
)
@atomic()
async def create(mode: CreateContractualMode):
    mode_id = await service_contractual_mode.create(obj_in=mode)
    spaces, responsabilities = await gather(
        *[
            service_space.get_all(),
            service_responsability.get_all(),
        ]
    )
    create_responsability_by_modes = []
    for space in spaces:
        for responsability in responsabilities:
            create_responsability_by_modes.append(
                CreateResponsabilityByMode(
                    responsability_id=responsability.id,
                    mode_id=mode_id,
                    space_id=space.id,
                    applies=False,
                )
            )
    tasks = [
        service_responsability_by_mode.create(obj_in=mode)
        for mode in create_responsability_by_modes
    ]
    await gather(*tasks)


@router.get(
    "/{id}",
    response_class=JSONResponse,
    response_model=ContractualModeDB,
    status_code=200,
)
async def read(id: int):
    mode = await service_contractual_mode.get_by_id(_id=id)
    if mode is None:
        raise HTTPException(status_code=404, detail="Mode not found")
    return mode


@router.patch(
    "/{id}",
    status_code=204,
)
async def update(id: int, mode: UpdateContractualMode):
    updated = await service_contractual_mode.update(_id=id, obj_in=mode)
    if not updated:
        raise HTTPException(status_code=404, detail="Mode not found")


@router.patch(
    "/{_id}/active",
    response_class=JSONResponse,
    response_model=None,
    status_code=204,
    responses={
        204: {"description": "Mode updated"},
        404: {"description": "Mode not found"},
    },
)
async def active(_id: int = Path(...)):
    updated = await service_contractual_mode.active(_id=_id, active=True)
    if not updated:
        raise HTTPException(status_code=404, detail="Mode not found")


@router.patch(
    "/{_id}/desactive",
    response_class=JSONResponse,
    response_model=None,
    status_code=204,
    responses={
        204: {"description": "Mode updated"},
        404: {"description": "Mode not found"},
    },
)
@atomic()
async def desactive(_id: int = Path(...)):
    updated = await service_contractual_mode.active(_id=_id, active=False)
    if not updated:
        raise HTTPException(status_code=404, detail="Mode not found")
    await service_responsability_by_mode.update_by_filter(
        payload={"mode": _id},
        obj_in=UpdateResponsabilityByMode(applies=False),
    )


@router.delete("/{id}", status_code=204, include_in_schema=False)
async def delete(id: int):
    deleted = await service_contractual_mode.delete(_id=id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Mode not found")
