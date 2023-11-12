from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from chat.models import Room
from asgiref.sync import async_to_sync

@receiver(post_save, sender=Room)
def send_notification(sender, instance, created, **kwargs):
    if created:
        room_name = instance.uuid       

        channel_layer = get_channel_layer()
        GROUP_NAME = 'user-notifications'
        event = {
            "type": "room_created",
            "text": 'Client created new room: ' + instance.uuid + ' Client: ' + instance.chat_user 
        }
        async_to_sync(channel_layer.group_send)(GROUP_NAME, event)
        #channel_layer.group_send(group_name, event)
        