from typing import Any, Dict, List, Optional

from app.schemas.general import CreateSchemaType, CrudType, UpdateSchemaType


class BaseService:
    def __init__(self, *, crud: CrudType) -> None:
        self._crud = crud

    async def create(self, *, obj_in: CreateSchemaType) -> Dict[str, Any]:
        return await self._crud.create(obj_in=obj_in)

    async def update(self, *, _id: int, obj_in: UpdateSchemaType) -> bool:
        return await self._crud.update(_id=_id, obj_in=obj_in)

    async def update_by_filter(
        self, *, payload: Dict[str, Any], obj_in: UpdateSchemaType
    ) -> bool:
        return await self._crud.update_by_filter(payload=payload, obj_in=obj_in)

    async def get_all(
        self,
        *,
        skip: Optional[int] = None,
        limit: Optional[int] = None,
        payload: Dict[str, Any] = {},
    ) -> List[Dict[str, Any]]:
        return await self._crud.get_all(payload=payload, skip=skip, limit=limit)

    async def get_by_id(self, *, _id: int) -> Optional[Dict[str, Any]]:
        return await self._crud.get_by_id(_id=_id)

    async def delete(self, *, _id: int) -> int:
        return await self._crud.delete(_id=_id)

    async def count(self, *, payload: Dict[str, Any] = {}) -> int:
        count = await self._crud.count(payload=payload)
        return count
