from uuid import UUID, uuid4
from copy import deepcopy
import unittest as ut
from sqlalchemy import select
from .base import BaseTestCase

from app.main import app  # Import your FastAPI app
from app.db import session_manager, db_session, db_transaction, Base, db_session_manager
from app.models import PackageTypeModel, PackageModel


class TestPackageRouter(BaseTestCase):

    async def test_get_package_types(self):
        response = await self.client.get("/package/types")
        self.assertEqual(response.status_code, 200) # shows you what's in the asserted variable in case of test_error
        response_data = response.json()
        self.assertGreaterEqual(len(response_data), 3)
        for t in response_data:
            self.assertIsNotNone(t['id'])


    async def test_post_route(self):
        response = await self.client.get("/package/")

        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.json())
        self.assertIn('total_items', response.json())
        self.assertEqual(response.json().get('total_items', 0), 0)
        self.assertEqual(len(response.json().get('results', [])), 0)

        package_types = await PackageTypeModel.get_all()
        chosen_type = package_types[0]

        package_data ={
            'name': 'bear',
            'weight': 1000.00,
            'type_id': str(chosen_type.id),
            'content_cost': 100,
        }
        false_package_data = deepcopy(package_data)
        false_package_data['type_id'] = str(uuid4())

        response = await self.client.post("/package/", json=false_package_data)
        self.assertEqual(response.status_code, 422)

        packages = (await self.session.scalars(select(PackageModel))).all()
        self.assertEqual(len(packages), 0)

        response = await self.client.post("/package/", json=package_data)
        self.assertEqual(response.status_code, 201)
        await self.session.reset()
        packages = (await self.session.scalars(select(PackageModel))).all()

        self.assertEqual(len(packages), 1)

        # Нужно будет так же протестировать куки сайта и как на них реагирует тестовое окружение.
