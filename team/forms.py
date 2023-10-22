from django import forms
from .models import Team

from user.models import User

INPUT_CLASS = 'w-full py-1.5 px-6 rounded-xl border'

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name','members',)
        
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': INPUT_CLASS
    }))
    
    members = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=forms.SelectMultiple(attrs={
        'class': INPUT_CLASS
    }))