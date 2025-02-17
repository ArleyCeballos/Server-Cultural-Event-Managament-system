from app.infra.postgres.crud.specific_responsability import crud_specific_responsability
from app.services.base import BaseService


class ServiceSpecificResponsability(BaseService):
    ...


service_specific_responsability = ServiceSpecificResponsability(
    crud=crud_specific_responsability
)
