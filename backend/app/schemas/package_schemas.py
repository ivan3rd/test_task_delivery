from uuid import UUID

from .utils import SchemaBase


class PackageInSchema(SchemaBase):
    name: str
    weight: float
    type_id: UUID | None
    content_cost: float | None


class PackageOutSchema(PackageInSchema):
    id: UUID
    delivery_cost: float | None
