from typing import Dict

from app.infra.postgres.crud.event import crud_event
from app.services.base import BaseService


class ServiceEvent(BaseService):
    async def get_status_of_accomplishments(self, _id: int) -> Dict[str, int]:
        return await crud_event.get_status_of_accomplishments(_id)

    async def get_all_status_of_accomplishments_by_date_range(
        self, start_date: str, end_date: str
    ):
        return await crud_event.get_all_status_of_accomplishments_by_date_range(
            start_date, end_date
        )

    async def get_count_by_spaces_and_months(self, year: int):
        return await crud_event.get_count_by_spaces_and_months(year)

    async def get_count_by_modes_and_months(self, year: int):
        return await crud_event.get_count_by_contractual_modes_and_months(year)


service_event = ServiceEvent(crud=crud_event)
