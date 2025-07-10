from django.urls import (
    path,
    include,
)
from rest_framework.routers import DefaultRouter

from app import (
    views,
    viewsets,
)


router = DefaultRouter()
router.register('messages', viewsets.MessageViewSet, basename='api_message')
router.register('documents', viewsets.DocumentViewSet, basename='api_document')

urlpatterns = [
    path('token/login/', views.APITokenLoginView.as_view(), name='api_token_login'),
    path('token/refresh/', views.APITokenRefreshView.as_view(), name='api_token_refresh'),
    path('token/logout/', views.APITokenLogoutView.as_view(), name='api_token_logout'),
    path('health/', views.api_health, name='api_health'),
    path('websocket/ticket/', views.api_websocket_ticket, name='api_websocket_ticket'),
    path('users/register/', views.api_user_register, name='api_user_register'),
    path('users/profile/', views.api_user_profile, name='api_user_profile'),
    path('users/password/request/', views.api_user_password_request, name='api_user_password_request'),
    path('users/password/reset/', views.api_user_password_reset, name='api_user_password_reset'),
    path('', include(router.urls)),
]
