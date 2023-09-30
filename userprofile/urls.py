from django.urls import path
from .import views

app_name = 'userprofile'

urlpatterns = [
    path('user_account/', views.user_account, name='user_account'),
    path('sign-up/', views.signup, name='signup'),
]
    