from django import forms
from .models import Client, ClientFile, Comment

INPUT_CLASS = 'w-full py-1.5 px-6 rounded-xl border'

class AddClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('name', 'email', 'phone', 'description',)
        
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': INPUT_CLASS
    }))
    
    email = forms.EmailField(required=False, widget=forms.TextInput(attrs={
        'class': INPUT_CLASS
    }))
    
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': INPUT_CLASS
    }))
        
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': INPUT_CLASS
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
        model = ClientFile
        fields = ('file',)
        