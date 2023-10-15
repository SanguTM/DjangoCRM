from django import forms
from .models import Ticket, Comment, TicketFile
from userprofile.models import UserProfile

class CreateTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('title', 'description',)

class UpdateTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('title', 'description', 'priority',)

class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        
class AddFileForm(forms.ModelForm):
    class Meta:
        model = TicketFile
        fields = ('file',)
        
class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('client',)