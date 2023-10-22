from django import forms
from .models import Lead, Comment, LeadFile

INPUT_CLASS = 'w-full py-1.5 px-6 rounded-xl border'

LOW = 'low'
MEDIUM = 'medium'
HIGH = 'high'
    
CHOICES_PRIORITY = (
    (LOW, 'Low'),
    (MEDIUM, 'Medium'),
    (HIGH, 'High'),
)

NEW = 'new'
CONTACTED = 'contacted'
WON = 'won'
LOST = 'lost'
    
CHOICES_STATUS = (
    (NEW, 'New'),
    (CONTACTED, 'Contacted'),
    (WON, 'Won'),
    (LOST, 'Lost'),
)

class AddLeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ('name', 'email', 'phone', 'description', 'priority', 'status')
        
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': INPUT_CLASS
    }))
    
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': INPUT_CLASS
    }))
    
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class': INPUT_CLASS
    }))
        
    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': INPUT_CLASS
    }))
    
    priority = forms.ChoiceField(choices=CHOICES_PRIORITY, widget=forms.Select(attrs={
        'class': INPUT_CLASS
    }))
    
    status = forms.ChoiceField(choices=CHOICES_STATUS, widget=forms.Select(attrs={
        'class': INPUT_CLASS
    }))
    
class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': INPUT_CLASS
    }))
        
class AddFileForm(forms.ModelForm):
    class Meta:
        model = LeadFile
        fields = ('file',)