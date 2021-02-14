from django.contrib import admin

from app.models import (
    Document,
)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    model = Document
    list_display = ('id', 'title', 'published_at', 'modified_at')
    search_fields = ('title',)
