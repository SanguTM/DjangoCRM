from django.db import models
from user.models import User
from team.models import Team
from client.models import Client
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)
    #user = models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='userprofile', on_delete=models.CASCADE)
    active_team = models.ForeignKey(Team, related_name='userprofile', blank=True, null=True, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, related_name='userprofile', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.user.username
    
#https://github.com/SteinOveHelset/saulgadgets/blob/master/apps/userprofile/models.py
User.userprofile = property(lambda u:UserProfile.objects.get_or_create(user=u)[0])