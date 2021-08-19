from django.urls import path
from .views import *

app_name = 'event_planner'
urlpatterns = [
    path('', index),
    path('create_user/', create_user),
    path('login/', login),
    path('logout/', logout),
    path('user/<int:user_id>', dashboard),
    path('login-required/', login_req),
    path('event/<int:event_id>/info', event_info, name='event_info'),
    path('events/', all_events),
    path('event/event-form', event_form),
    path('event/create-event', create_event),
    path('event/<int:event_id>/cancel-event', cancel_event),
    path('event/<int:event_id>/edit-event', edit_event, name='edit_event'),
    path('event/<int:event_id>/edit', edit_form, name='edit_form'),
    path('event/<int:event_id>/add-attendee', add_attendee),
    path('event/<int:event_id>/remove-attendee', remove_attendee),
    path('event/<int:event_id>/email-attendee', email_attendee),
    path('event/<int:event_id>/email-host', email_host, name='email_host'),
    path('event/<int:event_id>/add-comment', add_comment, name='add_comment'),
]