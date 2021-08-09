from django.db import models
from django.forms.fields import EmailField

# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False, null=True)

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    time = models.TimeField()
    date = models.DateField()
    host = models.ForeignKey(User, related_name="events_hosted", on_delete=models.CASCADE) # exclude this from form, pull from logged_user in session in views
    attendees = models.ManyToManyField(User, related_name="events_attended")
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False, null=True)

class Comment(models.Model):
    content = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, related_name="comments_made", on_delete=models.CASCADE) # exclude this from form, pull from logged_user in session in views
    event_commented = models.ForeignKey(Event, related_name="comments", on_delete=models.CASCADE) # exclude this from form, pull event_id from URL or something
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False, null=True)