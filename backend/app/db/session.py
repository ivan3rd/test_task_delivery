from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)
from .base import Base


class DatabaseSessionManager:
    def __init__(self):
        self._engine = None
        self._sessionmaker = None

    def init(self, url: str):
        self._engine = create_async_engine(
            url,
            pool_pre_ping=True,
            echo=True
        )
        self._sessionmaker = async_sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
            class_=AsyncSession
        )

    async def close(self):
        if self._engine is None:
            return
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    async def get_session(self) -> AsyncSession:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")
        return self._sessionmaker()

    async def create_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


session_manager = DatabaseSessionManager()
