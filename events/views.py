from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q
from django.utils.timezone import now
from .models import Event, Category
from datetime import datetime
from events.forms import EventForm, CategoryForm
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from users.views import is_admin


def is_organizer(user):
    return user.groups.filter(name="Organizer").exists()


def is_participant(user):
    return user.groups.filter(name="Participant").exists()


def index(request):
    query = request.GET.get('q', '')
    events = Event.objects.all()

    if query:
        events = events.filter(Q(name__icontains=query)
                               | Q(location__icontains=query))

    categories = Category.objects.all()
    # participants = Participant.objects.all()
    upcoming_events = Event.objects.filter(date__gte=now().date())
    past_events = Event.objects.filter(
        date__lt=now().date()).order_by('-date')[:6]

    context = {
        'events': events,
        'categories': categories,
        # 'participants': participants,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'query': query,
    }

    return render(request, 'events/index.html', context)


def search_results(request):
    query = request.GET.get('q', '')
    events = Event.objects.filter(Q(name__icontains=query) | Q(
        location__icontains=query)) if query else []

    context = {
        'events': events,
        'query': query,
    }

    return render(request, 'events/search_results.html', context)


@user_passes_test(is_organizer, login_url='no_permission')
def organizer_dashboard(request):
    event_type = request.GET.get('type', 'today')
    category_id = request.GET.get('category')

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # total_participants = Participant.objects.count()
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

    categories = Category.objects.all()

    context = {
        'total_events': total_events,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'todays_events': events if event_type == 'today' else base_query.filter(date=now().date()),
        'events': events,
        'current_type': event_type,
        'categories': categories,
        'selected_category': category_id,
        'start_date': start_date,
        'end_date': end_date,
        'total_event_participants': total_event_participants,
    }

    return render(request, 'events/organizer_dashboard.html', context)


# Event views
@login_required
@permission_required("events.add_event", login_url="no_permission")
def create_event(request):
    form = EventForm(request.POST or None, request.FILES)
    if form.is_valid():
        form.save()
        return redirect('events:all_events')
    context = {
        'form': form,
    }
    return render(request, 'events/events_template/create_event.html', context)


def all_events(request):
    events = Event.objects.all()
    context = {
        'events': events,
    }
    return render(request, 'events/events_template/all_events.html', context)


@login_required
@permission_required("events.change_event", login_url="no_permission")
def update_event(request, id):
    event = Event.objects.get(id=id)
    form = EventForm(request.POST or None,
                     request.FILES or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('events:all_events')
    context = {
        'event': event,
        'form': form,
    }
    return render(request, 'events/events_template/create_event.html', context)


@login_required
@permission_required("events.delete_event", login_url="no_permission")
def delete_event(request, id):
    event = Event.objects.get(id=id)
    if request.method == 'POST':
        event.delete()
        return redirect('events:all_events')
    context = {
        'event': event,
    }
    return render(request, 'events/events_template/delete_event.html', context)


def event_detail(request, id):
    event = Event.objects.get(id=id)
    context = {
        'event': event,
    }
    return render(request, 'events/event_detail.html', context)


# Category views
@user_passes_test(is_organizer, login_url='no_permission')
def create_category(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('events:all_categories')
    context = {
        'form': form,
    }
    return render(request, 'events/create_category.html', context)


@login_required
def all_categories(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'events/categories.html', context)


@user_passes_test(is_organizer, login_url='no_permission')
def update_category(request, id):
    category = Category.objects.get(id=id)
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect('events:all_categories')
    context = {
        'category': category,
        'form': form,
    }
    return render(request, 'events/create_category.html', context)


@user_passes_test(is_organizer, login_url='no_permission')
def delete_category(request, id):
    category = Category.objects.get(id=id)
    if request.method == 'POST':
        category.delete()
        return redirect('events:all_categories')
    context = {
        'category': category,
    }
    return render(request, 'events/delete_category.html', context)


@login_required
def events_by_category(request, id):
    category = Category.objects.get(id=id)
    events = Event.objects.filter(category=category)

    context = {
        'category': category,
        'events': events,
    }

    return render(request, 'events/events_by_category.html', context)


# RSVP

def send_rsvp_confirmation(user, event):
    subject = f"RSVP Confirmation for {event.name}"
    message = f"""
    Hello {user.username},

    You have successfully RSVPd for {event.name} on {event.date} at {event.time}.
    Location: {event.location}

    Thank you!
    """
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])


@login_required
def rsvp_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if event.rsvps.filter(id=request.user.id).exists():
        messages.error(request, "You have already RSVPd for this event.")
    else:
        event.rsvps.add(request.user)
        send_rsvp_confirmation(request.user, event)
        messages.success(
            request, f"You have successfully RSVPd for {event.name}!")

    return redirect('events:event_detail', id=event.id)


@login_required
def participant_dashboard(request):
    rsvp_events = request.user.rsvp_events.all()
    context = {
        'rsvp_events': rsvp_events,
    }
    return render(request, 'users/participant_dashboard.html', context)


@login_required
def dashboard(request):
    if is_admin(request.user):
        return redirect("admin_dashboard")
    elif is_organizer(request.user):
        return redirect("organizer_dashboard")
    elif is_participant(request.user):
        return redirect("participant_dashboard")

    return redirect("participant")
