from django.shortcuts import render
from events.models import Event, Category, Participant


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


def create_event(request):
    context = {

    }
    return render(request, 'events/create_event.html', context)


def create_category(request):
    context = {

    }
    return render(request, 'events/create_category.html', context)


def create_participant(request):
    context = {

    }
    return render(request, 'events/create_participant.html', context)
