import enum
import os
import pathlib
from uuid import uuid4

from django.db import models
from django.db.models import CASCADE
from django.utils import timezone


class Choices(enum.Enum):

    @classmethod
    def get_choices(cls) -> list:
        return [(item.name, item.value) for item in cls]


class WorkStatus(Choices):
    created = 'created'
    wip = 'wip'
    done = 'done'
    error = 'error'


class WorkPath:

    def __init__(self, kind):
        self.kind = kind

    def upload_to(self, instance, filename: str) -> str:
        assert isinstance(instance, Work)
        instance.orig_pdf_name = filename[:1024]
        uid = str(uuid4())
        return os.path.join('works', self.kind, uid[:2], f'{uid}{pathlib.Path(filename).suffix}')


class Work(models.Model):

    class Meta:
        ordering = ('pk', )

    STATUS = WorkStatus

    pdf_file = models.FileField(upload_to=WorkPath('pdf').upload_to)
    orig_pdf_name = models.CharField(max_length=1024, default='', blank=True)
    status = models.CharField(max_length=8, choices=STATUS.get_choices(), default=STATUS.created.value)
    page_count = models.PositiveIntegerField(default=0, blank=True)
    created_at = models.DateTimeField(default=timezone.now, blank=True)
    work_started_at = models.DateTimeField(null=True, blank=True, default=None)
    done_at = models.DateTimeField(null=True, blank=True, default=None)

    @property
    def output_urls(self) -> list:
        return [item.png_file.url for item in self.outputs.all()]


class Output(models.Model):

    work = models.ForeignKey(Work, related_name='outputs', on_delete=CASCADE)
    png_file = models.FileField(upload_to=WorkPath('png').upload_to)
