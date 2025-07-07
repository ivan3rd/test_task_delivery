import logging

from fastapi import HTTPException
from celery import shared_task

from app.db import db_session
from app.models import PackageModel
from app.utils import get_dollar_exchange_rate
from .utils import connect_db, run_coroutine

logger = logging.getLogger('celery.info')


from sqlalchemy import select

@shared_task(name='tasks.set_delivery_cost_task', acks_late=True)
@run_coroutine
@connect_db
async def set_delivery_cost_task():
    logger.info('set_delivery_cost_task(). Starting recounting delivery cost of a packages')
    der = await get_dollar_exchange_rate()
    if der is None:
        raise HTTPException(status_code=422, detail="Couldn't get der data from service. Can't proceed to recalculate delivery cost")
    async with db_session() as session:
        # Because data on packages could be extremly large,
        # async streaming will be used in order to not overload ram of container
        query = select(PackageModel).where(
            PackageModel.delivery_cost.is_(None)
        )
        data = await session.stream_scalars(query)

        packages_cost_recounted = 0
        async for package in data:
            package.count_delivery_cost(der)
            packages_cost_recounted += 1
        logger.info(f'set_delivery_cost(). Delivery cost was recounted for {packages_cost_recounted} packages.')
        await session.commit()
