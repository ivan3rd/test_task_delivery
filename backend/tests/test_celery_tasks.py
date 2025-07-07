from uuid import UUID, uuid4
from time import sleep
from sqlalchemy import select
from .base import BaseTestCase

from app.models import PackageTypeModel, PackageModel
from celery_tasks import set_delivery_cost_task


class TestCeleryTasks(BaseTestCase):

    async def unavailable_test_delivery_cost_task(self):
        """
        This test will only work if in backend/celery_tasks/utils/connect_db.py
        MySQL session manager will use TEST_DATABASE_URL instead of DATABASE_URL.
        If left as is, testcase will search created package item in different
        production database.
        """
        # creating data
        package_types = await PackageTypeModel.get_all()
        package = PackageModel(
            name='test_package',
            weight=69.17,
            type_id=package_types[0].id,
            content_cost=420.00,
            session_id=uuid4(),
        )
        self.session.add(package)
        await self.session.flush()
        await self.session.commit()
        self.assertIsNone(package.delivery_cost)
        set_delivery_cost_task.delay()
        sleep(2)
        self.session.reset()

        package = (await self.session.scalars(select(PackageModel).where(PackageModel.id == package.id))).one()
        self.assertIsNotNone(package.delivery_cost)
