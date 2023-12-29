from django import forms
import django_filters
from ticket.models import Ticket
from leads.models import Lead

INPUT_CLASS = 'w-34 py-1.5 px-6 rounded-xl border font-semibold'

class TicketFilter(django_filters.FilterSet):
    ACTIVE = 'active'
    COMPLETED = 'completed'
    PENDING = 'pending'
    
    CHOICES_STATUS = (
        (ACTIVE, 'Active'),
        (COMPLETED, 'Completed'),
        (PENDING, 'Pending'),
    )

    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    
    CHOICES_PRIORITY = (
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    )    

    status = django_filters.ChoiceFilter(choices=CHOICES_STATUS, label='Filter by status or by priority', widget=forms.Select(attrs={
        'class': INPUT_CLASS
    }))
    priority = django_filters.ChoiceFilter(choices=CHOICES_PRIORITY, label='', widget=forms.Select(attrs={
        'class': INPUT_CLASS
    }))
    # https://github.com/carltongibson/django-filter/issues/341 - reikia prefix naudoti, jeigu daugiau nei vienas filtras tam paciam template
    def __init__(self, data=None, queryset=None, *, request=None, user=None, prefix=None):
            super().__init__(data=data, queryset=queryset, prefix="ticket")
            
    class Meta:
        model = Ticket
        fields = ('status', 'priority',)
        
        
class LeadFilter(django_filters.FilterSet):
    NEW = 'new'
    CONTACTED = 'contacted'
    WON = 'won'
    LOST = 'lost'
    
    CHOICES_LEAD_STATUS = (
        (NEW, 'New'),
        (CONTACTED, 'Contacted'),
        (WON, 'Won'),
        (LOST, 'Lost'),
    )

    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    
    CHOICES_PRIORITY = (
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    )
        
    
    status = django_filters.ChoiceFilter(choices=CHOICES_LEAD_STATUS, label='Filter by status or by priority', widget=forms.Select(attrs={
        'class': INPUT_CLASS
    }))
    priority = django_filters.ChoiceFilter(choices=CHOICES_PRIORITY, label='', widget=forms.Select(attrs={
        'class': INPUT_CLASS
    }))
    
    def __init__(self, data=None, queryset=None, *, request=None, user=None, prefix=None):
        super().__init__(data=data, queryset=queryset, prefix="lead")    

    class Meta:
        model = Lead
        fields = ('status', 'priority',)
