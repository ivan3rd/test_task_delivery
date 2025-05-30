from uuid import UUID

from .utils import SchemaBase


class PackageTypeSchema(SchemaBase):
    id: UUID | str
    name: str
