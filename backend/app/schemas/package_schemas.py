from uuid import UUID

from pydantic import BaseModel
from .package_types_schemas import PackageType
from .utils import SchemaBase


class PackageInSchema(SchemaBase):
    name: str
    weight: float
    type_id: UUID | None
    content_cost: float | None


class PackageOutSchema(PackageInSchema):
    id: UUID
    delivery_cost: float | None
