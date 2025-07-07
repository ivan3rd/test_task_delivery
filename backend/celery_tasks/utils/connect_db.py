import logging
from asyncio import iscoroutinefunction
from functools import wraps

from app.settings import DATABASE_URL


logger = logging.getLogger('celery.info')


def connect_db(func):
    """
    Wrapper function for connecting to database
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # for now, easyest way to test task with real containers dynamic is to use test_database directly
        # Alternitevly, it's possible to create instance of celery_app in same conteiner and test eviroment that is data
        # await session_manager.init(TEST_DATABASE_URL)
        await session_manager.init(DATABASE_URL)
        await session_manager.connect()

        try:
            if iscoroutinefunction(func):
                return await func(*args, **kwargs)
            else:
                return func(*args, **kwargs)
        finally:
            await session_manager.session.close()
            await session_manager.close()

    return wrapper



