from asyncio import gather
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Path, Query, UploadFile
from fastapi.responses import JSONResponse
from tortoise.transactions import atomic

from app.schemas.accomplishment import CreateAccomplishment
from app.schemas.event import CreateEvent, EventDB, StatusAccomplishment, UpdateEvent
from app.schemas.event_has_responsability import CreateEventHasResponsability
from app.services.accomplishment import service_accomplishment
from app.services.bucket import service_bucket
from app.services.event import service_event
from app.services.event_has_responsability import service_event_has_responsability
from app.services.responsability_by_modality import service_responsability_by_mode

router = APIRouter()


@router.get(
    "",
    response_class=JSONResponse,
    response_model=List[EventDB],
    status_code=200,
    responses={
        200: {"description": "Events found"},
    },
)
async def get_all(
    skip: int = Query(0),
    limit: int = Query(10),
):
    events = await service_event.get_all(skip=skip, limit=limit)
    return events


@router.get(
    "/all/status",
    response_class=JSONResponse,
    response_model=StatusAccomplishment,
    status_code=200,
    responses={
        200: {"description": "Event found"},
        404: {"description": "Event not found"},
    },
)
async def get_all_status_of_accomplishments_by_date_range(
    start_date: str, end_date: str
):
    return await service_event.get_all_status_of_accomplishments_by_date_range(
        start_date, end_date
    )


@router.get(
    "/{_id}/status",
    response_class=JSONResponse,
    response_model=StatusAccomplishment,
    status_code=200,
    responses={
        200: {"description": "Event found"},
    },
)
async def get_status_of_accomplishments(_id: int):
    return await service_event.get_status_of_accomplishments(_id)


@router.get(
    "/count/spaces",
    response_class=JSONResponse,
    status_code=200,
    responses={
        200: {"description": "Event found"},
    },
)
async def get_count_by_spaces_and_months(year: Optional[int] = 2024):
    return await service_event.get_count_by_spaces_and_months(year)


@router.get(
    "/count/modes",
    response_class=JSONResponse,
    status_code=200,
    responses={
        200: {"description": "Event found"},
    },
)
async def get_count_by_modes_and_months(year: Optional[int] = 2024):
    return await service_event.get_count_by_modes_and_months(year)


@router.post(
    "",
    response_class=JSONResponse,
    status_code=201,
    responses={
        201: {"description": "Event created"},
    },
)
@atomic()
async def create_event(event: CreateEvent):
    event_id = await service_event.create(obj_in=event)
    responsability_by_modes = (
        await service_responsability_by_mode.get_applies_by_mode_and_space(
            mode=event.event_type_id,
            space=event.place_id,
        )
    )
    tasks = []

    async def create_event_has_responsability(event_id, responsability_by_mode_id):
        accomplishment_id = await service_accomplishment.create(
            obj_in=CreateAccomplishment()
        )
        await service_event_has_responsability.create(
            obj_in=CreateEventHasResponsability(
                event_id=event_id,
                responsability_by_mode_id=responsability_by_mode_id,
                accomplishment_id=accomplishment_id,
            )
        )

    for responsability_by_mode in responsability_by_modes:
        tasks.append(
            create_event_has_responsability(
                event_id=event_id, responsability_by_mode_id=responsability_by_mode.id
            )
        )
    # tasks.extend(
    #     [
    #         service_event_state.create(
    #             obj_in=CreateEventState(
    #                 event_id=event_id, state_id=1, justification="Evento Creado"
    #             )
    #         ),
    #         service_history_event_state.create(
    #             obj_in=CreateHistoryEventState(
    #                 event_id=event_id,
    #                 justification="Evento Creado",
    #                 state_id=1,
    #             )
    #         ),
    #     ]
    # )
    await gather(*tasks)
    return JSONResponse(status_code=201, content={"id": event_id})


@router.get(
    "/{_id}",
    response_class=JSONResponse,
    response_model=EventDB,
    status_code=200,
    responses={
        200: {"description": "Event found"},
        404: {"description": "Event not found"},
    },
)
async def get_event_by_id(_id: int = Path(...)):
    event = await service_event.get_by_id(_id=_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.patch(
    "/{_id}",
    response_class=JSONResponse,
    response_model=None,
    status_code=204,
    responses={
        204: {"description": "Event updated"},
        404: {"description": "Event not found"},
    },
)
async def update_event(update_event: UpdateEvent, _id: int = Path(...)):
    updated = await service_event.update(_id=_id, obj_in=update_event)
    if not updated:
        raise HTTPException(status_code=404, detail="Event not found")


@router.delete(
    "/{_id}",
    response_class=JSONResponse,
    response_model=None,
    status_code=204,
    responses={
        204: {"description": "Event deleted"},
        404: {"description": "Event not found"},
    },
)
async def delete_event(_id: int = Path(...)):
    deleted = await service_event.delete(_id=_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Event not found")


@router.post(
    "{_id}/updload-file",
    response_class=JSONResponse,
    response_model=None,
    status_code=204,
    responses={
        204: {"description": "File uploaded"},
        404: {"description": "Event not found"},
    },
)
async def upload_file(file: UploadFile, _id: int = Path(...)):
    try:
        contents = await file.read()
        filename = file.filename
        success = await service_bucket.upload_blob_async(
            f"event-file/{_id}/{filename}", contents, file.content_type
        )
        if success:
            return {"message": "File uploaded successfully."}
        else:
            return {"message": "Failed to upload the file."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
