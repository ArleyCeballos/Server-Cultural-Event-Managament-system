from typing import List

from fastapi import APIRouter, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from tortoise.transactions import atomic

from app.schemas.eventstate import CreateEventState, EventStateDB, UpdateEventState
from app.services.eventstate import service_event_state

router = APIRouter()


@router.get(
    "",
    response_class=JSONResponse,
    response_model=List[EventStateDB],
    status_code=200,
    responses={
        200: {"description": "Event states found"},
    },
)
async def get_all(
    skip: int = Query(0),
    limit: int = Query(10),
):
    event_states = await service_event_state.get_all(skip=skip, limit=limit)
    return event_states


@router.post(
    "",
    response_class=JSONResponse,
    status_code=204,
    responses={
        204: {"description": "Event state created"},
    },
)
async def create(new_event_state: CreateEventState):
    await service_event_state.create(obj_in=new_event_state)


@router.get(
    "/{_id}",
    response_class=JSONResponse,
    response_model=EventStateDB,
    status_code=200,
    responses={
        200: {"description": "Event state found"},
        404: {"description": "Event state not found"},
    },
)
async def get_by_id(_id: int = Path(...)):
    event_state = await service_event_state.get_by_id(_id=_id)
    if event_state is None:
        raise HTTPException(status_code=404, detail="Event state not found")
    return event_state


@router.patch(
    "/{_id}",
    response_class=JSONResponse,
    status_code=204,
    responses={
        204: {"description": "Event state updated"},
        404: {"description": "Event state not found"},
    },
)
@atomic()
async def update(update_event_state: UpdateEventState, _id: int = Path(...)):
    # old_event_state_obj = await service_event_state.get_by_id(_id=_id)
    # old_event_state = EventStateDB.model_validate(old_event_state_obj)
    # if old_event_state is None:
    #     raise HTTPException(status_code=404, detail="Event state not found")
    result = await service_event_state.update(_id=_id, obj_in=update_event_state)
    if not result:
        raise HTTPException(status_code=404, detail="Event state not found")
    # else:
    #     await service_history_event_state.create(
    #         obj_in=CreateHistoryEventState(
    #             event_id=old_event_state.event_id,
    #             state_id=update_event_state.state_id,
    #             justification=old_event_state.justification,
    #         )
    #     )


@router.delete(
    "/{_id}",
    response_class=JSONResponse,
    status_code=204,
    responses={
        204: {"description": "Event state deleted"},
        404: {"description": "Event state not found"},
    },
)
async def delete(_id: int = Path(...), include_in_schema=False):
    result = await service_event_state.delete(_id=_id)
    if result == 0:
        raise HTTPException(status_code=404, detail="Event state not found")
