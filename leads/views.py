from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from django.views import View

from client.models import Client, Comment as ClientComment, ClientFile
from team.models import Team

from .models import Lead

from .forms import AddLeadForm, AddCommentForm, AddFileForm


class ManagementRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_manager
    
    def handle_no_permission(self):
        messages.error(self.request, 'You have no access to the page')
        return redirect('dashboard:index')

class LeadListView(ManagementRequiredMixin, ListView):
    model = Lead
    
    def get_queryset(self):
        queryset = super(LeadListView, self).get_queryset()
        team = self.request.user.userprofile.active_team
        
        return queryset.filter(team=team) #is_client=False)
        
class LeadDetailView(ManagementRequiredMixin, DetailView):
    model = Lead
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddCommentForm()
        context['fileform'] = AddFileForm()
        
        return context
        
    #template_name = "leads/leads_detail.html"
    def get_queryset(self):
        queryset = super(LeadDetailView, self).get_queryset()
        team = self.request.user.userprofile.active_team
        
        #return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))
        return queryset.filter(team=team, pk=self.kwargs.get('pk'))
        
def leads_delete(request, pk):
    if request.user.is_manager:
        lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
        lead.delete()
    
        messages.success(request, 'The lead was deleted')
    
        return redirect('leads:list')
    else: 
        messages.error(request, 'You have no access to the page')
        return redirect('dashboard:index')


class LeadUpdateView(ManagementRequiredMixin, UpdateView):
    model = Lead
    form_class = AddLeadForm
    #fields = ('name', 'email', 'phone', 'description', 'priority', 'status')
    template_name = "leads/edit_lead.html"
    success_url = reverse_lazy('leads:list')
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'The lead was edited')
        return redirect(self.success_url)

    def get_queryset(self):
        queryset = super(LeadUpdateView, self).get_queryset()
        team = self.request.user.userprofile.active_team
        
        return queryset.filter(team=team, pk=self.kwargs.get('pk'))
    
class LeadCreateView(ManagementRequiredMixin, CreateView):
    model = Lead
    form_class = AddLeadForm
    #fields = ('name', 'email', 'phone', 'description', 'priority', 'status')
    template_name = "leads/add_lead.html"
    success_url = reverse_lazy('leads:list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.request.user.userprofile.active_team
        context['team'] = team
        context['title'] = 'Add lead'
        
        return context
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.team = self.request.user.userprofile.active_team
        self.object.save()
        
        messages.success(self.request, 'The lead was created')
        
        return redirect(self.success_url)
    
class LeadConvertView(ManagementRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        
        team = self.request.user.userprofile.active_team

        lead = get_object_or_404(Lead, pk=pk)
           
        client = Client.objects.create(
            name=lead.name,
            email=lead.email,
            phone=lead.phone,
            description=lead.description,
            created_by =request.user,
            team=lead.team,
        )
        
        lead.is_client = True
        lead.save()
        
        comments = lead.comments.all()
        files = lead.files.all()
        
        for comment in comments:
            ClientComment.objects.create(
                client = client,
                content = comment.content,
                created_by = comment.created_by,
                team = team
            )
            
        for file in files:
            ClientFile.objects.create(
                client = client,
                file = file.file,
                created_by = file.created_by,
                team = team
            )
        
        messages.success(request, 'The lead was converted to a client')
    
        return redirect('leads:list')
    
class AddCommentView(ManagementRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')         

        content = request.POST.get('content')
        
        form = AddCommentForm(request.POST)
        
        if form.is_valid():
            comment= form.save(commit=False)
            team = self.request.user.userprofile.active_team
            comment.team = team
            comment.created_by = request.user
            comment.lead_id = pk
            comment.save()
        
        return redirect('leads:detail', pk=pk)

class AddFileView(ManagementRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')         
        
        form = AddFileForm(request.POST, request.FILES)
        
        if form.is_valid():
            file = form.save(commit=False)
            team = self.request.user.userprofile.active_team
            file.team = team
            file.lead_id = pk
            file.created_by = request.user
            file.save()
        
        return redirect('leads:detail', pk=pk)
    

        
"""
@login_required
def leads_list(request):
    leads = Lead.objects.filter(created_by=request.user)
    #leads = Lead.objects.filter(created_by=request.user, is_client=False)
    
    return render(request, 'leads/lead_list.html', {
            'leads': leads
        })

@login_required
def leads_detail(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
    #lead = Lead.objects.filter(created_by=request.user).get(pk=pk)
    
    return render(request, 'leads/lead_detail.html', {
        'lead': lead
        })

@login_required
def leads_delete(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
    lead.delete()
    
    messages.success(request, 'The lead was deleted')
    
    return redirect('leads:list')

@login_required
def leads_edit(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
        
    if request.method == 'POST':
        form = AddLeadForm(request.POST, instance=lead)
        
        if form.is_valid():
            form.save()
            
            messages.success(request, 'The lead was edited')
        
            return redirect('leads:list')
    else:
        form = AddLeadForm(instance=lead)
        
    return render(request, 'leads/edit_lead.html', {
        'form': form
        })

@login_required
def add_lead(request):
    team = Team.objects.filter(created_by=request.user)[0]  
    
    if request.method == 'POST':
        form = AddLeadForm(request.POST)
        
        if form.is_valid():
            team = Team.objects.filter(created_by=request.user)[0]    
            
            lead = form.save(commit=False)
            lead.created_by = request.user
            lead.team = team
            lead.save()
            
            messages.success(request, 'The lead was created')

            return redirect('leads:list')
    else:
        form = AddLeadForm()    

    return render(request, 'leads/add_lead.html', {
        'form': form,
        'team': team
        })

@login_required
def leads_convert(request, pk):
    lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
    #team = Team.objects.filter(created_by=request.user)[0]    
    
    client = Client.objects.create(
        name=lead.name,
        email=lead.email,
        phone=lead.phone,
        description=lead.description,
        created_by =request.user,
        team=lead.team,
    )
    
    lead.is_client = True
    lead.save()
    
    messages.success(request, 'The lead was converted to a client')
    
    return redirect('leads:list')
"""