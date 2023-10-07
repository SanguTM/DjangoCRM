from django.db import models
from django.conf import settings
#from django.contrib.auth.models import User
from user.models import User
from team.models import Team

##https://docs.djangoproject.com/en/4.2/ref/models/fields/
##https://stackoverflow.com/questions/8609192/what-is-the-difference-between-null-true-and-blank-true-in-django
class Client(models.Model):
    team = models.ForeignKey(Team, related_name='clients', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='clients', on_delete=models.CASCADE)
    #created_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='clients', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('name','created_by')
    
    def __str__(self):
        return self.name ##pasako koks laukas bus rodomas admin puslapyje


class Comment(models.Model):
    team = models.ForeignKey(Team, related_name='client_comments', on_delete=models.CASCADE, null=True, blank=True)
    client = models.ForeignKey(Client, related_name='comments', on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='client_comments', on_delete=models.CASCADE)
    #created_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='client_comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.content
    
class ClientFile(models.Model):
    team = models.ForeignKey(Team, related_name='client_files', on_delete=models.CASCADE, null=True, blank=True)
    client = models.ForeignKey(Client, related_name='files', on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to='clientfiles', null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='client_files', on_delete=models.CASCADE)
    #created_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='client_files', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.created_by.username