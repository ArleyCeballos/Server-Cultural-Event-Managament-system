# crud_event.py
import json
from typing import Dict, List

from tortoise.transactions import in_transaction

from app.infra.postgres.crud.base import CRUDBase
from app.infra.postgres.models.event import Event
from app.schemas.event import CreateEvent, UpdateEvent

TranslateMonth: Dict[str, str] = {
    "January": "Enero",
    "February": "Febrero",
    "March": "Marzo",
    "April": "Abril",
    "May": "Mayo",
    "June": "Junio",
    "July": "Julio",
    "August": "Agosto",
    "September": "Septiembre",
    "October": "Octubre",
    "November": "Noviembre",
    "December": "Diciembre",
}


class CRUDEvent(CRUDBase[Event, CreateEvent, UpdateEvent]):
    async def get_status_of_accomplishments(self, _id: int) -> Dict[str, int]:
        query = """
        SELECT
            COUNT(*) AS TOTAL,
            COUNT(
                CASE
                    WHEN ACC.CHECK = TRUE THEN 1
                END
            ) AS COMPLETE,
            COUNT(
                CASE
                    WHEN ACC.CHECK = FALSE THEN 1
                END
            ) AS NOT_COMPLETE
        FROM
            "event" E
            INNER JOIN "eventhasresponsability" EHR ON E.ID = EHR.EVENT_ID
            INNER JOIN "accomplishment" ACC ON ACC.ID = EHR.ACCOMPLISHMENT_ID
        WHERE
            E.ID = $1;
        """

        async with in_transaction() as conn:
            results = await conn.execute_query_dict(query, [_id])
        return results[0] if results else {"total": 0, "complete": 0, "not_complete": 0}

    async def get_all_status_of_accomplishments_by_date_range(
        self, start_date: str, end_date: str
    ) -> Dict[str, int]:
        query = """
        SELECT
            COUNT(*) AS TOTAL,
            COUNT(
                CASE
                    WHEN ACC.CHECK = TRUE THEN 1
                END
            ) AS COMPLETE,
            COUNT(
                CASE
                    WHEN ACC.CHECK = FALSE THEN 1
                END
            ) AS NOT_COMPLETE
        FROM
            "event" E
            INNER JOIN "eventhasresponsability" EHR ON E.ID = EHR.EVENT_ID
            INNER JOIN "accomplishment" ACC ON ACC.ID = EHR.ACCOMPLISHMENT_ID
        WHERE
            E.date_start >= $1 AND E.date_start <= $2;
        """

        async with in_transaction() as conn:
            results = await conn.execute_query_dict(query, [start_date, end_date])
        return results[0] if results else {"total": 0, "complete": 0, "not_complete": 0}

    async def get_count_by_spaces_and_months(
        self, year: int
    ) -> Dict[str, List[Dict[str, str]]]:
        query = """
            WITH all_months AS (
                SELECT
                    generate_series(1, 12) AS month_num
            ),
            event_counts AS (
                SELECT
                    EXTRACT(MONTH FROM TO_DATE(e.date_start, 'YYYY-MM-DD')) AS month_num,
                    s.name AS space_name,
                    COUNT(*) AS event_count
                FROM
                    event e
                JOIN
                    space s ON e.place_id = s.id
                WHERE
                    s.active IS TRUE AND
                    EXTRACT(YEAR FROM TO_DATE(e.date_start, 'YYYY-MM-DD')) = $1
                GROUP BY
                    EXTRACT(MONTH FROM TO_DATE(e.date_start, 'YYYY-MM-DD')),
                    s.name
            )
            SELECT
                TRIM(TO_CHAR(TO_DATE(am.month_num::text, 'MM'), 'Month')) AS month,
                json_object_agg(s.name, COALESCE(ec.event_count, 0)) AS event_counts
            FROM
                all_months am
            CROSS JOIN
                (SELECT DISTINCT name FROM space WHERE space.active IS TRUE) s
            LEFT JOIN
                event_counts ec ON am.month_num = ec.month_num AND s.name = ec.space_name
            GROUP BY
                am.month_num
            ORDER BY
                am.month_num;
        """
        async with in_transaction() as conn:
            results: List[Dict] = await conn.execute_query_dict(query, [year])
        events_by_spaces_info: List[Dict[str, str]] = []
        space_types: List[Dict[str, str]] = []
        for row in results:
            event_counts: Dict = json.loads(row["event_counts"])
            if len(space_types) == 0:
                for spaces in event_counts.keys():
                    space_types.append({"name": spaces, "value": spaces})
            event_counts.update({"month": TranslateMonth[row["month"]]})
            events_by_spaces_info.append(event_counts)
        return {
            "events_by_spaces_info": events_by_spaces_info,
            "space_types": space_types,
        }

    async def get_count_by_contractual_modes_and_months(
        self, year: int
    ) -> Dict[str, List[Dict[str, str]]]:
        query = """
            WITH all_months AS (
                SELECT
                    generate_series(1, 12) AS month_num
            ),
            event_counts AS (
                SELECT
                    EXTRACT(MONTH FROM TO_DATE(e.date_start, 'YYYY-MM-DD')) AS month_num,
                    cm.name AS mode_name,
                    COUNT(*) AS event_count
                FROM
                    event e
                JOIN
                    contractualmode cm ON e.place_id = cm.id
                WHERE
                    cm.active IS TRUE AND
                    EXTRACT(YEAR FROM TO_DATE(e.date_start, 'YYYY-MM-DD')) = $1
                GROUP BY
                    EXTRACT(MONTH FROM TO_DATE(e.date_start, 'YYYY-MM-DD')),
                    cm.name
            )
            SELECT
                TRIM(TO_CHAR(TO_DATE(am.month_num::text, 'MM'), 'Month')) AS month,
                json_object_agg(cm.name, COALESCE(ec.event_count, 0)) AS event_counts
            FROM
                all_months am
            CROSS JOIN
                (SELECT DISTINCT name FROM contractualmode WHERE contractualmode.active IS TRUE) cm
            LEFT JOIN
                event_counts ec ON am.month_num = ec.month_num AND cm.name = ec.mode_name
            GROUP BY
                am.month_num
            ORDER BY
                am.month_num;
        """
        async with in_transaction() as conn:
            results: List[Dict] = await conn.execute_query_dict(query, [year])
        events_by_spaces_info: List[Dict[str, str]] = []
        space_types: List[Dict[str, str]] = []
        for row in results:
            event_counts: Dict = json.loads(row["event_counts"])
            if len(space_types) == 0:
                for spaces in event_counts.keys():
                    space_types.append({"name": spaces, "value": spaces})
            event_counts.update({"month": TranslateMonth[row["month"]]})
            events_by_spaces_info.append(event_counts)
        return {
            "events_by_mode_info": events_by_spaces_info,
            "mode_types": space_types,
        }


crud_event = CRUDEvent(model=Event)
