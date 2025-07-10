from django.urls import path
from django.urls import include
from django.conf import settings
from django.contrib import admin


# admin
admin.site.site_title = settings.ADMIN_TITLE
admin.site.site_header = settings.ADMIN_TITLE

# gather all
urlpatterns = [

    # admin
    path('api/admin/', admin.site.urls),

    # api
    path('api/', include(('app.urls', 'app'))),

]
