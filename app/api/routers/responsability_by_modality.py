from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.responses import JSONResponse

from app.schemas.responsability_by_modality import (
    CreateResponsabilityByMode,
    ResponsabilityByModeDB,
    SearchresponsabilityByMode,
    UpdateResponsabilityByMode,
)
from app.services.responsability_by_modality import service_responsability_by_mode

router = APIRouter()


@router.get(
    "",
    response_class=JSONResponse,
    response_model=List[ResponsabilityByModeDB],
    status_code=200,
    responses={
        200: {"description": "responsibilities by mode found"},
    },
)
async def get_all(
    search: SearchresponsabilityByMode = Depends(SearchresponsabilityByMode),
):
    responsibilities = await service_responsability_by_mode.get_all(
        skip=None,
        limit=None,
        payload={
            **search.model_dump(exclude_none=True),
            "mode__active": True,
            "space__active": True,
            "responsability__active": True,
        },
    )
    return responsibilities


@router.post(
    "",
    response_class=JSONResponse,
    response_model=ResponsabilityByModeDB,
    status_code=201,
    responses={
        201: {"description": "responsability by mode created"},
    },
)
async def create(new_responsability: CreateResponsabilityByMode):
    responsability = await service_responsability_by_mode.create(
        obj_in=new_responsability
    )
    return responsability


@router.get(
    "/{_id}",
    response_class=JSONResponse,
    response_model=ResponsabilityByModeDB,
    status_code=200,
    responses={
        200: {"description": "responsability by mode found"},
        404: {"description": "responsability by mode not found"},
    },
)
async def by_id(_id: int = Path(...)):
    responsability = await service_responsability_by_mode.get_by_id(_id=_id)
    if responsability is None:
        raise HTTPException(status_code=404, detail="responsability by mode not found")
    return responsability


@router.patch(
    "/{_id}",
    response_class=JSONResponse,
    response_model=None,
    status_code=204,
    responses={
        204: {"description": "responsability by mode updated"},
        404: {"description": "responsability by mode not found"},
    },
)
async def update(
    update_responsability: UpdateResponsabilityByMode, _id: int = Path(...)
):
    await service_responsability_by_mode.update(_id=_id, obj_in=update_responsability)


@router.delete(
    "/{_id}",
    response_class=JSONResponse,
    response_model=None,
    status_code=204,
    responses={
        204: {"description": "responsability by mode deleted"},
    },
)
async def delete(_id: int = Path(...)):
    responsability = await service_responsability_by_mode.delete(_id=_id)
    if responsability == 0:
        raise HTTPException(status_code=404, detail="responsability by mode not found")
