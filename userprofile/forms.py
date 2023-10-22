from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
#from django.contrib.auth.models import User
from user.models import User
from userprofile.models import UserProfile
from client.models import Client

INPUT_CLASS = 'w-full py-1.5 px-6 rounded-xl border'

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'first_name', 'last_name', 'password1', 'password2')
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': INPUT_CLASS
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Your email address',
        'class': INPUT_CLASS
    }))
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your phone number',
        'class': INPUT_CLASS
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your first name',
        'class': INPUT_CLASS
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your last name',
        'class': INPUT_CLASS
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': INPUT_CLASS
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repeat password',
        'class': INPUT_CLASS
    }))




class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': INPUT_CLASS
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': INPUT_CLASS
    }))
    
class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('client',)
        
    client = forms.ModelChoiceField(queryset=Client.objects.all(), widget=forms.Select(attrs={
        'class': INPUT_CLASS
    }))

        
class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'phone', 'first_name', 'last_name', 'password1')
    
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your first name',
        'class': INPUT_CLASS
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your last name',
        'class': INPUT_CLASS
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Your email address',
        'class': INPUT_CLASS
    }))
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your phone number',
        'class': INPUT_CLASS
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': INPUT_CLASS
    }))
