from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Message(models.Model):

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='User',
    )
    content = models.CharField(
        max_length=255,
        verbose_name='Content',
    )
    published_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Published At',
        db_index=True,
    )
    modified_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Modified At',
    )

    def __str__(self):
        return f"[M{self.pk}] {self.content[:20]}..."


class Document(models.Model):

    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'

    title = models.CharField(
        max_length=255,
        verbose_name='Title',
    )
    content = models.TextField(
        verbose_name='Content',
    )
    published_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Published At',
        db_index=True,
    )
    modified_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Modified At',
    )

    def __str__(self):
        return f"[D{self.pk}] {self.title[:20]}..."
