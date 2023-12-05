from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse

from .models import EventModel, BookEventModel, Review
from .forms import EventCreationForm, EventEditForm, BookingForm, ReviewForm

# Create your views here.


def index(request):
    events = EventModel.objects.filter(approved=True)

    context = {
        'events': events,
    }
    return render(request, 'events/index.html', context)


def all_events(request):
    events = EventModel.objects.filter(approved=True)

    paginator = Paginator(events, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }

    return render(request, 'events/all_events.html', context)


def event_detail(request, event_id):
    event = get_object_or_404(EventModel, pk=event_id)
    reviews = Review.objects.filter(event=event, approved=True)

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.event = event
            review.save()

            messages.success(request, 'Your review has been submitted and is pending approval.')

            return redirect('event_detail', event_id=event_id)
    else:
        review_form = ReviewForm()

    context = {
        'event': event,
        'reviews': reviews,
        'review_form': review_form
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


def edit_event(request, event_id):
    event = get_object_or_404(EventModel, pk=event_id, creator=request.user)

    if request.method == 'POST':
        form = EventEditForm(request.POST, instance=event)
        if form.is_valid():
            event.approved = False
            form.save()
            
            messages.success(request, "Your event has been edited and is pending approval.")

            return redirect('index')
    else:
        form = EventEditForm(instance=event)

    context = {
        'form': form,
        'event': event,
    }

    return render(request, 'events/edit_event.html', context)


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
def book_event(request, event_id):
    event = get_object_or_404(EventModel, pk=event_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.event = event
            booking.save()
            ticket_plural = 'ticket' if booking.num_of_tickets == 1 else 'tickets'
            messages.success(request, f'Successfully booked {event.title} with {booking.num_of_tickets} {ticket_plural}')
            return redirect(reverse('event_detail', args=[event.id]))
    else:
        form = BookingForm()
    
    context = {
        'form': form,
        'event': event,
    }

    return render(request, 'events/book_event.html', context)


@login_required
def user_booked_events(request):
    booked_events = BookEventModel.objects.filter(user=request.user)

    context = {
        'booked_events': booked_events
    }

    return render(request, 'events/booked_events.html', context)


def delete_booked_event(request, booking_id):
    booked_event = get_object_or_404(BookEventModel, pk=booking_id, user=request.user)

    if request.method == 'POST':
        booked_event.delete()
        messages.success(request, f'Booking for {booked_event.event.title} deleted successfully.')

    return redirect('events:user_booked_events')


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
        action = request.POST.get('action', '')

        if action == 'approve':
            event.approved = True
            event.save()
            messages.success(request, f'Event {event.title} has been approved.')

        elif action == 'reject':
            event.delete()
            messages.success(request, 'Event has been rejected and deleted.')

        return redirect('events:event_approval_list')

    # If the request method is not POST, render the approval form
    context = {
        'event': event,
    }

    return render(request, 'events/event_approval.html', context)


@login_required
def review_approval_list(request):
    if not request.user.is_superuser:
        return render(request, 'unauthorized.html')

    pending_reviews = Review.objects.filter(approved=False)

    context = {
        'pending_reviews': pending_reviews,
    }

    return render(request, 'events/review_approval_list.html', context)


@login_required
def review_approval(request, review_id):
    if not request.user.is_superuser:
        return render(request, 'unauthorized.html')

    review = get_object_or_404(Review, pk=review_id)

    if request.method == 'POST':
        action = request.POST.get('action', '')

        if action == 'approve':
            review.approved = True
            review.save()
            messages.success(request, f'Review by {review.user} has been approved.')
        elif action == 'reject':
            review.delete()
            messages.success(request, 'Review has been rejected and deleted.')
    
    return redirect('events:review_approval_list')



@login_required
def user_pending_reviews(request):
    pending_reviews = Review.objects.filter(user=request.user, approved=False)

    print(pending_reviews)

    context = {
        'pending_reviews': pending_reviews,
    }

    return render(request, 'events/user_pending_reviews.html', context)