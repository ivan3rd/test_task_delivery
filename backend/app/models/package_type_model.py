from uuid import UUID

import sqlalchemy as sa

from app.db import Base, db_session, session_manager


class PackageTypeModel(Base):
    __tablename__ = 'package_type'

    id = sa.Column(sa.String(36), primary_key=True, index=True, server_default=sa.text('UUID()'), default=sa.text('UUID()'))
    name = sa.Column(sa.String(255))

    @classmethod
    async def get_all(cls):
        return (await session_manager.session.scalars(
            sa.select(PackageTypeModel)
        )).all()
        # async with db_session() as session:
            # return (await session.scalars(
                # sa.select(PackageTypeModel)
            # )).all()

    @classmethod
    async def get_by_id(cls, _id: UUID | str):
        return (await session_manager.session.scalars(
            sa.select(PackageTypeModel)
            .where(PackageTypeModel.id == str(_id))
        )).one_or_none()
        # async with db_session() as session:
            # return (await session.scalars(
                # sa.select(PackageTypeModel)
                # .where(PackageTypeModel.id == str(_id))
            # )).one_or_none()

    # @classmethod
    # async def get_by_name(cls, name: str):
        # result = (await db_session().scalars(
            # sa.select(PackageTypeModel)
            # .where(PackageTypeModel.name == name)
        # )).one_or_none()
        # if not result:
            # result = (await db_session().scalars(
                # sa.select(PackageTypeModel)
                # .where(PackageTypeModel.name == 'misc')
            # )).one_or_none()
        # return result


