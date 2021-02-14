from django.urls import path
from django.urls import include
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static

from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token


# admin
admin.site.site_title = settings.ADMIN_TITLE
admin.site.site_header = settings.ADMIN_TITLE

# add media and static url
urlpatterns = []
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# gather all
urlpatterns.extend([

    # admin
    path('admin/', admin.site.urls),

    # auth
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token/auth/', obtain_jwt_token),
    path('api/token/refresh/', refresh_jwt_token),
    path('api/token/verify/', verify_jwt_token),

    # api
    path('api/', include(('app.urls', 'app'))),

])
