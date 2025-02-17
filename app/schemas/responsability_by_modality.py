from typing import Optional

from pydantic import BaseModel, Field


class CreateResponsabilityByMode(BaseModel):
    applies: bool = Field(...)
    responsability_id: int = Field(...)
    space_id: int = Field(...)
    mode_id: int = Field(...)


class SearchresponsabilityByMode(BaseModel):
    applies: Optional[bool] = Field(None)
    responsability: Optional[int] = Field(None)
    space_id: Optional[int] = Field(None)
    mode_id: Optional[int] = Field(None)


class UpdateResponsabilityByMode(BaseModel):
    applies: Optional[bool] = Field(None)


class ResponsabilityByModeDB(BaseModel):
    applies: bool = Field(...)
    responsability_id: int = Field(...)
    mode_id: int = Field(...)
    space_id: int = Field(...)
    id: int = Field(...)
    responsability_name: Optional[str] = Field(None)
    mode_name: Optional[str] = Field(None)
    space_name: Optional[str] = Field(None)

    class Config:
        from_attributes = True
