from typing import List

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from app.schemas.historyeventstate import CreateHistoryEventState, HistoriyEventRelation
from app.services.historyeventstate import service_history_event_state

router = APIRouter()


@router.get(
    "",
    response_class=JSONResponse,
    response_model=List[HistoriyEventRelation],
    status_code=200,
)
async def get_all(skip: int = Query(0), limit: int = Query(10)):
    return await service_history_event_state.get_all(skip=skip, limit=limit)


@router.get(
    "/event/{event_id}",
    response_class=JSONResponse,
    response_model=List[HistoriyEventRelation],
    status_code=200,
)
async def get_by_event_id(event_id: int):
    return await service_history_event_state.get_by_event_id(event_id=event_id)


@router.get(
    "/state/{state_id}",
    response_class=JSONResponse,
    response_model=List[HistoriyEventRelation],
    status_code=200,
)
async def get_by_state_id(state_id: int):
    return await service_history_event_state.get_by_state_id(state_id=state_id)


@router.post(
    "",
    response_class=JSONResponse,
    status_code=204,
)
async def create(historyeventstate: CreateHistoryEventState):
    await service_history_event_state.create(obj_in=historyeventstate)
