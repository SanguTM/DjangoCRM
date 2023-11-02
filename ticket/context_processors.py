from .models import Ticket

#sukuriame custom tagus templaitui
def pending_tickets(request):
    pending_tickets = 0
    
    if request.user.is_authenticated:
        if request.user.is_manager:
            pending_tickets = Ticket.objects.filter(status='pending')
        else:
            pending_tickets = pending_tickets
    else:
        pending_tickets = pending_tickets

    return {'pending_tickets': pending_tickets}

def workspace_tickets(request):
    if request.user.is_authenticated:
        workspace_tickets = Ticket.objects.filter(assign_to=request.user, is_resolved=False)
    else:
        workspace_tickets = 0
        
    return {'workspace_tickets': workspace_tickets}