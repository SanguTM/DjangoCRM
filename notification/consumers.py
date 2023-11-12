import json
from urllib import request
from asgiref.sync import AsyncToSync, async_to_sync, sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from django.utils.timesince import timesince
from user.models import User
from django.template.loader import get_template

class NotificationConsumer(AsyncWebsocketConsumer):
    groups = ['general_group']
    
    async def connect(self):
        self.user = self.scope['user']
        self.GROUP_NAME = 'user-notifications'
        await self.accept()
        
        await self.channel_layer.group_add(
            self.GROUP_NAME, self.channel_name
        )
        
        await self.channel_layer.group_send(self.GROUP_NAME, 
            {
                'type': 'tester_message'
            }
        )
                
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
                self.GROUP_NAME, self.channel_name
        )
                            
    async def tester_message(self, event):
        # Send information to the web socket (front end)
        await self.send(text_data=json.dumps({
            'type': 'tester_message'
        }))
        
    async def room_created(self, event):
        if self.user.is_staff:
            # Send information to the web socket (front end)
            await self.send(text_data=json.dumps({
                'type': event['type'],
                'text': event['text'],
            }))
            print(event)

    
    
    
    #https://stackoverflow.com/questions/55534182/new-chat-message-notification-django-channels

     
        #https://stackoverflow.com/questions/52446540/how-to-use-multiple-websocket-connections-using-django-channels