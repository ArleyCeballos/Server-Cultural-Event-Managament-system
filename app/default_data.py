import json

from app.api.routers.event import create_event
from app.schemas.contractual_mode import CreateContractualMode
from app.schemas.event import CreateEvent
from app.schemas.eventstate import CreateEventState
from app.schemas.responsability import CreateResponsability
from app.schemas.responsability_by_modality import CreateResponsabilityByMode
from app.schemas.space import CreateSpace
from app.schemas.state import CreateState
from app.services.contractual_mode import service_contractual_mode
from app.services.event import service_event
from app.services.eventstate import service_event_state
from app.services.responsability import service_responsability
from app.services.responsability_by_modality import service_responsability_by_mode
from app.services.space import service_space
from app.services.state import service_state


async def create_default_data():
    if len(await service_contractual_mode.get_all(skip=0, limit=10)) == 0:
        with open("default_data/contractual_mode.json") as file:
            data = json.load(file)
            if isinstance(data, list):
                print("CREATING CONTRACTUAL MODES")
                for obj in data:
                    obj_in = CreateContractualMode(**obj)
                    await service_contractual_mode.create(obj_in=obj_in)
    if len(await service_space.get_all(skip=0, limit=10)) == 0:
        with open("default_data/space.json") as file:
            data = json.load(file)
            if isinstance(data, list):
                print("CREATING SPACES")
                for obj in data:
                    obj_in = CreateSpace(**obj)
                    await service_space.create(obj_in=obj_in)
    if len(await service_responsability.get_all(skip=0, limit=10)) == 0:
        with open("default_data/responsability.json") as file:
            data = json.load(file)
            if isinstance(data, list):
                print("CREATING RESPONSABILITIES")
                for obj in data:
                    obj_in = CreateResponsability(**obj)
                    await service_responsability.create(obj_in=obj_in)
    if len(await service_contractual_mode.get_all(skip=0, limit=10)) == 0:
        with open("default_data/contractual_mode.json") as file:
            data = json.load(file)
            if isinstance(data, list):
                print("CREATING CONTRACTUALMODES")
                for obj in data:
                    obj_in = CreateContractualMode(**obj)
                    await service_contractual_mode.create(obj_in=obj_in)
    if len(await service_responsability_by_mode.get_all(skip=0, limit=10)) == 0:
        with open("default_data/responsability_by_modality.json") as file:
            data = json.load(file)
            if isinstance(data, list):
                print("CREATING RESPONSABILITIES BY MODALITIES")
                for obj in data:
                    obj_in = CreateResponsabilityByMode(**obj)
                    await service_responsability_by_mode.create(obj_in=obj_in)
    if len(await service_state.get_all(skip=0, limit=10)) == 0:
        with open("default_data/state.json") as file:
            data = json.load(file)
            if isinstance(data, list):
                print("CREATING STATES")
                for obj in data:
                    obj_in = CreateState(**obj)
                    await service_state.create(obj_in=obj_in)
    if len(await service_event.get_all(skip=0, limit=10)) == 0:
        with open("default_data/event.json") as file:
            data = json.load(file)
            if isinstance(data, list):
                print("CREATING EVENTS")
                for obj in data:
                    obj_in = CreateEvent(**obj)
                    await create_event(event=obj_in)
    if len(await service_event_state.get_all(skip=0, limit=10)) == 0:
        with open("default_data/eventstate.json") as file:
            data = json.load(file)
            if isinstance(data, list):
                print("CREATING EVENT STATES")
                for obj in data:
                    obj_in = CreateEventState(**obj)
                    await service_event_state.create(obj_in=obj_in)
