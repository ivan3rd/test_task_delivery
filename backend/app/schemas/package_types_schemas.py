from uuid import UUID

from pydantic import BaseModel


class PackageType(BaseModel):
    id: UUID
    name: str
