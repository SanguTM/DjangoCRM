"""
Definition of views.
"""
""
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest

from leads.models import Lead
from client.models import Client
from ticket.models import Ticket
from chat.models import Room

"""
def home(request):
    #Renders the home page
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )
   """ 


def index(request):
    if request.user.is_authenticated:
        if request.user.is_manager:
            team = request.user.userprofile.active_team
            ##rodo paskutinius 5 sukurtus leads ir clients
            leads = Lead.objects.filter(team=team).order_by('-created_at')[0:5]
            clients = Client.objects.filter(team=team).order_by('-created_at')[0:5]
            tickets = Ticket.objects.filter(assign_to=request.user, is_resolved=False)[0:5]
            rooms = Room.objects.filter(status=Room.WAITING)
      
            return render(request, 'dashboard/dashboard.html', {
                'leads': leads,
                'clients': clients,
                'tickets': tickets,
                'rooms': rooms,
            })
        if request.user.is_customer:
            tickets = Ticket.objects.filter(created_by=request.user, is_resolved=False)[0:5]
        
            return render(request, 'dashboard/dashboard.html', {
                'tickets': tickets,
            })
    else:
        return redirect('/log-in')

def about(request):
    return render(request, 'app/about.html')

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

"""
def about(request):
    #Renders the about page.
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
"""