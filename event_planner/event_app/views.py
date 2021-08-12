import bcrypt
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
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
            new_user = reg_form.save(commit=False)
            hash_pw = bcrypt.hashpw(reg_form.cleaned_data['password'].encode(), bcrypt.gensalt()).decode()
            new_user.password = hash_pw
            new_user.save()
            # stores the logged in user's id for usage elsewhere in app
            request.session['logged_user_id'] = new_user.id
            return redirect(f'/user/{new_user.id}')
        else:
            return render(request, 'login_reg.html', context={'RegForm': reg_form})

def login(request):
    if request.method == 'POST':
        user = User.objects.filter(email=request.POST['email'])
        if user:

            logged_user = user[0]
            # checks to see if the password submitted matches the password in the database
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                # holds the id of the currently logged in user, redirects to their dashboard
                request.session['logged_user_id'] = logged_user.id
                return redirect(f'/user/{logged_user.id}')

        messages.error(request, "invalid email or password")
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def login_req(request):
    return render(request, 'login_required.html')

def dashboard(request, user_id):
    # is there a way to turn lines 60/61 into a decorator?
    if 'logged_user_id' not in request.session:
        return redirect('/login-required')

    context = {
        'logged_user': User.objects.get(id=user_id),
    }
    return render(request, 'dashboard.html', context)

def event_info(request, event_id):
    if 'logged_user_id' not in request.session:
        return redirect('/login-required')
    context = {
        'this_event': Event.objects.get(id=event_id),
        'this_user': User.objects.get(id=request.session['logged_user_id']),
    }
    return render(request, 'event_info.html', context)


def all_events(request):
    if 'logged_user_id' not in request.session:
        return redirect('/login-required')

    context = {
        'events': Event.objects.all(),
        'user': User.objects.get(id=request.session['logged_user_id'])
    }
    return render(request, 'all_events.html', context)


def event_form(request):
    if 'logged_user_id' not in request.session:
        return redirect('/login-required')

    form = EventForm()
    context = {
        "EventForm": form,
    }
    return render(request, "create_event.html", context)

def create_event(request):
    if 'logged_user_id' not in request.session:
        return redirect('/login-required')
    if request.method == 'POST':
        e_form = EventForm(request.POST)
        if e_form.is_valid():
            new_event = e_form.save(commit=False)
            new_event.host = User.objects.get(id=request.session['logged_user_id'])
            print(new_event.host.first_name)
            new_event.save()
            return redirect(f'/event/info/{new_event.id}')

        return render(request, 'create_event.html', context={'EventForm': e_form})

# def edit_event(request, event_id):
# USE event_form = EventForm(initial={'field1': intial value}) instantiate event object into form