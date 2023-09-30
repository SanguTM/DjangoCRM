from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from team.models import Team
from userprofile.models import UserProfile
from .forms import TeamForm

@login_required
def edit_team(request, pk):
    team = get_object_or_404(Team, created_by=request.user, pk=pk)
    
    if request.method == 'POST':
        form = TeamForm(request.POST, instance=team)
        
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Team was edited')

            return redirect('userprofile:user_account')
    else:
        form = TeamForm(instance=team)
    
    return render(request, 'team/edit_team.html', {
        'team': team,
        'form': form
    })

@login_required
def team_detail(request, pk):
    team = get_object_or_404(Team, members__in=[request.user], pk=pk)
    
    return render(request, 'team/team_detail.html', {'team': team})

@login_required
def teams_list(request):
    teams = Team.objects.filter(members__in=[request.user])

    return render(request, 'team/team_list.html', {'teams': teams})

@login_required
def team_activate(request, pk):
    team = Team.objects.filter(members__in=[request.user]).get(pk=pk)
    userprofile = request.user.userprofile
    userprofile.active_team = team
    userprofile.save()
    
    return redirect('teams:detail', pk=pk)
    #return redirect('teams:list')

@login_required
def team_add(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        
        if form.is_valid():
            team = form.save(commit=False)
            team.created_by = request.user   
            team.save()
            team.members.add(request.user)            

            userprofile = request.user.userprofile
            userprofile.active_team = team
            userprofile.save()
        
            messages.success(request, 'The team was created')
            
            return redirect('teams:list')
        
    else:
        form = TeamForm()
            
    return render(request, 'team/add_team.html', {
        #'team': team,
        'form': form
    })

