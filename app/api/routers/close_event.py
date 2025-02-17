from typing import List

from fastapi import APIRouter, HTTPException, Path, Query, UploadFile
from fastapi.responses import JSONResponse

from app.schemas.close_event import CloseEventDB, CreateCloseEvent
from app.services.bucket import service_bucket
from app.services.close_event import service_close_event
from app.services.event import service_event

router = APIRouter()


@router.get(
    "",
    response_class=JSONResponse,
    response_model=List[CloseEventDB],
    status_code=200,
    responses={
        200: {"description": "CloseEvents found"},
    },
)
async def get_all(
    skip: int = Query(0),
    limit: int = Query(10),
):
    events = await service_close_event.get_all(skip=skip, limit=limit)
    return events


@router.post(
    "",
    response_class=JSONResponse,
    status_code=201,
    responses={
        201: {"description": "CloseEvent created"},
    },
)
async def create(
    close_event: CreateCloseEvent,
):
    status_of_accomplishments = await service_event.get_status_of_accomplishments(
        close_event.event_id
    )
    if status_of_accomplishments["total"] == 0:
        raise HTTPException(
            status_code=400, detail="Event has a problem with accomplishments"
        )
    if status_of_accomplishments["not_complete"] > 0:
        raise HTTPException(status_code=400, detail="Event not finished")
    close_event_id = await service_close_event.create(obj_in=close_event)
    return JSONResponse(status_code=201, content={"id": close_event_id})


@router.post(
    "/files/{event_id}",
    response_class=JSONResponse,
    status_code=201,
    responses={
        201: {"description": "CloseEvent created"},
    },
)
async def upload_file(file: UploadFile, event_id: int = Path(...)):
    try:
        contents = await file.read()
        filename = file.filename
        success = await service_bucket.upload_blob_async(
            f"close_event/{event_id}/{filename}", contents, file.content_type
        )
        if success:
            return {"message": "File uploaded successfully."}
        else:
            return {"message": "Failed to upload the file."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/{_id}",
    response_class=JSONResponse,
    response_model=CloseEventDB,
    status_code=200,
    responses={
        200: {"description": "CloseEvent found"},
        404: {"description": "CloseEvent not found"},
    },
)
async def get_event_by_id(_id: int = Path(...)):
    event = await service_close_event.get_by_id(_id=_id)
    if event is None:
        raise HTTPException(status_code=404, detail="CloseEvents not found")
    return event
