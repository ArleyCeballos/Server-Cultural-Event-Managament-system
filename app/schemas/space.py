from pydantic import BaseModel, Field


class CreateSpace(BaseModel):
    name: str = Field(...)


class UpdateSpace(BaseModel):
    name: str = Field(None)


class SpaceDB(CreateSpace):
    id: int = Field(...)

    class Config:
        from_attributes = True
