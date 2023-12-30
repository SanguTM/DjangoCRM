from django import forms
from .models import Ticket, Comment, TicketFile

INPUT_CLASS = 'w-full py-1.5 px-6 rounded-xl border'

LOW = 'low'
MEDIUM = 'medium'
HIGH = 'high'
    
CHOICES_PRIORITY = (
    (LOW, 'Low'),
    (MEDIUM, 'Medium'),
    (HIGH, 'High'),
)

ACTIVE = 'active'
COMPLETED = 'completed'
PENDING = 'pending'
    
CHOICES_STATUS = (
    (ACTIVE, 'Active'),
    (COMPLETED, 'Completed'),
    (PENDING, 'Pending'),
)

class CreateTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('title', 'description', 'priority',)
        
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': INPUT_CLASS
    }))
    description = forms.CharField(strip=False,widget=forms.Textarea(attrs={
        'class': INPUT_CLASS
    }))
    priority = forms.ChoiceField(choices=CHOICES_PRIORITY, widget=forms.Select(attrs={
        'class': INPUT_CLASS
    }))

class UpdateTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('title', 'description', 'priority', 'status')
        
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': INPUT_CLASS
    }))
    description = forms.CharField(strip=False, widget=forms.Textarea(attrs={
        'class': INPUT_CLASS
    }))
    priority = forms.ChoiceField(choices=CHOICES_PRIORITY, widget=forms.Select(attrs={
        'class': INPUT_CLASS
    }))
    status = forms.ChoiceField(choices=CHOICES_STATUS, widget=forms.Select(attrs={
        'class': INPUT_CLASS
    }))
    
class CloseTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('solution',)
        
    solution = forms.CharField(label='', widget=forms.Textarea(attrs={
        'class': INPUT_CLASS,
        'required': True
    }))

class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        
    content = forms.CharField(label='', widget=forms.Textarea(attrs={
        'class': INPUT_CLASS
    }))
        
class AddFileForm(forms.ModelForm):
    class Meta:
        model = TicketFile
        fields = ('file',)
        