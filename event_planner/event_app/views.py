from django.db.models.query_utils import Q
import bcrypt
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.urls import reverse
from django.core.mail import send_mail, send_mass_mail


def index(request):
    form = RegistrationForm()
    context = {
        "RegForm": form,
    }
    return render(request, "login_reg.html", context)

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
            # if data does not pass validations, render form along with errors
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
    # is there a way to turn the following two lines into a decorator?
    if 'logged_user_id' not in request.session:
        return redirect('/login-required')

    context = {
        'logged_user': User.objects.get(id=user_id),
    }
    return render(request, 'dashboard.html', context)

def event_info(request, event_id):
    if 'logged_user_id' not in request.session:
        return redirect('/login-required')

    comment_form = CommentForm()
    # specify form action in views so it can access event_id
    comment_form.helper.form_action = reverse('event_planner:add_comment', kwargs={'event_id': event_id})
    context = {
        'this_event': Event.objects.get(id=event_id),
        'this_user': User.objects.get(id=request.session['logged_user_id']),
        'CommentForm': comment_form,
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
            # creates event but doesn't commit save to allow for adding host from session
            new_event = e_form.save(commit=False)
            new_event.host = User.objects.get(id=request.session['logged_user_id'])
            new_event.save()
            return redirect(f'/event/{new_event.id}/info')

        return render(request, 'create_event.html', context={'EventForm': e_form})

def cancel_event(request, event_id):
    this_event = Event.objects.get(id=event_id)

    this_event.delete()
    return redirect(f"/user/{request.session['logged_user_id']}")

def edit_form(request, event_id):
    if 'logged_user_id' not in request.session:
        return redirect('/login-required')

    this_event = Event.objects.get(id=event_id)
    event_form = EditEventForm(instance=this_event)
    context = {
        'user': User.objects.get(id=request.session['logged_user_id']),
        'EditForm': event_form,
        'event': this_event,
    }
    return render(request, 'edit_event.html', context)

def edit_event(request, event_id):
    if 'logged_user_id' not in request.session:
        return redirect('/login-required')

    if request.method == 'POST':
        # event instance so the form only EDITS THE DESIRED EVENT, NOT MAKE NEW
        this_event = Event.objects.get(id=event_id)
        edit_form = EditEventForm(request.POST, instance=this_event)
        if edit_form.is_valid():
            updated_event = edit_form.save()
            return redirect(f'/event/{updated_event.id}/info')

        return render(request, 'edit_event.html', context={'EditForm': edit_form})

def add_attendee(request, event_id):
    attendee = User.objects.get(id=request.session['logged_user_id'])
    event = Event.objects.get(id=event_id)

    event.attendees.add(attendee)
    event.save()
    messages.success(request, 'you have successfully RSVP\'d!')
    return redirect(f'/event/{event.id}/info')

def remove_attendee(request, event_id):
    attendee = User.objects.get(id=request.session['logged_user_id'])
    event = Event.objects.get(id=event_id)

    event.attendees.remove(attendee)
    event.save()
    messages.success(request, 'you have successfully left the event!')
    return redirect(f'/event/{event.id}/info')

# create a contact form in forms.py, and then use the info pulled from there to create email
def email_attendee(request, event_id):
    this_event = Event.objects.get(id=event_id)
    attendees = this_event.attendees.all()
    attendee_emails = []
    for attendee in attendees:
        attendee_emails.append(attendee.email)

    message1 = ('Event Change', f'Please check the {this_event.title} page, there has been a change!', 'test@mail.com', attendee_emails)
    send_mass_mail((message1,), fail_silently=False)
    messages.success(request, 'you have successfully emailed the attendees!')
    return redirect(f'/event/{this_event.id}/info')

def add_comment(request, event_id):
    if 'logged_user_id' not in request.session:
        return redirect('/login-required')

    commenter = User.objects.get(id=request.session['logged_user_id'])
    event = Event.objects.get(id=event_id)

    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        new_comment.created_by = commenter
        new_comment.event_commented = event
        new_comment.save()
        return redirect(f'/event/{event.id}/info')
    
    # provide context so the user and event info renders upon comment error
    context = {
        'CommentForm': comment_form,
        'this_event': event,
        'this_user': commenter,
    }
    return render(request, 'event_info.html', context)