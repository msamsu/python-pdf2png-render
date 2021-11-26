from rest_framework import viewsets

from endpoints.models import Work
from endpoints.serializers import WorkSerializer


class WorkViewSet(viewsets.ModelViewSet):
    serializer_class = WorkSerializer
    queryset = Work.objects.all()
