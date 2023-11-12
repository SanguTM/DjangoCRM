from django.apps import AppConfig


class notificationConfig(AppConfig):
    name = 'notification'

    def ready(self):
        from . import signals