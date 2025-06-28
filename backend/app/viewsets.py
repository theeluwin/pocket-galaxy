from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import (
    authentication_classes,
    permission_classes,
)

from app.serializers import DocumentSerializer
from app.models import Document


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class DocumentViewSet(viewsets.ModelViewSet):

    model = Document
    queryset = Document.objects.order_by('-pk')
    serializer_class = DocumentSerializer
    filterset_fields = {
        'id': ('exact',),
    }
