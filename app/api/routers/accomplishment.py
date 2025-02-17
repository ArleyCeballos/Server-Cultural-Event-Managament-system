from typing import List

from fastapi import APIRouter, HTTPException, Path, Query, UploadFile
from fastapi.responses import JSONResponse
from tortoise.transactions import atomic

from app.schemas.accomplishment import AccomplishmentDB, UpdateAccomplishment
from app.services.accomplishment import service_accomplishment
from app.services.bucket import service_bucket

router = APIRouter()


@router.get(
    "",
    response_class=JSONResponse,
    response_model=List[AccomplishmentDB],
    status_code=200,
    responses={
        200: {"description": "Accomplishments found"},
    },
)
async def get_all(
    skip: int = Query(0),
    limit: int = Query(10),
):
    events = await service_accomplishment.get_all(skip=skip, limit=limit)
    return events


@router.get(
    "/{_id}",
    response_class=JSONResponse,
    response_model=AccomplishmentDB,
    status_code=200,
    responses={
        200: {"description": "Accomplishment found"},
        404: {"description": "Accomplishment not found"},
    },
)
async def get_by_id(_id: int = Path(...)):
    event = await service_accomplishment.get_by_id(_id=_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.patch(
    "/{_id}",
    response_class=JSONResponse,
    response_model=None,
    status_code=204,
    responses={
        204: {"description": "Accomplishment completed"},
        404: {"description": "Accomplishment not found"},
    },
)
async def complete(update_accomplishment: UpdateAccomplishment, _id: int = Path(...)):
    updated = await service_accomplishment.complete_accomplishment(
        _id=_id, accomplishment=update_accomplishment
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Accomplishment not found")


@router.patch(
    "/{_id}/cancel",
    response_class=JSONResponse,
    response_model=None,
    status_code=204,
    responses={
        204: {"description": "Accomplishment canceled"},
        404: {"description": "Accomplishment not found"},
    },
)
async def cancel(_id: int = Path(...)):
    canceled = await service_accomplishment.cancel_accomplishment(_id=_id)
    if not canceled:
        raise HTTPException(status_code=404, detail="Accomplishment not found")


@router.delete(
    "/{_id}",
    response_class=JSONResponse,
    response_model=None,
    status_code=204,
    responses={
        204: {"description": "Accomplishment deleted"},
        404: {"description": "Accomplishment not found"},
    },
)
async def delete(_id: int = Path(...)):
    deleted = await service_accomplishment.delete(_id=_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Accomplishment not found")


@router.post(
    "{_id}/updload-file",
    response_class=JSONResponse,
    response_model=None,
    status_code=204,
    responses={
        204: {"description": "File uploaded"},
        404: {"description": "Accomplishment not found"},
    },
)
@atomic()
async def upload_file(file: UploadFile, _id: int = Path(...)):
    try:
        contents = await file.read()
        filename = file.filename
        file_url = f"accomplishment/{_id}/{filename}"
        await service_accomplishment.update(
            _id=_id,
            obj_in=UpdateAccomplishment(file_url=file_url),
        )
        success = await service_bucket.upload_blob_async(
            file_url, contents, file.content_type
        )
        if success:
            return {"message": "File uploaded successfully."}
        else:
            return {"message": "Failed to upload the file."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
