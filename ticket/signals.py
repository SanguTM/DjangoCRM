from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from ticket.models import Ticket
from notification.models import Email

@receiver(post_save, sender=Ticket)
def send_notification(sender, instance, created, **kwargs):
    if created:
        
        channel_layer = get_channel_layer()
        GROUP_NAME = 'user-notifications'
        event = {
            "type": 'ticket_created',
            "text": 'Client created new ticket: ' + instance.title + ' Client: ' + instance.created_by.username
        }
        async_to_sync(channel_layer.group_send)(GROUP_NAME, event)
        #channel_layer.group_send(group_name, event)


        