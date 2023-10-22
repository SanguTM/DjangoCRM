from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from team.models import Team
from userprofile.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import SignupForm, UpdateProfileForm, UpdateUserForm
from user.models import User
from django.contrib import messages

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_customer = True
            user.is_manager = False
            user = form.save()
            
            #sukuriam user, issiloginam nes kitaip gausim annonomous user su id 0 ir tik tada darom su juo veiksmus
            login(request, user)
            team = Team.objects.create(name='The team name', created_by=user)
            team.members.add(user)
            
            team.save()
            
            UserProfile.objects.create(user=user, active_team=team)

            return redirect('/log-in')
    else:
        form = SignupForm()

    return render(request, 'userprofile/signup.html', {
        'form': form
        })

@login_required
def user_account(request):
    team = request.user.userprofile.active_team
    user = request.user
    
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=user) 
        
        if form.is_valid():
            form.save()
            messages.success(request, 'The profile was edited')
            
            return redirect('userprofile:user_account')
        
    else:
        form = UpdateUserForm(instance=user)   

    client = request.user.userprofile.client
    return render(request, 'userprofile/user_account.html', {
        'team': team,
        'client': client,
        'form': form,
    })

@login_required
def update_profile(request, pk):
    profile = get_object_or_404(UserProfile, pk=pk)
    user = profile.user
    
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=profile) 
        
        if form.is_valid():
            form.save()
            
            return redirect('userprofile:list')
        
    else:
        form = UpdateProfileForm(instance=profile)
        
    return render(request, 'userprofile/edit_profile.html', {
        'form': form,
        'user': user,
        })
        
@login_required
def user_list(request):
    user_profiles = UserProfile.objects.filter(user__is_customer=True)
    
    #user_profiles = UserProfile.objects.filter()

    if request.user.is_manager:
        return render(request, 'userprofile/user_list.html', {
            #'users': users,
            'user_profiles': user_profiles,
        })
    else: 
        messages.error(request, 'You have no access to the page')
        return redirect('dashboard:index')       


@login_required
def user_detail(request, pk):
    #client = get_object_or_404(Client, created_by=request.user, pk=pk)
    user = get_object_or_404(User, pk=pk)
    user_profile = UserProfile.objects.get(user=user)

    #team = Team.objects.filter(created_by=request.user)[0]  
    if request.user.is_manager:
    
        return render(request, 'userprofile/user_detail.html', {
            'user': user,
            'user_profile': user_profile,
        })
    else: 
        messages.error(request, 'You have no access to the page')
        return redirect('dashboard:index')