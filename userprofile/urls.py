from django.urls import path
from .import views

app_name = 'userprofile'

urlpatterns = [
    path('user_account/', views.user_account, name='user_account'),
    path('sign-up/', views.signup, name='signup'),
    path('<int:pk>/edit-profile/', views.update_profile, name='edit-profile'),
    path('userlist/', views.user_list, name='list'),
    path('<int:pk>/', views.user_detail, name='detail'),
]
    