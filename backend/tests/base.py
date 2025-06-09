import os
import io
import sqlalchemy as sa
from httpx import AsyncClient, ASGITransport
# import trio
from typing import override
from uuid import UUID, uuid4
import unittest as ut
from unittest.mock import patch, MagicMock
import asyncio

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine

from app.db import session_manager, db_session, db_transaction, Base
from app.models import PackageTypeModel
from app.main import app as main_app, lifespan # Import your FastAPI app


DATABASE_URL = os.getenv('DATABASE_URL')
TEST_DATABASE_URL = DATABASE_URL+'/test_delivery?local_infile=1'


class BaseTestCase(ut.IsolatedAsyncioTestCase):

    client: AsyncClient = None


    async def init_db(self):
        await session_manager.init(TEST_DATABASE_URL)
        await session_manager.connect()
        await session_manager.create_all()

    async def close_db(self):
        await session_manager.session.close()
        await session_manager.drop_all()
        await session_manager.close()


    @override
    async def asyncSetUp(self):
        # client
        self.client = AsyncClient(transport=ASGITransport(app=main_app), base_url='http://test')

        # db
        await self.init_db()
        type_packages = [{'name': 'electronics'}, {'name': 'clothes'}, {'name': 'misc'}]
        self.session = session_manager.session
        for t in type_packages:
            self.session.add(PackageTypeModel(name=t['name']))
        await self.session.commit()


    @override
    async def asyncTearDown(self):
        await self.close_db()
        await self.client.aclose()


