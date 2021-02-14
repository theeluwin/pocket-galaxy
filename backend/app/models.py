from django.db import models


class Document(models.Model):

    title = models.CharField(
        max_length=20,
        verbose_name="Title"
    )
    content = models.TextField(
        verbose_name="Content"
    )
    published_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Published At"
    )
    modified_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Modified At"
    )

    def __str__(self):
        return f"[doc-{self.pk}] {self.title}"
