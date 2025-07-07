import os
from httpx import AsyncClient, ASGITransport
from typing import override
import unittest as ut


from app.db import session_manager
from app.models import PackageTypeModel
from app.main import app as main_app # Import your FastAPI app
from app.settings import TEST_DATABASE_URL


class BaseTestCase(ut.IsolatedAsyncioTestCase):

    client: AsyncClient = None
    client1: AsyncClient = None


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

        self.client1 = AsyncClient(transport=ASGITransport(app=main_app), base_url='http://test')

        # db
        await self.init_db()
        self.type_packages = [{'name': 'electronics'}, {'name': 'clothes'}, {'name': 'misc'}]
        self.session = session_manager.session
        for t in self.type_packages:
            self.session.add(PackageTypeModel(name=t['name']))
        await self.session.commit()


    @override
    async def asyncTearDown(self):
        await self.close_db()
        await self.client.aclose()


