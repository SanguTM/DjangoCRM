from django.conf import settings
from django.db import models
#from django.contrib.auth.models import User
from user.models import User

from team.models import Team

class Lead(models.Model):
    
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    
    CHOICES_PRIORITY = (
        (LOW, 'low'),
        (MEDIUM, 'medium'),
        (HIGH, 'high'),
    )
    
    NEW = 'new'
    CONTACTED = 'contacted'
    WON = 'won'
    LOST = 'lost'
    
    CHOICES_STATUS = (
        (NEW, 'new'),
        (CONTACTED, 'contacted'),
        (WON, 'won'),
        (LOST, 'lost'),
    )
    
    team = models.ForeignKey(Team, related_name='leads', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=10, choices=CHOICES_PRIORITY, default=MEDIUM)
    status = models.CharField(max_length=10, choices=CHOICES_STATUS, default=NEW)
    is_client = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='leads', on_delete=models.CASCADE)
    #created_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='leads', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name ##pasako koks laukas bus rodomas admin puslapyje
    
class LeadFile(models.Model):
    team = models.ForeignKey(Team, related_name='lead_files', on_delete=models.CASCADE, null=True, blank=True)
    lead = models.ForeignKey(Lead, related_name='files', on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to='leadfiles', null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='lead_files', on_delete=models.CASCADE)
    #created_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='lead_files', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.created_by.username


class Comment(models.Model):
    team = models.ForeignKey(Team, related_name='lead_comments', on_delete=models.CASCADE, null=True, blank=True)
    lead = models.ForeignKey(Lead, related_name='comments', on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='lead_comments', on_delete=models.CASCADE)
    #created_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='lead_comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.content