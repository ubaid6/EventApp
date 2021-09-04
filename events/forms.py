from django.contrib.auth.forms import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from . models import Event
from . models import UserEventInfo


class CreateEvent(ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'content']


