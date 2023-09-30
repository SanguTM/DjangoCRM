from django.contrib import admin
from .models import Client, ClientFile, Comment

admin.site.register(Client)
admin.site.register(Comment)
admin.site.register(ClientFile)