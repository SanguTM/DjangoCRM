from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from leads.models import Lead
from client.models import Client
from ticket.models import Ticket
from chat.models import Room


# Create your views here.

@login_required
def dashboard(request):
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