from uuid import uuid4, UUID
from datetime import datetime

import sqlalchemy as sa

from app.db import Base, db_session, session_manager
from .package_type_model import PackageTypeModel


class PackageModel(Base):
    __tablename__ = 'package'

    id = sa.Column(sa.String(36), primary_key=True, index=True, server_default=sa.text('UUID()'), default=sa.text('UUID()'))
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow, server_default=sa.func.now(), nullable=False)
    updated_at = sa.Column(sa.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, server_default=sa.func.now(), server_onupdate=sa.func.now(), nullable=False)

    name = sa.Column(sa.String(255))
    weight = sa.Column(sa.Float)
    session_id = sa.Column(sa.String(36), nullable=False)
    type_id = sa.Column(sa.String(36), sa.ForeignKey('package_type.id', ondelete='CASCADE'), nullable=False)
    content_cost = sa.Column(sa.Float)
    delivery_cost = sa.Column(sa.Float)

    @classmethod
    async def get_total_count(
        cls,
        package_type: str | None = None,
        session_id: UUID | None = None
    ):
        query = sa.select(sa.func.count(PackageModel.id))
        if session_id:
            query = query.where(PackageModel.session_id == str(session_id))
        if package_type:
            query = query.outerjoin(
                PackageTypeModel, PackageModel.type_id == PackageTypeModel.id
            ).where(PackageTypeModel.name == package_type)
        return (await session_manager.session.scalar(query))
        # async with db_session() as session:
            # return (await session.scalar(query))

    @classmethod
    async def get_all(
        cls, page: int | None = None,
        page_size: int | None = None,
        package_type: str | None = None,
        has_delivery_cost: bool | None = None,
        session_id: UUID | None = None
    ):
        query = sa.select(PackageModel)
        if session_id:
            query = query.where(PackageModel.session_id == str(session_id))
        if package_type:
            query = query.outerjoin(
                PackageTypeModel, PackageModel.type_id == PackageTypeModel.id
            ).where(PackageTypeModel.name == package_type)
            print('package_type: ', package_type)
        if has_delivery_cost is not None:
            if has_delivery_cost == False:
                query = query.where(PackageModel.delivery_cost.is_(None))
            if has_delivery_cost == True:
                query = query.where(PackageModel.delivery_cost.is_not(None))
        if page and page_size:
            offset = (page - 1) * page_size
            query = query.offset(offset).limit(page_size)
        return (await session_manager.session.scalars(query))
        # async with db_session() as session:
            # return (await session.scalars(query)).all()

    @classmethod
    async def get_by_id(cls, _id: UUID | str, session_id: UUID | None = None):
        query = sa.select(PackageModel).where(PackageModel.id == str(_id))
        if session_id:
            query = query.where(PackageModel.session_id == str(session_id))
        return (await session_manager.session.scalars(query)).one_or_none()

    def count_delivery_cost(self, der: float = 100):
        self.delivery_cost = (self.weight * 0.5 + self.content_cost * 0.01) * der

