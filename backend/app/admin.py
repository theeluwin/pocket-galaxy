from django.contrib import admin

from app.models import (
    Message,
    Document,
)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):

    model = Message

    list_display = ('id', 'user', 'content', 'published_at', 'modified_at')
    ordering = ('-published_at',)
    search_fields = ('content',)

    raw_id_fields = ('user',)
    readonly_fields = ('published_at', 'modified_at')
    fieldsets = (
        ('Details', {
            'fields': ('user', 'content',),
        }),
        ('Metadata', {
            'fields': ('published_at', 'modified_at'),
        }),
    )


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):

    model = Document

    list_display = ('id', 'title', 'published_at', 'modified_at')
    ordering = ('-published_at',)
    search_fields = ('title',)

    readonly_fields = ('published_at', 'modified_at')
    fieldsets = (
        ('Details', {
            'fields': ('title', 'content'),
        }),
        ('Metadata', {
            'fields': ('published_at', 'modified_at'),
        }),
    )
