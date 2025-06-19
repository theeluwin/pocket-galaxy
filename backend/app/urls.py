from django.urls import path
from django.urls import include
from rest_framework import routers

from app import views
from app.viewsets import DocumentViewSet


router = routers.SimpleRouter()
router.register('documents', DocumentViewSet)

urlpatterns = [
    path('health/', views.api_health),
    path('', include((router.urls, 'router'))),
]
