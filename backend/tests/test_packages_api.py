from uuid import uuid4
from copy import deepcopy
from sqlalchemy import select
from .base import BaseTestCase

from app.models import PackageTypeModel, PackageModel


class TestPackageRouter(BaseTestCase):

    async def test_get_package_types(self):
        response = await self.client.get("/package/types")
        self.assertEqual(response.status_code, 200) # shows you what's in the asserted variable in case of test_error
        response_data = response.json()
        self.assertGreaterEqual(len(response_data), 3)
        for t in response_data:
            self.assertIsNotNone(t['id'])


    async def test_create_and_get(self):
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

        response = await self.client.get("/package/")

        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.json())
        self.assertIn('total_items', response.json())
        self.assertEqual(response.json().get('total_items', 0), 1)
        self.assertEqual(len(response.json().get('results', [])), 1)

        target_package = next((i for i in response.json().get('results', []) if i['name'] == package_data['name']))
        self.assertIsNotNone(target_package)

        self.assertEqual(target_package['weight'], package_data['weight'])
        self.assertIs(type(target_package['weight']), float)
        self.assertEqual(target_package['content_cost'], package_data['content_cost'])
        self.assertIs(type(target_package['content_cost']), float)
        self.assertIsNotNone(target_package['id'])
        self.assertIsNone(target_package['delivery_cost'])

        response = await self.client.put("/package/set-delivery-cost")
        self.assertEqual(response.status_code, 200)

        await self.session.reset()
        response = await self.client.get(f"/package/{target_package['id']}")

        self.assertEqual(response.status_code, 200)
        refreshed_package = response.json()
        self.assertEqual(refreshed_package['name'], target_package['name'])
        self.assertIsNotNone(refreshed_package['delivery_cost'])


        # target_package = next((i for i in response.json().get('results', []) if i['name'] == package_data['name']))
        # Проверяем, что искомая посылка доступна только в пределах сессии первого клиента
        # Пока не работает, нужно перепроверить, когда переделаю сессии
        # response = await self.client1.get("/package/")

        # self.assertEqual(response.status_code, 200)
        # self.assertIn('results', response.json())
        # self.assertIn('total_items', response.json())
        # self.assertEqual(response.json().get('total_items', 0), 0)
        # self.assertEqual(len(response.json().get('results', [])), 0)


    # async def test_get_route(self):
        # response = await self.client.get("/package/")
        # assert response

