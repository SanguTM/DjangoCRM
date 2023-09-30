from .models import Team

#sukuriame custom tagus templaitui
def active_team(request):
    if request.user.is_authenticated:
        if request.user.userprofile.active_team:
            active_team = request.user.userprofile.active_team
        else:
            active_team = Team.objects.filter(created_by=request.user)[0]
            #active_team = None
    else:
        active_team = None
    
    return {'active_team': active_team}