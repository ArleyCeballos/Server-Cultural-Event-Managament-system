from asyncio import gather
from typing import List

from fastapi import APIRouter, HTTPException, Path, Query, UploadFile
from fastapi.responses import JSONResponse
from tortoise.transactions import atomic

from app.schemas.responsability import (
    CreateResponsability,
    ResponsabilityDB,
    UpdateResponsability,
)
from app.schemas.responsability_by_modality import (
    CreateResponsabilityByMode,
    UpdateResponsabilityByMode,
)
from app.services.bucket import service_bucket
from app.services.contractual_mode import service_contractual_mode
from app.services.responsability import service_responsability
from app.services.responsability_by_modality import service_responsability_by_mode
from app.services.space import service_space

router = APIRouter()


@router.get(
    "",
    response_class=JSONResponse,
    response_model=List[ResponsabilityDB],
    status_code=200,
    responses={
        200: {"description": "Responsibilities found"},
    },
)
async def get_all(active: bool = Query(None)):
    responsibilities = await service_responsability.get_all(
        skip=None, limit=None, payload={"active": active} if active else {}
    )
    return responsibilities


@router.post(
    "",
    response_class=JSONResponse,
    status_code=204,
    responses={
        204: {"description": "responsability created"},
    },
)
@atomic()
async def create(responsability: CreateResponsability):
    responsability_id = await service_responsability.create(obj_in=responsability)
    contractual_modes, spaces = await gather(
        *[
            service_contractual_mode.get_all(),
            service_space.get_all(),
        ]
    )
    create_responsability_by_modes = []
    for mode in contractual_modes:
        for space in spaces:
            create_responsability_by_modes.append(
                CreateResponsabilityByMode(
                    responsability_id=responsability_id,
                    mode_id=mode.id,
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
    "/{_id}",
    response_class=JSONResponse,
    response_model=ResponsabilityDB,
    status_code=200,
    responses={
        200: {"description": "responsability found"},
        404: {"description": "responsability not found"},
    },
)
async def by_id(_id: int = Path(...)):
    responsability = await service_responsability.get_by_id(_id=_id)
    if responsability is None:
        raise HTTPException(status_code=404, detail="responsability not found")
    return responsability


@router.patch(
    "/{_id}",
    response_class=JSONResponse,
    response_model=None,
    status_code=204,
    responses={
        204: {"description": "responsability updated"},
        404: {"description": "responsability not found"},
    },
)
async def update(update_responsability: UpdateResponsability, _id: int = Path(...)):
    updated = await service_responsability.update(_id=_id, obj_in=update_responsability)
    if not updated:
        raise HTTPException(status_code=404, detail="responsability not found")


@router.patch(
    "/{_id}/active",
    response_class=JSONResponse,
    response_model=None,
    status_code=204,
    responses={
        204: {"description": "responsability updated"},
        404: {"description": "responsability not found"},
    },
)
async def active(_id: int = Path(...)):
    updated = await service_responsability.active(_id=_id, active=True)
    if not updated:
        raise HTTPException(status_code=404, detail="responsability not found")


@router.patch(
    "/{_id}/desactive",
    response_class=JSONResponse,
    response_model=None,
    status_code=204,
    responses={
        204: {"description": "responsability updated"},
        404: {"description": "responsability not found"},
    },
)
@atomic()
async def desactive(_id: int = Path(...)):
    updated = await service_responsability.active(_id=_id, active=False)
    if not updated:
        raise HTTPException(status_code=404, detail="responsability not found")
    await service_responsability_by_mode.update_by_filter(
        payload={"responsability": _id},
        obj_in=UpdateResponsabilityByMode(applies=False),
    )


@router.delete(
    "/{_id}",
    response_class=JSONResponse,
    response_model=None,
    status_code=204,
    responses={
        204: {"description": "responsability deleted"},
        404: {"description": "responsability not found"},
    },
)
async def delete(_id: int = Path(...)):
    deleted = await service_responsability.delete(_id=_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="responsability not found")


@router.post(
    "{_id}/updload-file",
    response_class=JSONResponse,
    response_model=None,
    status_code=204,
    responses={
        204: {"description": "File uploaded"},
        404: {"description": "responsability not found"},
    },
)
async def upload_file(file: UploadFile, _id: int = Path(...)):
    try:
        contents = await file.read()
        filename = file.filename
        success = await service_bucket.upload_blob_async(
            f"template/{_id}/{filename}", contents, file.content_type
        )
        if success:
            return {"message": "File uploaded successfully."}
        else:
            return {"message": "Failed to upload the file."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
