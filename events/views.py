from django.shortcuts import redirect, get_object_or_404
from django.db.models import Count, Q
from django.utils.timezone import now
from .models import Event, Category
from datetime import datetime
from events.forms import EventForm, CategoryForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from users.views import is_admin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.views import View


def is_organizer(user):
    return user.groups.filter(name="Organizer").exists()


def is_participant(user):
    return user.groups.filter(name="Participant").exists()


class IndexView(ListView):
    model = Event
    template_name = 'events/index.html'
    context_object_name = 'events'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        events = Event.objects.all()

        if query:
            events = events.filter(Q(name__icontains=query)
                                   | Q(location__icontains=query))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["upcoming_events"] = Event.objects.filter(
            date__gte=now().date())
        context["past_events"] = Event.objects.filter(
            date__lt=now().date()).order_by('-date')[:6]
        context['query'] = self.request.GET.get('q', '')
        return context


class SearchResultsView(ListView):
    model = Event
    template_name = 'events/search_results.html'
    context_object_name = 'events'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        return Event.objects.filter(Q(name__icontains=query) | Q(
            location__icontains=query)) if query else []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get('q', '')
        return context


class OrganizerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return is_organizer(self.request.user)

    def handle_no_permission(self):
        return redirect('no_permission')


class OrganizerDashboardView(OrganizerRequiredMixin, TemplateView):
    template_name = 'events/organizer_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_type = self.request.GET.get('type', 'today')
        category_id = self.request.GET.get('category')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        total_events = Event.objects.count()
        upcoming_events = Event.objects.filter(date__gte=now().date()).count()
        past_events = Event.objects.filter(date__lt=now().date()).count()

        total_event_participants = Event.objects.annotate(
            participant_count=Count('rsvps')
        ).aggregate(total=Count('rsvps'))['total']

        base_query = Event.objects.select_related(
            'category').prefetch_related('rsvps')

        if event_type == 'upcoming':
            events = base_query.filter(
                date__gte=now().date()).order_by('date', 'time')
        elif event_type == 'past':
            events = base_query.filter(
                date__lt=now().date()).order_by('-date', 'time')
        elif event_type == 'all':
            events = base_query.all().order_by('date', 'time')
        else:
            events = base_query.filter(date=now().date()).order_by('time')

        if category_id:
            events = events.filter(category_id=category_id)

        if start_date and end_date:
            try:
                start = datetime.strptime(start_date, '%Y-%m-%d').date()
                end = datetime.strptime(end_date, '%Y-%m-%d').date()
                events = events.filter(date__range=[start, end])
            except ValueError:
                pass

        context.update({
            'total_events': total_events,
            'upcoming_events': upcoming_events,
            'past_events': past_events,
            'todays_events': events if event_type == 'today' else base_query.filter(date=now().date()),
            'events': events,
            'current_type': event_type,
            'categories': Category.objects.all(),
            'selected_category': category_id,
            'start_date': start_date,
            'end_date': end_date,
            'total_event_participants': total_event_participants,
        })

        return context


# Event views
class CreateEventView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events/events_template/create_event.html'
    success_url = reverse_lazy('events:all_events')
    permission_required = 'events.add_event'

    def handle_no_permission(self):
        return redirect('no_permission')


class AllEventsView(ListView):
    model = Event
    template_name = 'events/events_template/all_events.html'
    context_object_name = 'events'


class UpdateEventView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events/events_template/create_event.html'
    success_url = reverse_lazy('events:all_events')
    permission_required = 'events.change_event'
    pk_url_kwarg = 'id'

    def handle_no_permission(self):
        return redirect('no_permission')


class DeleteEventView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Event
    template_name = 'events/events_template/delete_event.html'
    success_url = reverse_lazy('events:all_events')
    permission_required = 'events.delete_event'
    context_object_name = 'event'
    pk_url_kwarg = 'id'

    def handle_no_permission(self):
        return redirect('no_permission')


class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'
    pk_url_kwarg = 'id'


# Category views
class CreateCategoryView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'events/create_category.html'
    success_url = reverse_lazy('events:all_categories')

    def test_func(self):
        return self.request.user.groups.filter(name='Organizer').exists()


class AllCategoriesView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'events/categories.html'
    context_object_name = 'categories'


class UpdateCategoryView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'events/create_category.html'
    success_url = reverse_lazy('events:all_categories')
    pk_url_kwarg = 'id'

    def test_func(self):
        return self.request.user.groups.filter(name="Organizer").exists()


class DeleteCategoryView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category
    template_name = 'events/delete_category.html'
    success_url = reverse_lazy('events:all_categories')
    pk_url_kwarg = 'id'

    def test_func(self):
        return self.request.user.groups.filter(name="Organizer").exists()


class EventsByCategoryView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'events/events_by_category.html'
    context_object_name = 'events'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['id'])
        return Event.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


# RSVP
class RSVPEventView(LoginRequiredMixin, View):
    def send_rsvp_confirmation(self, user, event):
        subject = f"RSVP Confirmation for {event.name}"
        message = f"""
        Hello {user.username},

        You have successfully RSVPd for {event.name} on {event.date} at {event.time}.
        Location: {event.location}

        Thank you!
        """
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)

        if event.rsvps.filter(id=request.user.id).exists():
            messages.error(request, "You have already RSVPd for this event.")
        else:
            event.rsvps.add(request.user)
            self.send_rsvp_confirmation(request.user, event)
            messages.success(
                request, f"You have successfully RSVPd for {event.name}!")

        return redirect('events:event_detail', id=event.id)


class ParticipantDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'users/participant_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rsvp_events'] = self.request.user.rsvp_events.all()
        return context


@login_required
def dashboard(request):
    if is_admin(request.user):
        return redirect("admin_dashboard")
    elif is_organizer(request.user):
        return redirect("organizer_dashboard")
    elif is_participant(request.user):
        return redirect("participant_dashboard")

    return redirect("participant")
