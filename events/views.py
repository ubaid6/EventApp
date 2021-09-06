from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from .models import Event
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import forms
from .forms import CreateEvent
from .models import Event, UserEventInfo
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView, DeleteView

# Create your views here.

@login_required(login_url='login')
def home(request):
    for object in UserEventInfo.objects.all():
        object.function()

    for event in Event.objects.all():
        event.shouldAttend = False

    n = 0
    for event in Event.objects.all():
        for evInfo in UserEventInfo.objects.all():
            if evInfo.event == event and evInfo.user == request.user and (evInfo.isAttending == True or evInfo.isCreator == True):
                event.shouldAttend = False
                break
            else:
                n += 1
        if n == len(UserEventInfo.objects.all()):
            event.shouldAttend = True
        else:
            event.shouldAttend = False
        event.save()
        print(n, len(UserEventInfo.objects.all()))
        n = 0



    context = {
        'events': Event.objects.all(),
        'eventinfo': UserEventInfo.objects.all(),
    }
    return render(request, 'events/events.html', context)



@login_required(login_url='login')
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


class editEvent(UpdateView):
    model = Event
    fields = ['title', 'content']
    template_name = 'events/editevent.html'

class deleteEvent(DeleteView):
    model = Event
    template_name = 'events/delete.html'
    context_object_name = 'event'
    success_url = reverse_lazy('events-home')


@login_required(login_url='login')
def attend(request, id):
    event = Event.objects.get(pk=id)
    event.subscribed += 1
    userEventInfo = UserEventInfo()
    userEventInfo.user = request.user
    userEventInfo.event = event
    userEventInfo.isAttending = True
    event.save()
    userEventInfo.save()
    messages.success(request, f'You have subscribed to {event.title}!')
    return redirect('events-home')










