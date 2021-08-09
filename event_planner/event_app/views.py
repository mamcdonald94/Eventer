import event_app
from django.http.response import HttpResponse
from django.shortcuts import render
from .forms import *
from django.contrib.auth.decorators import login_required
from .models import *

def index(request):
    form = RegistrationForm()
    context = {
        "RegForm": form,
    }
    return render(request, "login_reg.html", context)

# need to figure out how to apply validations and encrypt passwords using a django form -- might need to exclude the password field and then manipulate it later like host field in Event model
@login_required(login_url='login/')
def event_info(request):
    return render(request, 'event_info.html')

@login_required(login_url='login/')
def event_form(request):
    form = EventForm()
    context = {
        "EventForm": form,
    }
    return render(request, "create_event.html", context)

@login_required(login_url='login/')
def create_event(request):
    pass
# creating event follows below -- how to render errors?
    # if request.method == "POST":
    #     event_form = EventForm(request.POST)
    #     new_event = event_form.save(commit=False)
    #     new_event.host = 