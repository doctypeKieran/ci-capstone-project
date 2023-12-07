from django.contrib import admin
from .models import EventModel, BookEventModel, Review

# Register your models here.


admin.site.register(EventModel)
admin.site.register(BookEventModel)
admin.site.register(Review)
