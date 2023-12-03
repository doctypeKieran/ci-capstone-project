from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages

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

            messages.success(request, "Your event has been submitted and is pending approval.")

            return redirect('index')
    else:
        form = EventCreationForm()
    
    context = {
        'form': form,
    }

    return render(request, 'events/create_event.html', context)


@login_required
def delete_event(request, event_id):
    event = get_object_or_404(EventModel, pk=event_id)

    if request.user == event.creator or request.user.is_superuser:
        event.delete()
        messages.success(request, f"Event {event.title} successfully deleted.")

    else:
        messages.error(request, "You don't have permission to delete that event.")

    return redirect('index')


@login_required
def user_pending_events(request):
    pending_events = EventModel.objects.filter(creator=request.user, approved=False)

    context = {
        'pending_events': pending_events,
    }

    return render(request, 'events/user_pending_events.html', context)


@login_required
def delete_pending_event(request, event_id):
    event = get_object_or_404(EventModel, pk=event_id, creator=request.user, approved=False)

    event.delete()
    messages.success(request, f"Event {event.title} successfully deleted")

    return redirect('events:user_pending_events')


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

    if request.method == 'POST':
        action = request.POST.get('action', '')  # Get the action from the form

        if action == 'approve':
            event.approved = True
            event.save()
            messages.success(request, f'Event {event.title} has been approved.')

        elif action == 'reject':
            # Delete the event and display a success message
            event.delete()
            messages.success(request, 'Event has been rejected and deleted.')

        return redirect('events:event_approval_list')

    # If the request method is not POST, render the approval form
    context = {
        'event': event,
    }

    return render(request, 'events/event_approval.html', context)
