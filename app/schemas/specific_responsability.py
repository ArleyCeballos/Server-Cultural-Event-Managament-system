from pydantic import BaseModel, Field


class CreateSpecificResponsability(BaseModel):
    name: str = Field(...)
    description: str = Field(...)


class UpdateSpecificResponsability(BaseModel):
    name: str = Field(None)
    description: str = Field(None)


class SpecificResponsabilityDB(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True
