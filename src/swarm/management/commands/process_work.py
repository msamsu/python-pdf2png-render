from django.core.management.base import BaseCommand

from swarm.tasks import process_pdf


class Command(BaseCommand):

    def handle(self, *args, **options):
        process_pdf(5)
