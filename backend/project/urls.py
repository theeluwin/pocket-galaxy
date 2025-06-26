from django.urls import path
from django.urls import include
from django.conf import settings
from django.contrib import admin

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


# admin
admin.site.site_title = settings.ADMIN_TITLE
admin.site.site_header = settings.ADMIN_TITLE

# gather all
urlpatterns = [

    # admin
    path('api/admin/', admin.site.urls),

    # auth
    path('api/token/auth/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # api
    path('api/', include(('app.urls', 'app'))),

]
