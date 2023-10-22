from django.urls import path
from .import views

app_name = 'tickets'

urlpatterns = [
    path('', views.ticket_list, name='list'),
    path('<int:pk>/', views.ticket_detail, name='detail'),
    path('add-ticket/', views.add_ticket, name='add'),
    path('queue/', views.ticket_queue, name='queue'),
    path('workspace/', views.ticket_workspace, name='workspace'),
    path('resolved/', views.tickets_resolved, name='resolved'),
    path('<int:pk>/edit/', views.edit_ticket, name='edit'),
    path('<int:pk>/delete/', views.tickets_delete, name='delete'),
    path('<int:pk>/accept/', views.ticket_accept, name='accept'),
    path('<int:pk>/close/', views.ticket_close, name='close'),
    path('<int:pk>/add-comment/', views.ticket_detail, name='add-comment'),
    path('<int:pk>/add-file/', views.ticket_add_file, name='add-file'),
]
