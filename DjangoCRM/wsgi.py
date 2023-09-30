"""
WSGI config for DjangoCRM project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

For more information, visit
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'DjangoCRM.settings')

from django.contrib.auth.models import User
from team.models import Team
from userprofile.models import UserProfile

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
application = get_wsgi_application()

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
