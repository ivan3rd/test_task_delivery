from celery import Celery
from kombu import Queue
from app.settings import CACHE_URL
# from app.main import app as main_app


# BROKER_URL = os.getenv('CACHE_URL')

# celery_app = Celery(main_app)
app = Celery(
    'tasks',
    broker=f'{CACHE_URL}/1',
    backend=f'{CACHE_URL}/2',
    include=['celery_tasks.tasks'],
)

app.conf.update(
    # tasks_queues=(Queue('tasks.test_task')),
    tasks_routes={
        # 'tasks.test_task': {'queue': 'tasks.test_task'}
        'tasks.set_delivery_cost_task': {'queue': 'tasks.set_delivery_cost_task'}
    },
    task_seralizer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    # For async optimization
    task_always_eager=False,
    task_create_missing_queues=True,
)

