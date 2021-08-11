import event_app
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages

def index(request):
    form = RegistrationForm()
    context = {
        "RegForm": form,
    }
    return render(request, "login_reg.html", context)

# need to figure out how to apply validations and encrypt passwords using a django form -- might need to exclude the password field and then manipulate it later like host field in Event model

def create_user(request):
    if request.method == 'POST':
        reg_form = RegistrationForm(request.POST)
        if reg_form.is_valid():
            new_user = reg_form.save()
            # stores the logged in user's id for usage elsewhere in app
            request.session['logged_user_id'] = new_user.id
            return redirect(f'/user/{new_user.id}')
        else:
            return render(request, 'login_reg.html', context={'RegForm': reg_form})

def login(request):
    pass

def logout(request):
    request.session.flush()
    return redirect('/')

def dashboard(request, user_id):
    if 'logged_user_id' not in request.session:
        messages.error(request, "You must be logged in or registered to access this page!")
        return redirect('/')
    context = {
        'logged_user': User.objects.get(id=user_id),
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url='')
def event_info(request):
    return render(request, 'event_info.html')

@login_required(login_url='')
def event_form(request):
    form = EventForm()
    context = {
        "EventForm": form,
    }
    return render(request, "create_event.html", context)

@login_required(login_url='')
def create_event(request):
    pass
# creating event follows below -- how to render errors?
    # if request.method == "POST":
    #     event_form = EventForm(request.POST)
    #     new_event = event_form.save(commit=False)
    #     new_event.host = 



# def edit_event(request, event_id):
# USE event_form = EventForm(initial={'field1': intial value})