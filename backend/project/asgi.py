import os

from django.core.asgi import get_asgi_application
from channels.routing import (
    ProtocolTypeRouter,
    URLRouter,
)


from project.middlewares.channels import ChannelsJWTAuthMiddlewareStack
from app.routing import websocket_urlpatterns


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': ChannelsJWTAuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
})
