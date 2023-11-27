import datetime
import random
from sqlite3 import IntegrityError
import string
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.core.mail import get_connection, send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail.backends.smtp import EmailBackend

import ticket
from .models import Ticket
from .form import *
from user.models import User
from userprofile.models import UserProfile
from notification.models import Email, EmailSetting
from dashboard.filters import TicketFilter
# Create your views here.

#https://stackoverflow.com/questions/37219601/how-can-i-get-the-email-configuration-from-the-db
# Custom email backend

@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    user = User.objects.get(username = ticket.created_by)
    user_tickets = Ticket.objects.filter(created_by=user)
    user_profile = UserProfile.objects.get(user=user)
    url = request.build_absolute_uri()
    #user_tickets = ticket.created_by.all().user

    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(False)
            comment.created_by = request.user
            comment.ticket_id = pk
            comment.save()

            subject = "Ticket "+ ticket.ticket_number + " received new comment"  
            comment_user = User.objects.get(username = comment.created_by).email
            
            settings = EmailSetting.objects.first()

            if settings:
                connection = get_connection(
                        host=settings.email_host,
                        port=settings.email_port,
                        use_tls=settings.email_use_tls,
                        from_email = settings.email_from_email,
                        username=settings.email_host_user,
                        password=settings.email_host_password)
                
            if settings:
                if comment.ticket.assign_to:
                    assign_user = User.objects.get(username = ticket.assign_to).email
                else:
                    assign_user = ''
                
                if comment_user == user and comment.ticket.assign_to:
                    recipent_list = [
                        assign_user,
                    ]
            
                elif assign_user == comment_user and comment.ticket.assign_to:
                    recipent_list = [
                        user.email,
                    ]
                else:
                    recipent_list = [
                        user.email,
                        comment_user,
                        assign_user,
                        ]
                    
                context = {
                    "ticket": ticket, 
                    "url": url
                }   

                html = render_to_string('notification/new_comment_mail.html', context=context)
                plain_message = strip_tags(html)

                message = EmailMultiAlternatives(
                    subject = subject,
                    body = plain_message,
                    #message = message,
                    to = recipent_list,
                    #from_email = 'Django CRM support',
                    connection=connection
                )
                
                message.attach_alternative(html, 'text/html')
                message.send()
                
                #send_mail(
                #    subject = subject,
                #    message = message,
                #    recipient_list = recipent_list,
                #    from_email = 'Django CRM support',
                #    connection=connection
                #)

                message = "Ticket received new comment. Check it here: " + url
                Email.objects.create(subject=subject, message=message, email = recipent_list)
               
            return redirect('tickets:detail', pk=pk)
    else:
        form = AddCommentForm()
    
    return render(request, 'ticket/ticket_detail.html', {
        'ticket': ticket,
        'user': user,
        'user_tickets': user_tickets,
        'user_profile': user_profile,
        'form': form,
        'fileform': AddFileForm(),
        'closeticket': CloseTicketForm(),
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
            while not ticket.ticket_number:
                id = ''.join(random.choices(string.digits, k=6))
                try:
                    ticket.ticket_number = id
                    ticket.save()
                    break
                except IntegrityError:
                    continue
            #ticket.save()
            
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
        ticketFilter = TicketFilter(request.GET, queryset=Ticket.objects.all())
    else:
        tickets = Ticket.objects.filter(created_by=request.user)
        ticketFilter = TicketFilter(request.GET, queryset=Ticket.objects.filter(created_by=request.user))
    
    return render(request, 'ticket/tickets_list.html', {
        'tickets': tickets,
        'filter': ticketFilter,
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
        
        settings = EmailSetting.objects.first()

        if settings:
            connection = get_connection(
                    host=settings.email_host,
                    port=settings.email_port,
                    use_tls=settings.email_use_tls,
                    from_email = settings.email_from_email,
                    username=settings.email_host_user,
                    password=settings.email_host_password)
                
        if settings:
            url = request.build_absolute_uri()
            url = url[:-6]
            subject = "Ticket: " + ticket.ticket_number + " was closed"
            message = "Ticket received new comment. Check it here: " + url
            user = User.objects.get(username = ticket.created_by)
            recipent_list = [
                user.email
            ]

            context = {
                "ticket": ticket, 
                "url": url
            }
            
            html = render_to_string('notification/ticked_resolved_mail.html', context=context)
            plain_message = strip_tags(html)            

            message = EmailMultiAlternatives(
                    subject = subject,
                    body = plain_message,
                    #message = message,
                    to = recipent_list,
                    #from_email = 'Django CRM support',
                    connection=connection
                )
                
            message.attach_alternative(html, 'text/html')
            message.send()
                
            message = "Ticket received new comment. Check it here: " + url

            Email.objects.create(subject=subject, message=message, email = recipent_list)
            
        if request.method == 'POST':      
            form = CloseTicketForm(request.POST, instance=ticket)
        
            if form.is_valid():
                form.save()
                messages.success(request, 'The ticket was closed')      
        else:
            form = CloseTicketForm(instance=ticket)
    
        return redirect('tickets:queue')
    else: 
        messages.error(request, 'You have no access to the page')
        return redirect('dashboard:index')

@login_required
def ticket_workspace(request):
    if request.user.is_manager:
        #tickets = get_list_or_404(Ticket, assign_to=request.user, is_resolved=False)
        tickets = Ticket.objects.filter(assign_to=request.user, is_resolved=False)
        ticketFilter = Ticket.objects.filter(assign_to=request.user, is_resolved=False)
    
        return render(request, 'ticket/tickets_workspace.html', {
            'tickets': tickets,
            'filter': ticketFilter,
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
    ticket = get_object_or_404(Ticket, pk=pk)
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

class SearchResultsList(LoginRequiredMixin, ListView):
    model = Ticket
    context_object_name = "tickets"
    template_name = "ticket/ticket_search.html"

    def get_queryset(self):
        tickets = self.request.GET.get("q", None)
        if ticket:
            return Ticket.objects.filter(
                Q(title__icontains=tickets) | Q(description__icontains=tickets)
            )
