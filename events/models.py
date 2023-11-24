from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

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
    # Event image here when cloudinary is set up
    description = models.TextField()
    ticket_price = models.FloatField(default=0)
    event_date = models.DateField()
    event_time = models.TimeField()
    city = models.CharField(max_length=50)
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']
        unique_together = [['event_date', 'event_time', 'city']]

    def __str__(self):
        return f"Event name: {self.title} held in {self.city} on {self.event_date}"