from django.urls import path

from . import views

app_name = 'events'

urlpatterns = [
    path('', views.index, name='index'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('create-event/', views.create_event, name='create_event'),
]