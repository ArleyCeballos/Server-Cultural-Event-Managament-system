from pydantic import BaseModel, Field


class CreateContractualMode(BaseModel):
    name: str = Field(...)


class UpdateContractualMode(BaseModel):
    name: str = Field(None)


class ContractualModeDB(CreateContractualMode):
    id: int = Field(...)

    class Config:
        from_attributes = True
