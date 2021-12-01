from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from endpoints.models import Work
from endpoints.serializers import WorkSerializer
from swarm.tasks import process_pdf


class WorkViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    serializer_class = WorkSerializer
    queryset = Work.objects.all()

    def perform_create(self, serializer: WorkSerializer):
        super(WorkViewSet, self).perform_create(serializer)
        process_pdf.delay(serializer.instance.id)
