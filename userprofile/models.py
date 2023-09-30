from ast import mod
from pyexpat import model
from turtle import mode
from django.db import models
from django.contrib.auth.models import User
from team.models import Team
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)
    active_team = models.ForeignKey(Team, related_name='userprofile', blank=True, null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username
    
#https://github.com/SteinOveHelset/saulgadgets/blob/master/apps/userprofile/models.py
User.userprofile = property(lambda u:UserProfile.objects.get_or_create(user=u)[0])