from rest_framework import viewsets

from app.serializers import (
    DocumentSerializer,
)
from app.models import (
    Document,
)


class DocumentViewSet(viewsets.ModelViewSet):

    model = Document
    queryset = Document.objects.order_by('-pk')
    serializer_class = DocumentSerializer
    filterset_fields = {
        'id': ('exact',),
    }
