from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse

from .models import EventModel, BookEventModel, Review
from .forms import EventCreationForm, EventEditForm, BookingForm, ReviewForm, EditReviewForm

# Create your views here.


def index(request):
    """
    The home page view.  This will render the index.html
    template which will only display events from the events 
    model which are approved.
    """
    events = EventModel.objects.filter(approved=True)

    context = {
        'events': events,
    }
    return render(request, 'events/index.html', context)


def all_events(request):
    """
    This view will render all events which are approved on
    a separate page, 'all-events', which will use the
    'all_events.html' template.  The use of the Django
    Paginator will ensure that only six get displayed at a
    time before a new page is created.
    """
    events = EventModel.objects.filter(approved=True)

    paginator = Paginator(events, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }

    return render(request, 'events/all_events.html', context)


def event_detail(request, event_id):
    """
    The purpose of this view is to display the full details of
    a particular event. Reviews for the selected event will
    also be shown at the bottom of the current event details.
    Providing the currently logged in user isn't the user who
    created the event, they can also submit a new review which
    will be put up for approval by an admin.
    """
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
    """
    Logged in users will be able to create an event with the use
    of the `EventCreationForm` which uses fields from the
    `EventModel` form. Once an event has been created, it will
    be put up for review by an admin and redirect the user back
    to the home page.
    """
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
    """
    Using the `EventEditForm`, users can edit their previously
    created events. The fields will be prepopulated with the
    exact same data as their previous event by creating an
    instance of the current event model and rendering that
    as a new form to be edited. Once the changes are submitted,
    the edited event will go back up for approval.
    """
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
    """
    A logged in user has the ability to delete their own
    event. A superuser has the ability to delete any event,
    enabling them to keep the site clean of redundant events.

    Should a user attempt to perform this functionality and they
    aren't a superuser/the user who created the event, they will
    receive an error message.
    """
    event = get_object_or_404(EventModel, pk=event_id)

    if request.user == event.creator or request.user.is_superuser:
        event.delete()
        messages.success(request, f"Event {event.title} successfully deleted.")

    else:
        messages.error(request, "You don't have permission to delete that event.")

    return redirect('index')


@login_required
def book_event(request, event_id):
    """
    Once a user clicks to book an event, they will be directed
    to a "book_event.html" template where they can select
    how many tickets they'd like to book for that event by
    using the `BookingForm` form.
    """
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
    """
    This view will display all booked events by the current
    user on a 'booked_events.html' template. With the use of a
    filter, only the current user's booked events will be displayed
    here.
    """
    booked_events = BookEventModel.objects.filter(user=request.user)

    context = {
        'booked_events': booked_events
    }

    return render(request, 'events/booked_events.html', context)


def delete_booked_event(request, booking_id):
    """
    Users can also delete their booked events should they feel
    the desire to no longer attend. `booked_event` will ensure that
    the the logged in user is the user making the request, and that
    the booking being deleted is the booking which was created.
    """
    booked_event = get_object_or_404(BookEventModel, pk=booking_id, user=request.user)

    if request.method == 'POST':
        booked_event.delete()
        messages.success(request, f'Booking for {booked_event.event.title} deleted successfully.')

    return redirect('events:user_booked_events')


@login_required
def user_pending_events(request):
    """
    Once a user creates an event, it will go up for approval. Users
    can see their pending approvals in the rendered template, and
    they are also welcome to delete their pending approvals if they
    do not wish for them to be approved.
    """
    pending_events = EventModel.objects.filter(creator=request.user, approved=False)

    context = {
        'pending_events': pending_events,
    }

    return render(request, 'events/user_pending_events.html', context)


@login_required
def delete_pending_event(request, event_id):
    """
    This view handles the logic for deleting user pending reviews by
    filtering unapproved events and ensuring that the user who made
    the request is also the event creator.
    """
    event = get_object_or_404(EventModel, pk=event_id, creator=request.user, approved=False)

    event.delete()
    messages.success(request, f"Event {event.title} successfully deleted")

    return redirect('events:user_pending_events')


@login_required
def event_approval_list(request):
    """
    For superusers only.
    Superusers can see which events need to be approved by displaying
    unapproved events. If a user attempts to navigate to this page
    and is not a superuser, they will be directed to a template,
    `unauthorized.html`.
    """
    if not request.user.is_superuser:
        return render(request, 'unauthorized.html')
    
    pending_events = EventModel.objects.filter(approved=False)

    context = {
        'pending_events': pending_events,
    }

    return render(request, 'events/event_approval_list.html', context)


@login_required
def event_approval(request, event_id):
    """
    For superusers only.
    From the event approval list, a superuser can approve
    or reject an event depending on the action of the button 
    which is clicked. The `approve` action button will approve 
    of an event. Similarly, the `reject` action button will
    reject the event and delete it from the database permanently.
    """
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
    """
    For superusers only.
    A superuser can see a list of pending reviews which are
    unapproved. If a user who is not a superuser attempts to
    navigate to this link, they will be directed to a template,
    `unauthorized.html`.
    """
    if not request.user.is_superuser:
        return render(request, 'unauthorized.html')

    pending_reviews = Review.objects.filter(approved=False)

    context = {
        'pending_reviews': pending_reviews,
    }

    return render(request, 'events/review_approval_list.html', context)


@login_required
def review_approval(request, review_id):
    """
    For superusers only.
    This view handles the logic for approving or rejecting
    event reviews in the exact same manner of approving or
    rejecting created events.
    """
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
    """
    Just as users can see their pending events, users can
    also see reviews which are pending approval.
    """
    pending_reviews = Review.objects.filter(user=request.user, approved=False)

    context = {
        'pending_reviews': pending_reviews,
    }

    return render(request, 'events/user_pending_reviews.html', context)


@login_required
def edit_review(request, review_id):
    """
    Using the same logic as `edit_event`, a user can edit
    their review. Once the review is edited, it goes back
    up for approval. This logic flow ensures that users can't
    submit a clean review and then edit it with offensive/vulgar
    language.
    """
    review = get_object_or_404(Review, pk=review_id, user=request.user)

    if request.method == 'POST':
        form = EditReviewForm(request.POST, instance=review)
        if form.is_valid():
            review.approved = False
            form.save()
            
            messages.success(request, "Your review has been edited and is pending approval.")

            return redirect('index')
    else:
        form = EditReviewForm(instance=review)

    context = {
        'form': form,
        'review': review,
    }

    return render(request, 'events/edit_event.html', context)
