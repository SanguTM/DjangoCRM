from django.apps import AppConfig


class ticketConfig(AppConfig):
    name = 'ticket'

    def ready(self):
        from . import signals