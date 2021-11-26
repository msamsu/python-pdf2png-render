from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied

from endpoints.models import Work
from swarm.tasks import process_pdf


class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = ('id', 'pdf_file', 'orig_pdf_name', 'status', 'page_count', 'created_at', 'work_started_at', 'done_at', 'output_urls')
        read_only_fields = ('id', 'orig_pdf_name', 'status', 'page_count', 'created_at', 'work_started_at', 'done_at', 'output_urls')

    def create(self, validated_data: dict) -> Work:
        if validated_data['pdf_file'].content_type != 'application/pdf':
            raise ValidationError({'error': 'pdf_file is not of content type application/pdf'})
        instance = super(WorkSerializer, self).create(validated_data)
        process_pdf.delay(instance.id)
        return instance

    def update(self, instance: Work, validated_data: dict):
        # TODO: delete
        raise PermissionDenied({'error': 'not permitted'})
