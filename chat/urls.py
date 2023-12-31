from django.urls import path
from .import views

app_name = 'chat'

urlpatterns = [
    path('api/create-room/<str:uuid>/', views.create_room, name='create-room'),
    path('chat-admin', views.chat_admin, name='admin'),
    path('chat-admin/<str:uuid>/', views.room, name='room'),
    path('chat-admin/<str:uuid>/delete/', views.room_delete, name='delete'),
]
    