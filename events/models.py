from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from cloudinary.models import CloudinaryField

# Create your models here.


class EventModel(models.Model):
    """
    Event model with fields for title, teaser, creator, image, description,
    date, time, approved status
    """
    title = models.CharField(max_length=250)
    teaser = models.CharField(max_length=300)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='events'
    )
    event_image_url = models.URLField(blank=True, null=True)
    description = models.TextField()
    ticket_price = models.FloatField(default=0)
    event_date = models.DateField()
    event_time = models.TimeField()
    city = models.CharField(max_length=50)
    venue = models.CharField(max_length=100, null=False, blank=False, default='')  # noqa
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['event_date']
        # The code below ensures that events can't take place at
        # the same date and time at the same city.
        unique_together = [['event_date', 'event_time', 'venue']]

    def __str__(self):
        return f"Event name: {self.title} held in {self.city} on {self.event_date}"  # noqa

    def get_image(self):
        return self.event_image_url


class BookEventModel(models.Model):
    """
    A model for users to book events, using the current user and
    current event as foreign keys to correlate with the event being
    booked by the currently logged in user. The user can select a number
    of tickets: a minimum of 1, a maximum of 10.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(EventModel, on_delete=models.CASCADE)
    num_of_tickets = models.PositiveIntegerField(default=1, choices=[(i, i) for i in range(1, 11)])  # noqa
    date_booked = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        ticket_plural = 'ticket' if self.num_of_tickets == 1 else 'tickets'
        return f"Event: {self.event.title} booked by '{self.user}' with {self.num_of_tickets} {ticket_plural}."  # noqa


class Review(models.Model):
    """
    A model for users to leave reviews, using the current event and
    user as foreign keys to correlate to the current event being
    reviewed by the currently logged-in user. Review score will be
    options with a minumum of 1, maximum of 5, and will be unapproved
    by default.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(EventModel, on_delete=models.CASCADE)
    review_title = models.CharField(max_length=150)
    review_text = models.TextField()
    review_score = models.PositiveIntegerField(default=1, choices=[(i, i) for i in range(1, 6)])  # noqa
    review_submitted = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Review: {self.review_title} submitted by {self.user} on {self.review_submitted}"  # noqa
