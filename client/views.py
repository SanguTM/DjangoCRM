import csv

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import Client
from .forms import AddClientForm, AddCommentForm, AddFileForm

@login_required
def clients_list(request):
    team = request.user.userprofile.active_team
    clients = team.clients.all()
    #clients = Client.objects.filter(created_by=request.user)

    if request.user.is_manager:
        return render(request, 'client/clients_list.html', {
            'clients': clients
        })
    else: 
        messages.error(request, 'You have no access to the page')
        return redirect('dashboard:index')
    
@login_required
def clients_detail(request, pk):
    #client = get_object_or_404(Client, created_by=request.user, pk=pk)
    client = get_object_or_404(Client, pk=pk)
    #team = Team.objects.filter(created_by=request.user)[0]  
    if request.user.is_manager:
        if request.method == 'POST':
            form = AddCommentForm(request.POST)
        
            if form.is_valid():
                comment = form.save(False)
                comment.team = request.user.userprofile.active_team
                comment.created_by = request.user
                comment.client_id = pk
                comment.save()
            
                return redirect('clients:detail', pk=pk)
        else:
            form = AddCommentForm()
    
        return render(request, 'client/clients_detail.html', {
            'client': client,
            'form': form,
            'fileform':AddFileForm(),
        })
    else: 
        messages.error(request, 'You have no access to the page')
        return redirect('dashboard:index')

@login_required
def add_client(request):
    team = request.user.userprofile.active_team
    if request.user.is_manager:
        if request.method == 'POST':
            form = AddClientForm(request.POST)
        
            if form.is_valid():
                #team = Team.objects.filter(created_by=request.user)[0]            

                client = form.save(commit=False)
                client.created_by = request.user
                client.team = request.user.userprofile.active_team
                client.save()
            
                messages.success(request, 'The client was created')

                return redirect('clients:list')
        else:
            form = AddClientForm()    

        return render(request, 'client/add_client.html', {
            'form': form,
            'team': team
        })
    else: 
        messages.error(request, 'You have no access to the page')
        return redirect('dashboard:index')

@login_required
def clients_delete(request, pk):
    if request.user.is_manager:
        client = get_object_or_404(Client, created_by=request.user, pk=pk)
        client.delete()
    
        messages.success(request, 'The client was deleted')
    
        return redirect('clients:list')
    else: 
        messages.error(request, 'You have no access to the page')
        return redirect('dashboard:index')

@login_required
def clients_edit(request, pk):
    if request.user.is_manager:
        #client = get_object_or_404(Client, created_by=request.user, pk=pk)
        client = get_object_or_404(Client, pk=pk)
        
        if request.method == 'POST':
            form = AddClientForm(request.POST, instance=client)
        
            if form.is_valid():
                form.save()
            
                messages.success(request, 'The client was edited')
        
                return redirect('clients:list')
        else:
            form = AddClientForm(instance=client)
        
        return render(request, 'client/edit_client.html', {
            'form': form
            })
    else: 
        messages.error(request, 'You have no access to the page')
        return redirect('dashboard:index')

@login_required
def client_add_file(request, pk):
    if request.user.is_manager:
        client = get_object_or_404(Client, pk=pk)
        #team = Team.objects.filter(created_by=request.user)[0]
    
        if request.method == 'POST':
            form = AddFileForm(request.POST, request.FILES)
        
            if form.is_valid():
                file = form.save(commit=False)
                file.team = request.user.userprofile.active_team
                file.client_id = pk
                file.created_by = request.user
                file.save()
        
                return redirect('clients:detail', pk=pk)
        return redirect('clients:detail', pk=pk)
    else: 
        messages.error(request, 'You have no access to the page')
        return redirect('dashboard:index')

@login_required
def client_export_to_CSV(request):
    if request.user.is_manager:
        clients = Client.objects.all()
    
        response = HttpResponse(
            content_type = 'text/csv',
            headers= {'Content-Disposition': 'attachment; filename="clients.csv"'},
        )
    
        writer = csv.writer(response)
        writer.writerow(['Client name', 'Email', 'Phone', 'Description', 'Created by', 'Creted at'])
    
        for client in clients:
            writer.writerow([client.name, client.email, client.phone, client.description, client.created_by, client.created_at])
        
        return response
    else: 
        messages.error(request, 'You have no access to the page')
        return redirect('dashboard:index')