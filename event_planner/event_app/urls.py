from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('event/id/info', event_info),
]