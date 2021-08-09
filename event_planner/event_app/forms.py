from django import forms
from django.forms import fields
from .models import User

class RegistrationForm(forms.ModelForm):
    class Meta:
        pass