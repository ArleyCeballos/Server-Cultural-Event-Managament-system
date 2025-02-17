from typing import List

from fastapi import APIRouter, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from tortoise.transactions import atomic

from app.schemas.accomplishment import CreateAccomplishment
from app.schemas.event_has_responsability import (
    CreateEventHasResponsability,
    EventHasResponsabilityDB,
    UpdateEventHasResponsability,
)
from app.schemas.specific_responsability import CreateSpecificResponsability
from app.services.accomplishment import service_accomplishment
from app.services.event_has_responsability import service_event_has_responsability
from app.services.specific_responsability import service_specific_responsability

router = APIRouter()


@router.get(
    "",
    response_class=JSONResponse,
    response_model=List[EventHasResponsabilityDB],
    status_code=200,
    responses={
        200: {"description": "Events found"},
    },
)
async def get_by_event_id(
    event_id: int = Query(...),
):
    events = await service_event_has_responsability.get_by_event_id(event_id=event_id)
    return events


@router.patch(
    "/{_id}",
    status_code=204,
    responses={
        204: {"description": "Event updated"},
    },
)
async def update(
    update_event_has_responsability: UpdateEventHasResponsability, _id: int = Path(...)
):
    updated = await service_event_has_responsability.update(
        _id=_id, obj_in=update_event_has_responsability
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Event not found")


@router.post(
    "/event/{_id}/specific-responsability",
    response_class=JSONResponse,
    status_code=204,
    responses={
        204: {"description": "Event created"},
    },
)
@atomic()
async def create_specific_responsability(
    create_specific_responsability: CreateSpecificResponsability, _id: int = Path(...)
):
    specific_responsability_id = await service_specific_responsability.create(
        obj_in=create_specific_responsability
    )
    accomplishment_id = await service_accomplishment.create(
        obj_in=CreateAccomplishment()
    )
    await service_event_has_responsability.create(
        obj_in=CreateEventHasResponsability(
            event_id=_id,
            specific_responsability_id=specific_responsability_id,
            accomplishment_id=accomplishment_id,
        )
    )
