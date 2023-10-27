import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from .models import Ticket
from .form import *
from user.models import User
from userprofile.models import UserProfile
# Create your views here.

@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    user = User.objects.get(username = ticket.created_by)
    user_tickets = Ticket.objects.filter(created_by=user)
    user_profile = UserProfile.objects.get(user=user)
    #user_tickets = ticket.created_by.all().user
    
    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(False)
            comment.created_by = request.user
            comment.ticket_id = pk
            comment.save()
            
            return redirect('tickets:detail', pk=pk)
    else:
        form = AddCommentForm()
    
    return render(request, 'ticket/ticket_detail.html', {
        'ticket': ticket,
        'user_tickets': user_tickets,
        'user_profile': user_profile,
        'form': form,
        'fileform':AddFileForm(),
    })

# Kliento dalis
@login_required
def add_ticket(request):
    if request.method == 'POST':
        form = CreateTicketForm(request.POST)
        
        if form.is_valid():
            
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.status = 'pending' 
            ticket.save()
            
            messages.success(request, 'The ticket was created')
            
            return redirect('tickets:list')
        
    else:
        form = CreateTicketForm()
    
    return render(request, 'ticket/add_ticket.html', {
        'form': form,
    })

@login_required
def edit_ticket(request, pk):
    #ticket = get_object_or_404(Ticket, created_by=request.user, pk=pk)  
    ticket = get_object_or_404(Ticket, pk=pk)  
     
    if request.method == 'POST':      
        form = UpdateTicketForm(request.POST, instance=ticket)
        
        if form.is_valid():
            form.save()
        
            messages.success(request, 'The ticket was edited')
            
            return redirect('tickets:list')
            
    else:
        form = UpdateTicketForm(instance=ticket)
        if request.user.is_manager:
            form.fields['title'].disabled = True
            form.fields['description'].disabled = True
        if request.user.is_customer:
            form.fields['status'].disabled = True
            
    return render(request, 'ticket/edit_ticket.html', {
        'form': form
        })   

@login_required
def ticket_list(request):
    #tickets = get_list_or_404(Ticket, created_by=request.user)
    if request.user.is_manager:
        tickets = Ticket.objects.all()
    else:
        tickets = Ticket.objects.filter(created_by=request.user)
    
    return render(request, 'ticket/tickets_list.html', {
        'tickets': tickets      
    })

@login_required
def tickets_delete(request, pk):
    ticket = get_object_or_404(Ticket, created_by=request.user, pk=pk)
    ticket.delete()
    
    messages.success(request, 'The ticket was deleted')
    
    return redirect('tickets:list')


# Vadybai
@login_required
def ticket_queue(request):
    if request.user.is_manager:
        tickets = Ticket.objects.filter(status='pending')
    
        return render(request, 'ticket/tickets_queue.html', {
            'tickets': tickets      
        })
    else: 
        messages.error(request, 'You have no access to the page')
        return redirect('dashboard:index')

@login_required
def ticket_accept(request, pk):
    if request.user.is_manager:
        ticket = get_object_or_404(Ticket, pk=pk)
        ticket.assign_to = request.user
        ticket.status = 'active'
        ticket.accepted_at = datetime.datetime.now()
        ticket.save()
    
        return redirect('tickets:queue')
    else: 
        messages.error(request, 'You have no access to the page')
        return redirect('dashboard:index')

@login_required
def ticket_close(request, pk):
    if request.user.is_manager:
        ticket = get_object_or_404(Ticket, pk=pk)
        ticket.status = 'completed'
        ticket.is_resolved = True
        ticket.closed_at = datetime.datetime.now()
        ticket.save()
    
        return redirect('tickets:queue')
    else: 
        messages.error(request, 'You have no access to the page')
        return redirect('dashboard:index')

@login_required
def ticket_workspace(request):
    if request.user.is_manager:
        #tickets = get_list_or_404(Ticket, assign_to=request.user, is_resolved=False)
        tickets = Ticket.objects.filter(assign_to=request.user, is_resolved=False)
    
        return render(request, 'ticket/tickets_workspace.html', {
            'tickets': tickets
        })
    else: 
        messages.error(request, 'You have no access to the page')
        return redirect('dashboard:index')

@login_required
def tickets_resolved(request):
    if request.user.is_manager:
        tickets = Ticket.objects.filter(is_resolved=True)
    
        return render(request, 'ticket/tickets_resolved.html', {
            'tickets': tickets
        })
    else: 
        messages.error(request, 'You have no access to the page')
        return redirect('dashboard:index')


@login_required
def ticket_add_file(request, pk):
    ticket = get_object_or_404(Ticket, created_by=request.user, pk=pk)
    #team = Team.objects.filter(created_by=request.user)[0]
    
    if request.method == 'POST':
        form = AddFileForm(request.POST, request.FILES)
        
        if form.is_valid():
            file = form.save(commit=False)
            file.ticket_id = pk
            file.created_by = request.user
            file.save()
        
            return redirect('tickets:detail', pk=pk)
    return redirect('tickets:detail', pk=pk)
