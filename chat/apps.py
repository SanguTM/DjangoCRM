from django.apps import AppConfig


class chatConfig(AppConfig):
    name = 'chat'

    def ready(self):
        from . import signals