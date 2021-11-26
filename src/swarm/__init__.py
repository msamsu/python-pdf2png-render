from celery import Celery

from celery.concurrency import asynpool
from django.conf import settings

__author__ = 'martin'

# for avoiding the error: Timed out waiting for UP message from <Worker(Worker-11, started daemon)>
# http://stackoverflow.com/questions/24202789/celery-correct-way-to-run-lengthy-initialization-function-per-process
asynpool.PROC_ALIVE_TIMEOUT = 15.0


app = Celery(
    main='pdf2png',
    broker=settings.CELERY_BROKER_URL,
)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# app.conf.update(
#     CELERY_ACCEPT_CONTENT=['json', 'pickle'],
#     CELERY_TASK_SERIALIZER='json',
#     CELERY_RESULT_PERSISTENT=False,
#     CELERY_TIMEZONE=settings.TIME_ZONE,
#     CELERYD_FORCE_EXECV=False,
#     CELERY_DISABLE_RATE_LIMITS=True,
#     CELERYBEAT_SCHEDULE=settings.CELERYBEAT_SCHEDULE,
#     # CELERY_DB_REUSE_MAX=1000,
#     CELERY_IGNORE_RESULT=True,
#     CELERY_STORE_ERRORS_EVEN_IF_IGNORED=False,
#     # results of tasks should be stored at least the same time as async task `.get(timeout=...)`
#     # otherwise results of tasks which already ended can expire before long sibling tasks even finish
#     CELERY_TASK_RESULT_EXPIRES=settings.CELERY_BROKER_HEARTBEAT,
#     CELERY_AMQP_TASK_RESULT_EXPIRES=settings.CELERY_BROKER_HEARTBEAT,
#     CELERY_SEND_EVENTS=False,
#     CELERY_EVENT_QUEUE_TTL=30,
#     BROKER_TRANSPORT_OPTIONS={'confirm_publish': True},
#     BROKER_HEARTBEAT=settings.CELERY_BROKER_HEARTBEAT,
# )

app.conf.update(
   task_serializer='json',
   accept_content=['json', 'pickle'],
   timezone=settings.TIME_ZONE,
   enable_utc=True,
   # broker_transport_options={'confirm_publish': True},
   # broker_heartbeat=20,
   # broker_pool_limit=0,
   task_acks_late=True,
   worker_prefetch_multiplier=100,
)
