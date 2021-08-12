from django.urls import path
from .views import *


urlpatterns = [
    path('', index),
    path('create_user/', create_user),
    path('login/', login),
    path('logout/', logout),
    path('login-required/', login_req),
    path('event/info', event_info),
    path('event/event-form', event_form),
    path('event/create-event', create_event),
    path('user/<int:user_id>', dashboard),
]