from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from .models import Event
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import forms
from .forms import CreateEvent
from .models import Event, UserEventInfo
from django.contrib import messages
from users.models import User
from django.views.generic.edit import UpdateView, DeleteView
from django.core.paginator import Paginator
# Create your views here.

@login_required(login_url='login')
def home(request):

    # print(request.user.emailAuthenticated)

    for object in UserEventInfo.objects.all():
        object.function()

    for event in Event.objects.all():
        event.shouldAttend = False

    n = 0
    for event in Event.objects.all():
        for evInfo in UserEventInfo.objects.all():
            if evInfo.event == event and evInfo.user == request.user and (evInfo.isAttending == True):
                event.shouldAttend = False
                break
            else:
                n += 1
        if n == len(UserEventInfo.objects.all()):
            event.shouldAttend = True
        else:
            event.shouldAttend = False
        event.save()
        # print(n, len(UserEventInfo.objects.all()))
        n = 0

    events_paginator = Paginator(Event.objects.all().order_by('-date_posted'), 10)
    events = events_paginator.get_page(1)


    context = {
        # 'events': Event.objects.all(),
        'events': events,
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
            messages.success(request, 'Event created!')
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


@login_required(login_url='login')
def unattend(request, id):
    event = Event.objects.get(pk=id)
    for eventInfo in UserEventInfo.objects.all():
        if eventInfo.event == event and eventInfo.user == request.user and eventInfo.isAttending == True:
            eventInfo.delete()
            event.subscribed -= 1
            event.save()

    messages.success(request, f'You have unsubscribed from {event.title}')
    return redirect('events-home')


@login_required(login_url='login')
def myEvents(request):
    context = {
        'events': Event.objects.all(),
        'userEventInfo': UserEventInfo.objects.all()
    }

    return render(request, 'events/my-events.html', context)












