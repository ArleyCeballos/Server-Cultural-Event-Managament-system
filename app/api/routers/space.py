from asyncio import gather
from typing import List

from fastapi import APIRouter, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from tortoise.transactions import atomic

from app.schemas.responsability_by_modality import (
    CreateResponsabilityByMode,
    UpdateResponsabilityByMode,
)
from app.schemas.space import CreateSpace, SpaceDB, UpdateSpace
from app.services.contractual_mode import service_contractual_mode
from app.services.responsability import service_responsability
from app.services.responsability_by_modality import service_responsability_by_mode
from app.services.space import service_space

router = APIRouter()


@router.get(
    "",
    response_class=JSONResponse,
    response_model=List[SpaceDB],
    status_code=200,
)
async def get_all(active: bool = Query(None)):
    return await service_space.get_all(
        skip=None, limit=None, payload={"active": active} if active else {}
    )


@router.post(
    "",
    response_class=JSONResponse,
    status_code=204,
)
@atomic()
async def create(space: CreateSpace):
    space_id = await service_space.create(obj_in=space)
    contractual_modes, responsabilities = await gather(
        *[
            service_contractual_mode.get_all(),
            service_responsability.get_all(),
        ]
    )
    create_responsability_by_modes = []
    for mode in contractual_modes:
        for responsability in responsabilities:
            create_responsability_by_modes.append(
                CreateResponsabilityByMode(
                    responsability_id=responsability.id,
                    mode_id=mode.id,
                    space_id=space_id,
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
    response_model=SpaceDB,
    status_code=200,
)
async def read(id: int):
    space = await service_space.get_by_id(_id=id)
    if space is None:
        raise HTTPException(status_code=404, detail="Space not found")
    return space


@router.patch(
    "/{id}",
    status_code=204,
)
async def update(id: int, space: UpdateSpace):
    updated = await service_space.update(_id=id, obj_in=space)
    if not updated:
        raise HTTPException(status_code=404, detail="Space not found")


@router.patch(
    "/{_id}/active",
    response_class=JSONResponse,
    response_model=None,
    status_code=204,
    responses={
        204: {"description": "Space updated"},
        404: {"description": "Space not found"},
    },
)
async def active(_id: int = Path(...)):
    updated = await service_space.active(_id=_id, active=True)
    if not updated:
        raise HTTPException(status_code=404, detail="Space not found")


@router.patch(
    "/{_id}/desactive",
    response_class=JSONResponse,
    response_model=None,
    status_code=204,
    responses={
        204: {"description": "Space updated"},
        404: {"description": "Space not found"},
    },
)
@atomic()
async def desactive(_id: int = Path(...)):
    updated = await service_space.active(_id=_id, active=False)
    if not updated:
        raise HTTPException(status_code=404, detail="Space not found")
    await service_responsability_by_mode.update_by_filter(
        payload={"space": _id},
        obj_in=UpdateResponsabilityByMode(applies=False),
    )


@router.delete("/{id}", status_code=204, include_in_schema=False)
async def delete(id: int):
    deleted = await service_space.delete(_id=id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Space not found")
