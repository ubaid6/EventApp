from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class ChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
