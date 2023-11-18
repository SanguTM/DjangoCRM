from django.contrib import admin
from .models import Email, EmailSetting
from django import forms

#https://stackoverflow.com/questions/72208458/django-admin-editable-but-hidden-field
class EmailSettingForm(forms.ModelForm):
    class Meta:
        model = EmailSetting
        widgets = {
            'email_host': forms.TextInput,
            'email_port': forms.TextInput,
            'email_from_email': forms.TextInput,
            'email_host_user': forms.TextInput,
            'email_host_password': forms.PasswordInput,
        }
        fields = '__all__'
        
class EmailSettingAdmin(admin.ModelAdmin):
    form = EmailSettingForm

# Register your models here.
admin.site.register(Email)
admin.site.register(EmailSetting, EmailSettingAdmin)