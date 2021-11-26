import logging

from django.core.exceptions import ObjectDoesNotExist
from celery import shared_task

from endpoints.models import Work

logger = logging.getLogger('default')


@shared_task(ack_late=True, queue='swarm')
def process_pdf(pk: int):
    try:
        work = Work.objects.get(pk=pk)
    except ObjectDoesNotExist:
        logger.debug(f'Work of pk {pk} does not exist')
        return
    print(f'Work {work.id} started')
    logger.debug(f'Work {work.id} started')
