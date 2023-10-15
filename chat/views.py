import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from user.models import User
from django.contrib import messages

# Create your views here.

from .models import Room

@require_POST
def create_room(request, uuid):
    name = request.POST.get('name', '')
    url = request.POST.get('url', '')
    
    Room.objects.create(uuid=uuid, chat_user=name, url=url)
    
    return JsonResponse({'message': 'room created'})

@login_required
def admin(request):
    rooms = Room.objects.all()
    users = User.objects.all()
    
    return render(request, 'chat/admin.html', {
        'rooms': rooms,
        'users': users
    })

@login_required
def room(request, uuid):
    room = get_object_or_404(Room, uuid=uuid)
    
    if room.status == Room.WAITING:
        room.status = Room.ACTIVE
        room.agent = request.user
        room.save()
    
    return render(request, 'chat/room.html', {
        'room': room    
    })
    

@login_required
def room_delete(request, uuid):
    if request.user.is_manager:
        room = get_object_or_404(Room, uuid=uuid)
        room.delete()
    
        messages.success(request, 'The room was deleted')
    
        return redirect('chat:admin')
    else: 
        messages.error(request, 'You have no access to the page')
        return redirect('dashboard:index')