from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from endpoints.models import Work


class WorkSerializer(serializers.ModelSerializer):
    pages_rendered = serializers.SerializerMethodField()
    pages_text = serializers.SerializerMethodField()

    class Meta:
        model = Work
        fields = ('id', 'pdf_file', 'orig_pdf_name', 'status', 'page_count', 'created_at', 'work_started_at', 'done_at', 'pages_rendered', 'pages_text')
        read_only_fields = ('id', 'orig_pdf_name', 'status', 'page_count', 'created_at', 'work_started_at', 'done_at', 'pages_rendered', 'pages_text')

    def get_pages_rendered(self, obj: Work) -> list:
        return [self.context['request'].build_absolute_uri(item.png_file.url) for item in obj.outputs.all()]

    def get_pages_text(self, obj: Work) -> list:
        return [item.text for item in obj.outputs.all()]

    def create(self, validated_data: dict) -> Work:
        content_type = validated_data['pdf_file'].content_type
        if content_type != 'application/pdf':
            raise ValidationError({'error': f'pdf_file is not of content type application/pdf: {content_type}'})
        return super(WorkSerializer, self).create(validated_data)
