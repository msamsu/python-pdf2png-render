from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from endpoints.models import Work


class WorkSerializer(serializers.ModelSerializer):
    output_urls = serializers.SerializerMethodField()

    class Meta:
        model = Work
        fields = ('id', 'pdf_file', 'orig_pdf_name', 'status', 'page_count', 'created_at', 'work_started_at', 'done_at', 'output_urls')
        read_only_fields = ('id', 'orig_pdf_name', 'status', 'page_count', 'created_at', 'work_started_at', 'done_at', 'output_urls')

    def get_output_urls(self, obj: Work) -> list:
        return [self.context['request'].build_absolute_uri(item.png_file.url) for item in obj.outputs.all()]

    def create(self, validated_data: dict) -> Work:
        if validated_data['pdf_file'].content_type != 'application/pdf':
            raise ValidationError({'error': 'pdf_file is not of content type application/pdf'})
        return super(WorkSerializer, self).create(validated_data)
