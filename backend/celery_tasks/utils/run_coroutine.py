import logging

from app.settings import TEST_DATABASE_URL

logger = logging.getLogger('celery.info')

from asyncio import iscoroutinefunction, run
from functools import wraps


def run_coroutine(func):
    """
    Wrapper function that is essential for working with celery in async eviroment
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return run(func(*args, **kwargs))

    if iscoroutinefunction(func):
        return wrapper
    else:
        return func



