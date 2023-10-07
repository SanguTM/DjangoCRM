from django.conf import settings
#from django.contrib.auth.models import User
from user.models import User

from django.db import models

class Plan(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    max_leads = models.IntegerField()
    max_clients = models.IntegerField()
    
    def __str__(self):
        return self.name

class Team(models.Model):
    plan = models.ForeignKey(Plan, related_name='teams', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name='teams')
    #members = models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='teams')
    created_by = models.ForeignKey(User, related_name='created_teams', on_delete=models.CASCADE)
    #created_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='created_teams', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
