from app.infra.postgres.crud.base import CRUDBase
from app.infra.postgres.models.specific_responsability import SpecificResponsability
from app.schemas.specific_responsability import (
    CreateSpecificResponsability,
    UpdateSpecificResponsability,
)


class CRUDSpecificResponsability(
    CRUDBase[
        SpecificResponsability,
        CreateSpecificResponsability,
        UpdateSpecificResponsability,
    ]
):
    ...


crud_specific_responsability = CRUDSpecificResponsability(model=SpecificResponsability)
