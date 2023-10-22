from django.urls import path
from .import views

app_name = 'leads'

urlpatterns = [
    #path('', views.leads_list, name='list'),
    path('', views.LeadListView.as_view(), name='list'),
    #path('<int:pk>/', views.leads_detail, name='detail'),
    path('<int:pk>/', views.LeadDetailView.as_view(), name='detail'),
    path('<int:pk>/delete/', views.leads_delete, name='delete'),
    #path('<int:pk>/delete/', views.LeadDeleteView.as_view(), name='delete'),
    #path('<int:pk>/edit/', views.leads_edit, name='edit'),
    path('<int:pk>/edit/', views.LeadUpdateView.as_view(), name='edit'),
    #path('<int:pk>/convert/', views.leads_convert, name='convert'),
    path('<int:pk>/convert/', views.LeadConvertView.as_view(), name='convert'),
    path('add-lead/', views.LeadCreateView.as_view(), name='add'),
    path('<int:pk>/add-comment/', views.AddCommentView.as_view(), name='add-comment'),
    path('<int:pk>/add-file/', views.AddFileView.as_view(), name='add-file'),
    #path('add-lead/', views.add_lead, name='add'),
]