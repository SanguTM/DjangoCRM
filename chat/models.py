from django.db import models
from user.models import User


class Message(models.Model):
    content = models.TextField()
    sent_by = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    
    class Meta:
        ordering = ('created_at',)
        
    def __str__(self):
        return self.sent_by
    
class Room(models.Model):
    ACTIVE = 'active'
    WAITING = 'waiting'
    CLOSED = 'closed'
    
    CHOICES_STATUS = (
        (ACTIVE, 'Active'),
        (WAITING, 'Waiting'),
        (CLOSED, 'Closed'),
    )

    uuid = models.CharField(max_length=255)
    chat_user = models.CharField(max_length=255)
    agent = models.ForeignKey(User, related_name='rooms', blank=True, null=True, on_delete=models.SET_NULL)
    messages = models.ManyToManyField(Message, blank=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=15, choices=CHOICES_STATUS, default=WAITING)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('created_at',)
        
    def __str__(self):
        #return self.chat_user - self.uuid
        return f'{self.chat_user} - {self.uuid}'