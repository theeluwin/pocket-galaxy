from django.apps import AppConfig as AppConfigBase


class AppConfig(AppConfigBase):

    name = 'app'
    default_auto_field = 'django.db.models.BigAutoField'
