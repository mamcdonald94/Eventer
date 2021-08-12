from django.core.exceptions import ValidationError
from django.db import models
from django import forms
from django.forms.fields import EmailField
import re

# Create your models here.

def name_validator(value):
    if len(value) < 2:
        raise ValidationError(
            "first/last name must be longer than 1 character"
        )

def title_validator(value):
    if len(value) < 5:
        raise ValidationError(
            "event title must be at least 5 characters"
        )

def password_validator(value):
    PW_REGEX = re.compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$')
    if not PW_REGEX.match(value):
        raise ValidationError(
            "password must be at least 8 characters, contain one uppercase letter, one lowercase letter, and one number"
        )
    # elif postData['password'] != postData['confirm_password']:
    #     raise ValidationError(
    #         "passwords did not match"
    #     )

def address_validator(value):
    ADD_REGEX = re.compile(r'^\d+\w+\s\w+\s\w+\s\w+\s\w+\s\d{5}$')
    if not ADD_REGEX.match(value):
        raise ValidationError(
            "please input a valid street address, state abbreviation and zip code (ex: 123 Main St Anywhere GA 12345)"
        )

def comment_validator(value): # add support for curse word filtering later(?)
    if len(value) < 15:
        raise ValidationError(
            "comment must be at least 15 characters"
        )

class User(models.Model):
    first_name = models.CharField(max_length=255, validators=[name_validator])
    last_name = models.CharField(max_length=255, validators=[name_validator])
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=255, validators=[password_validator])
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False, null=True)
    # events_hosted = list of events hosted by the User
    # events_attended = list of events attended by the User
    # comments_made = list of comments made by the User

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Event(models.Model):
    title = models.CharField(max_length=255, validators=[title_validator])
    description = models.CharField(max_length=255)
    location = models.CharField(max_length=255, validators=[address_validator])
    time = models.TimeField()
    date = models.DateField()
    host = models.ForeignKey(User, related_name="events_hosted", on_delete=models.CASCADE) # exclude this from form, pull from logged_user in session in views
    attendees = models.ManyToManyField(User, related_name="events_attended")
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False, null=True)
    # comments = list of comments on each Event

    def __str__(self):
        return f"{self.title}"

class Comment(models.Model):
    content = models.CharField(max_length=255, validators=[comment_validator])
    created_by = models.ForeignKey(User, related_name="comments_made", on_delete=models.CASCADE) # exclude this from form, pull from logged_user in session in views
    event_commented = models.ForeignKey(Event, related_name="comments", on_delete=models.CASCADE) # exclude this from form, pull event_id from URL or something
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False, null=True)

    def __str__(self):
        return f"Comment created by: {self.created_by.first_name}"