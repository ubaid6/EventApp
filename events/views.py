from django.shortcuts import render, redirect
from .models import Event
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import forms
from .forms import CreateEvent
from .models import Event, UserEventInfo
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.

@login_required(login_url='login')
def home(request):
    context = {
        'events': Event.objects.all()
    }
    return render(request, 'events/events.html', context)
    # if not request.user.is_authenticated:
    #     return redirect('login')
    # else:
    #     return render(request, 'events/events.html', context)

def create(request):
    if request.method == "POST":
        form = CreateEvent(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            userEventInfo = UserEventInfo()
            userEventInfo.user = request.user
            userEventInfo.event = instance
            userEventInfo.isCreator = True
            userEventInfo.save()
            messages.success(request, 'It worked!')
            return redirect('events-home')
    else:
        form = CreateEvent()
    return render(request, 'events/create.html', {'form' : form})

