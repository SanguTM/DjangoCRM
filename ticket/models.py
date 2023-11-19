import uuid
from django.db import models
from user.models import User

class Ticket(models.Model):
    
    ACTIVE = 'active'
    COMPLETED = 'completed'
    PENDING = 'pending'
    
    CHOICES_STATUS = (
        (ACTIVE, 'Active'),
        (COMPLETED, 'Completed'),
        (PENDING, 'Pending'),
    )
    
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    
    CHOICES_PRIORITY = (
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    )

    #ticket_number = models.UUIDField(default=uuid.uuid4)
    ticket_number = models.CharField(max_length=15, unique=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='tickets', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    assign_to = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    is_resolved = models.BooleanField(default=False)
    accepted_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=CHOICES_STATUS, default=PENDING)
    priority = models.CharField(max_length=15, choices=CHOICES_PRIORITY, default=MEDIUM)
    solution = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at', 'priority', 'ticket_number']
    
    def __str__(self):
        return f'{self.title} - {self.created_by} - {self.created_at}'
    
class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='comments', on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='ticket_comments', on_delete=models.CASCADE)
    #created_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='client_comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.content
    
class TicketFile(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='files', on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to='ticketfiles', null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='ticket_files', on_delete=models.CASCADE)
    #created_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='client_files', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.created_by.username