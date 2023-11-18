from django.db import models

# Create your models here.

class Email(models.Model):
    subject = models.CharField(max_length=2000, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_sent = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f'{self.created_at} - {self.email} - {self.subject}'
    
class EmailSetting(models.Model):
    email_host = models.TextField(blank=True, null=True)
    email_port = models.TextField(blank=True, null=True)
    email_use_tls = models.BooleanField(default = True)
    email_from_email = models.TextField(blank=True, null=True)
    email_host_user = models.TextField(blank=True, null=True)
    email_host_password = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.email_host_user
    