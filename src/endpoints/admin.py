from django.contrib import admin

from endpoints.models import Work


class WorkAdmin(admin.ModelAdmin):
    search_fields = ('id', )
    list_display = ('id', 'orig_pdf_name', 'pdf_file', 'status', 'page_count', 'created_at', 'work_started_at', 'done_at')
    list_filter = ('status', )
    has_add_permission = has_delete_permission = lambda self, request, obj=None: request.user.is_superuser


admin.site.register(Work, WorkAdmin)
