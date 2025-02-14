from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils import timezone
from django.db.models import Q, Count
from .models import Event, Participant, Category
from .forms import EventForm, ParticipantForm, CategoryForm

class HompageView(ListView):
    model = Category
    template_name = 'events/category_list.html'
    context_object_name = 'categories'

class CategoryListView(ListView):
    model = Category
    template_name = 'events/category_list.html'
    context_object_name = 'categories'

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'events/category_detail.html'
    context_object_name = 'category'

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'events/category_form.html'
    success_url = reverse_lazy('category_list')

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'events/category_form.html'
    success_url = reverse_lazy('category_list')

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'events/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')

class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'

    def get_queryset(self):
        queryset = Event.objects.annotate(participant_count=Count('participants'))
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | 
                Q(location__icontains=search_query)
            )
        
        return queryset

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['participants'] = self.object.participants.all()
        return context

class EventCreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('event_list')

class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('event_list')

class EventDeleteView(DeleteView):
    model = Event
    template_name = 'events/event_confirm_delete.html'
    success_url = reverse_lazy('event_list')

class ParticipantListView(ListView):
    model = Participant
    template_name = 'events/participant_list.html'
    context_object_name = 'participants'

class ParticipantDetailView(DetailView):
    model = Participant
    template_name = 'events/participant_detail.html'
    context_object_name = 'participant'

class ParticipantCreateView(CreateView):
    model = Participant
    form_class = ParticipantForm
    template_name = 'events/participant_form.html'
    success_url = reverse_lazy('participant_list')

class ParticipantUpdateView(UpdateView):
    model = Participant
    form_class = ParticipantForm
    template_name = 'events/participant_form.html'
    success_url = reverse_lazy('participant_list')

class ParticipantDeleteView(DeleteView):
    model = Participant
    template_name = 'events/participant_confirm_delete.html'
    success_url = reverse_lazy('participant_list')

def dashboard(request):
    today = timezone.now().date()
    total_participants = Participant.objects.count()
    total_events = Event.objects.count()
    upcoming_events = Event.objects.filter(date__gte=today).count()
    past_events = Event.objects.filter(date__lt=today).count()
    today_events = Event.objects.filter(date=today)

    show_type = request.GET.get('show', 'today')
    if show_type == 'all':
        events = Event.objects.all()
    elif show_type == 'upcoming':
        events = Event.objects.filter(date__gte=today)
    elif show_type == 'past':
        events = Event.objects.filter(date__lt=today)
    else:
        events = today_events
    
    context = {
        'total_participants': total_participants,
        'total_events': total_events,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'today_events': today_events,
        'events': events,
        'show_type': show_type,
    }
    
    return render(request, 'events/dashboard.html', context)


def homepage(request):
    today = timezone.now().date()
    upcoming_events = Event.objects.filter(date__gte=today).order_by('date')[:4]
    past_events = Event.objects.filter(date__lt=today).order_by('-date')[:4]
    categories = Category.objects.annotate(event_count=Count('events'))
    total_events = Event.objects.count()
    total_participants = Participant.objects.count()
    
    context = {
        'upcoming_events': upcoming_events,
        'categories': categories,
        'total_events': total_events,
        'past_events': past_events,
        'total_participants': total_participants,
    }
    
    return render(request, 'events/homepage.html', context)