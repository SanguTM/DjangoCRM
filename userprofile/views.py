from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from team.models import Team
from userprofile.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import SignupForm

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
    return render(request, 'userprofile/user_account.html')