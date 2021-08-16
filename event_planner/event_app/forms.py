from django import forms
from django.forms import fields, widgets
from django.urls.base import reverse
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
import crispy_forms.layout as cfl
# import bcrypt


class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')
        widgets = {
            'password': forms.PasswordInput,
        }

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get("password")

        confirm_password = cleaned_data.get("confirm_password")
        # check password match before hashing
        if password != confirm_password:
            self.add_error('confirm_password', "Password does not match")
        # hash password
        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'RegistrationForm'
        self.helper.form_class = 'bootstrap4'
        self.helper.form_method = 'POST'
        self.helper.form_action = '/create_user/'
        self.helper.attrs = {'novalidate': ''}
        self.helper.form_show_errors = True

        self.helper.add_input(Submit('submit', 'Register'))

class EventForm(forms.ModelForm):
    time = forms.TimeField(error_messages={'invalid': 'please enter a time in 12-hour format (ex: 7:00 AM, 3:30 PM, etc.)'})
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

# I'm sure there is a better way to do this, but I created a second form class specifically for editing
class EditEventForm(forms.ModelForm):
    time = forms.TimeField(error_messages={'invalid': 'please enter a time in 12-hour format (ex: 7:00 AM, 3:30 PM, etc.)'})
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'EditEventForm'
        self.helper.form_class = 'bootstrap4'
        self.helper.form_method = 'POST'
        # searches for the named url path ('edit_event') and supplies the event instance id to the url so the event can be edited
        self.helper.form_action = reverse('event_planner:edit_event', args=[self.instance.id])
        self.helper.attrs = {'novalidate': ''}

        self.helper.add_input(Submit('submit', 'Edit Event'))
    
    class Meta:
        model = Event
        exclude = ['host', 'attendees']
        widgets = {
            'date': forms.SelectDateWidget,
        }


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'CommentForm'
        self.helper.form_class = 'bootstrap4'
        self.helper.form_method = 'POST'
        self.helper.attrs = {'novalidate': ''}

        self.helper.add_input(Submit('submit', 'Add Comment'))

    class Meta:
        model = Comment
        exclude = ['created_by', 'event_commented']
        widgets = {
            'content': widgets.Textarea,
        }