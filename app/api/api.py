from fastapi import APIRouter

from app.api.routers import (
    accomplishment,
    bucket,
    close_event,
    contractual_mode,
    event,
    event_has_responsability,
    eventstate,
    historyeventstate,
    responsability,
    responsability_by_modality,
    root,
    space,
    specific_responsability,
    state,
)

api_router = APIRouter()
api_router.include_router(root.router, prefix="/health-check", tags=["Health Check"])
api_router.include_router(
    responsability_by_modality.router,
    prefix="/responsability-by-mode",
    tags=["Responsability By Mode"],
)
api_router.include_router(
    responsability.router, prefix="/responsability", tags=["Responsability"]
)
api_router.include_router(
    contractual_mode.router, prefix="/contractual-modes", tags=["Contractual Modes"]
)
api_router.include_router(space.router, prefix="/spaces", tags=["Spaces"])
api_router.include_router(event.router, prefix="/events", tags=["Events"])
api_router.include_router(bucket.router, prefix="/bucket", tags=["Bucket"])
api_router.include_router(eventstate.router, prefix="/eventstate", tags=["Event State"])
api_router.include_router(
    historyeventstate.router, prefix="/historyeventstate", tags=["History Event State"]
)
api_router.include_router(
    event_has_responsability.router,
    prefix="/event-has-responsability",
    tags=["Event Has Responsability"],
)
api_router.include_router(
    accomplishment.router, prefix="/accomplishments", tags=["Accomplishments"]
)

api_router.include_router(
    specific_responsability.router,
    prefix="/specific-responsability",
    tags=["Specific Responsability"],
)
api_router.include_router(state.router, prefix="/states", tags=["States"])
api_router.include_router(
    close_event.router, prefix="/close-event", tags=["Close Event"]
)
