from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from leads.models import Lead
from client.models import Client
from ticket.models import Ticket
from chat.models import Room
from .filters import TicketFilter, LeadFilter

# Create your views here.

@login_required
def dashboard(request):
    if request.user.is_manager:
        team = request.user.userprofile.active_team
        ##rodo paskutinius 5 sukurtus leads ir clients
        leads = Lead.objects.filter(team=team).order_by('-created_at')[0:5]
        clients = Client.objects.filter(team=team).order_by('-created_at')[0:5]
        tickets = Ticket.objects.filter(assign_to=request.user, is_resolved=False)[0:5]
        rooms = Room.objects.filter(status=Room.WAITING)
        ticketFilter = TicketFilter(request.GET, queryset=Ticket.objects.filter(assign_to=request.user, is_resolved=False))
        leadFilter = LeadFilter(request.GET, Lead.objects.filter(team=team).order_by('-created_at'))
      
        return render(request, 'dashboard/dashboard.html', {
            'leads': leads,
            'clients': clients,
            'tickets': tickets,
            'rooms': rooms,
            'filter': ticketFilter,
            'leadFilter': leadFilter,
        })
    if request.user.is_customer:
        tickets = Ticket.objects.filter(created_by=request.user, is_resolved=False)[0:5]
        ticketFilter = TicketFilter(request.GET, queryset=Ticket.objects.filter(created_by=request.user, is_resolved=False))
        
        return render(request, 'dashboard/dashboard.html', {
            'tickets': tickets,
            'filter': ticketFilter
        })