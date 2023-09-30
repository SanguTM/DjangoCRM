from django.urls import path
from .import views

app_name = 'teams'

urlpatterns = [
    path('', views.teams_list, name='list'),
    path('<int:pk>/edit/', views.edit_team, name='edit'),
    path('<int:pk>/activate/', views.team_activate, name='activate'),
    path('<int:pk>/', views.team_detail, name='detail'),
    path('add-team/', views.team_add, name='add'),
]