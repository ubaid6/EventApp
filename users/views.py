from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm, ChangeForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('events-home')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})


@login_required(login_url='login')
def viewprofile(request):
    args = {
        'user' : request.user
    }
    return render(request, 'users/viewprofile.html', args)


@login_required(login_url='login')
def editprofile(request):
    if request.method == "POST":
        form = ChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Details changed for {username}')
            return redirect('events-home')
    else:
        form = ChangeForm()
    return render(request, 'users/editprofile.html', {'form': form})
