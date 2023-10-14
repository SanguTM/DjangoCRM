"""
Definition of views.
"""
""
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest

from leads.models import Lead
from client.models import Client

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
        team = request.user.userprofile.active_team
        ##rodo paskutinius 5 sukurtus leads ir clients
        leads = Lead.objects.filter(team=team).order_by('-created_at')[0:5]
        clients = Client.objects.filter(team=team).order_by('-created_at')[0:5]
   
    
        return render(request, 'dashboard/dashboard.html', {
            'leads': leads,
            'clients': clients,
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