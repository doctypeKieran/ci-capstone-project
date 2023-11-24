from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import EventModel

# Create your views here.

def index(request):
    events = EventModel.objects.filter(approved=True)

    context = {
        'events': events,
    }
    return render(request, 'events/index.html', context)

def event_detail(request, event_id):
    event = get_object_or_404(EventModel, pk=event_id)

    context = {
        'event': event,
    }

    return render(request, 'events/event_detail.html', context)