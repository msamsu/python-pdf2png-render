from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/v1/', include(('endpoints.urls', 'v1'), namespace='v1')),
    path('openapi', get_schema_view(title="python-pdf2png-render",
                                    description="Python PDF to PNG distributed rendering web app",
                                    version="1.0.0"), name='openapi-schema'),
    path('', TemplateView.as_view(template_name='swagger-ui.html', extra_context={'schema_url':'openapi-schema'}), name='swagger-ui'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
