from pydantic import BaseModel, Field


class CreateState(BaseModel):
    name: str = Field(...)


class UpdateState(BaseModel):
    name: str = Field(None)


class StateDB(CreateState):
    id: int = Field(...)

    class Config:
        from_attributes = True
