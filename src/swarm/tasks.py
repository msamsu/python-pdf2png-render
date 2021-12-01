import logging
import tempfile

from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.utils import timezone
from pdf2image import convert_from_path

from endpoints.models import Work, Output

logger = logging.getLogger('default')


@shared_task(ack_late=True, queue='swarm')
def process_pdf(pk: int):
    try:
        work = Work.objects.get(pk=pk)
    except ObjectDoesNotExist:
        logger.debug(f'Work of pk {pk} does not exist')
        return

    work.work_started_at = timezone.now()
    work.save(update_fields=['work_started_at'])

    logger.info(f'Work {work.id} started')

    # doc = fitz.open(work.pdf_file.path)
    # print(doc)
    # print(dir(doc))
    # print(doc.__dict__)
    # print(doc.page_count)
    # print(doc.metadata)
    #
    # for page in doc:
    #     print(page)
    #     # print(page.get_text())
    #     pix = page.get_pixmap(width=1200)
    #     print(dir(pix))
    #     print(pix.width)
    #     pix.save("out.png")

    try:
        with tempfile.TemporaryDirectory() as path:
            pages = convert_from_path(work.pdf_file.path, output_folder=path, size=(1200, 1600), dpi=99)
            work.page_count = len(pages)
            work.outputs.all().delete()
            for page in pages:
                with tempfile.TemporaryFile() as ff:
                    page.save(ff, 'PNG')
                    Output.objects.create(work=work, png_file=File(ff, name='temp.png'))
    except:
        logger.exception(f'Processing work {work.id} failed')
        work.status = 'error'
        work.save()
    else:
        logger.info(f'Work {work.id} finished')
        work.done_at = timezone.now()
        work.status = 'done'
        work.save()
