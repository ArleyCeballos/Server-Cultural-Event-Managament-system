from typing import List

from fastapi import APIRouter, HTTPException, Path, Query
from fastapi.responses import JSONResponse

from app.schemas.specific_responsability import (
    CreateSpecificResponsability,
    SpecificResponsabilityDB,
    UpdateSpecificResponsability,
)
from app.services.specific_responsability import service_specific_responsability

router = APIRouter()


@router.get(
    "",
    response_class=JSONResponse,
    response_model=List[SpecificResponsabilityDB],
    status_code=200,
    responses={
        200: {"description": "Specific Responsibilities found"},
    },
)
async def get_all(
    skip: int = Query(0),
    limit: int = Query(10),
):
    responsibilities = await service_specific_responsability.get_all(
        skip=skip, limit=limit
    )
    return responsibilities


@router.post(
    "",
    response_class=JSONResponse,
    status_code=204,
    responses={
        204: {"description": "Specific Responsability created"},
    },
)
async def create(specific_responsability: CreateSpecificResponsability):
    await service_specific_responsability.create(obj_in=specific_responsability)


@router.get(
    "/{_id}",
    response_class=JSONResponse,
    response_model=SpecificResponsabilityDB,
    status_code=200,
    responses={
        200: {"description": "Specific Responsability found"},
        404: {"description": "Specific Responsability not found"},
    },
)
async def by_id(_id: int = Path(...)):
    specific_responsability = await service_specific_responsability.get_by_id(_id=_id)
    if specific_responsability is None:
        raise HTTPException(status_code=404, detail="Specific Responsability not found")
    return specific_responsability


@router.patch(
    "/{_id}",
    response_class=JSONResponse,
    response_model=None,
    status_code=204,
    responses={
        204: {"description": "Specific Responsability updated"},
        404: {"description": "Specific Responsability not found"},
    },
)
async def update(
    update_specific_responsability: UpdateSpecificResponsability, _id: int = Path(...)
):
    updated = await service_specific_responsability.update(
        _id=_id, obj_in=update_specific_responsability
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Specific Responsability not found")


@router.delete(
    "/{_id}",
    response_class=JSONResponse,
    response_model=None,
    status_code=204,
    responses={
        204: {"description": "Specific Responsability deleted"},
        404: {"description": "Specific Responsability not found"},
    },
)
async def delete(_id: int = Path(...)):
    deleted = await service_specific_responsability.delete(_id=_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Specific Responsability not found")
