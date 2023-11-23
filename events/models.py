from django.db import models
from django.contrib.auth.models import User

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
    event_date = models.DateField(unique=True)
    event_time = models.TimeField(unique=True)
    city = models.CharField(max_length=50)
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']