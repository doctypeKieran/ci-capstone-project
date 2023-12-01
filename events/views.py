from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import EventModel
from .forms import EventCreationForm

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


@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventCreationForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.save()
            return redirect('index')
    else:
        form = EventCreationForm()
    
    context = {
        'form': form,
    }

    return render(request, 'events/create_event.html', context)


@login_required
def event_approval_list(request):
    if not request.user.is_superuser:
        return render(request, 'unauthorized.html')
    
    pending_events = EventModel.objects.filter(approved=False)

    context = {
        'pending_events': pending_events,
    }

    return render(request, 'events/event_approval_list.html', context)


@login_required
def event_approval(request, event_id):
    if not request.user.is_superuser:
        return render(request, 'unauthorized.html')
    
    event = get_object_or_404(EventModel, pk=event_id)

    if not event.approved:
        event.approved = True
        event.save()
    
    return redirect('events:event_approval_list')