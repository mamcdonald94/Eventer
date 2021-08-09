from django.urls import path
from .views import *


urlpatterns = [
    path('login/', index),
    path('event/info', event_info),
    path('event/event-form', event_form),
    path('event/create-event', create_event),
]