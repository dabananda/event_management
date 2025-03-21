from django.shortcuts import render, redirect
from events.models import Event, Category, Participant
from events.forms import CategoryForm, EventForm, ParticipantForm


def index(request):
    events = Event.objects.all()
    categories = Category.objects.all()
    participants = Participant.objects.all()

    context = {
        'events': events,
        'categories': categories,
        'participants': participants,
    }

    return render(request, 'events/index.html', context)


def organizer_dashboard(request):
    context = {

    }
    return render(request, 'events/organizer_dashboard.html', context)


# Event views

def create_event(request):
    form = EventForm(request.POST or None)
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


def update_event(request, id):
    event = Event.objects.get(id=id)
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('events:all_events')
    context = {
        'event': event,
        'form': form,
    }
    return render(request, 'events/events_template/create_event.html', context)


def delete_event(request, id):
    event = Event.objects.get(id=id)
    if request.method == 'POST':
        event.delete()
        return redirect('events:all_events')
    context = {
        'event': event,
    }
    return render(request, 'events/events_template/delete_event.html', context)


# Category views

def create_category(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('events:all_categories')
    context = {
        'form': form,
    }
    return render(request, 'events/create_category.html', context)


def all_categories(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'events/categories.html', context)


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


def delete_category(request, id):
    category = Category.objects.get(id=id)
    if request.method == 'POST':
        category.delete()
        return redirect('events:all_categories')
    context = {
        'category': category,
    }
    return render(request, 'events/delete_category.html', context)


def create_participant(request):
    context = {

    }
    return render(request, 'events/create_participant.html', context)
