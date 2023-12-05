from django.urls import path

from . import views

app_name = 'events'

urlpatterns = [
    path('', views.index, name='index'),
    path('all-events/', views.all_events, name='all_events'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('create-event/', views.create_event, name='create_event'),
    path('approval/list/', views.event_approval_list, name='event_approval_list'),
    path('approval/approve/<int:event_id>/', views.event_approval, name='event_approval'),
    path('user-pending-events/', views.user_pending_events, name='user_pending_events'),
    path('delete-event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('delete-pending-event/<int:event_id>/', views.delete_pending_event, name='delete_pending_event'),
    path('edit-event/<int:event_id>/', views.edit_event, name='edit_event'),
    path('book-event/<int:event_id>/', views.book_event, name='book_event'),
    path('booked-events/', views.user_booked_events, name='user_booked_events'),
    path('delete-booking/<int:booking_id>/', views.delete_booked_event, name='delete_booking'),
    path('user-pending-reviews', views.user_pending_reviews, name='user_pending_reviews'),
]