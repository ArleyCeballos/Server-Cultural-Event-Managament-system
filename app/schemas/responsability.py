from typing import Optional

from pydantic import BaseModel, Field


class CreateResponsability(BaseModel):
    name: str = Field(...)
    description: str = Field(...)


class UpdateResponsability(BaseModel):
    name: str = Field(None)
    description: str = Field(None)
    template_url: str = Field(None)


class ResponsabilityDB(CreateResponsability):
    id: int = Field(...)
    template_url: Optional[str] = Field(None)

    class Config:
        from_attributes = True
