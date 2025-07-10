import logging

from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from app.consumers import ChatConsumer
from app.models import (
    Message,
    Document,
)
from app.serializers import (
    MessageSerializer,
    DocumentSerializer,
)


def broadcast_chat_message(message):
    channel_layer = get_channel_layer()
    if not channel_layer:
        return
    try:
        async_to_sync(channel_layer.group_send)(
            ChatConsumer.GROUP_NAME,
            {
                'type': 'broadcast_message',
                'message': message,
            }
        )
    except Exception as e:
        logger = logging.getLogger('channels')
        logger.error(f"Failed to broadcast message: {e}")


class MessageViewSet(viewsets.ModelViewSet):

    model = Message
    queryset = Message.objects.select_related('user').order_by('-published_at')
    serializer_class = MessageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']
    ordering = ['-published_at']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        broadcast_chat_message(serializer.data)


class DocumentViewSet(viewsets.ModelViewSet):

    model = Document
    queryset = Document.objects.order_by('-published_at')
    serializer_class = DocumentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']
    filter_backends = [OrderingFilter]
    ordering_fields = ['id', 'published_at', 'modified_at']
    ordering = ['-published_at']
