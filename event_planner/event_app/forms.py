from django import forms
from django.forms import fields, widgets
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Password does not match")
        return cleaned_data
    # add helper to this form

class EventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'EventForm'
        self.helper.form_class = 'bootstrap4'
        self.helper.form_method = 'POST'
        self.helper.form_action = '/event/create-event'
        self.helper.attrs = {'novalidate': ''}

        self.helper.add_input(Submit('submit', 'Create Event'))

    class Meta:
        model = Event
        exclude = ['host', 'attendees']
        widgets = {
            'date': forms.SelectDateWidget,
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['created_by', 'event_commented']
        widgets = {
            'content': widgets.Textarea,
        }