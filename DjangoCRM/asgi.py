"""
ASGI config for jatte project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
import django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'DjangoCRM.settings')

django.setup()

from chat import routing
#from django.contrib.auth.models import User
from user.models import User
from userprofile.models import UserProfile 
from team.models import Team


#application = get_asgi_application()
django_asgi_application = get_asgi_application()

application = ProtocolTypeRouter(
    {
        'http': django_asgi_application,
        'websocket': AllowedHostsOriginValidator(AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns)))
    }    
)

#https://stackoverflow.com/questions/6244382/how-to-automate-createsuperuser-on-django
users = User.objects.all()
if not users:
    user = User.objects.create_superuser(username="sangu", email="", password="Qwer7894", is_active=True, is_staff=True)
    
    #user = User.objects.all().first()
    team = Team.objects.create(name='Superteam', created_by=user)
    team.members.add(user)  
    UserProfile.objects.create(user=user, active_team=team)
    userprofile = user.userprofile
    userprofile.active_team = team
