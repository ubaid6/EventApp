from django.shortcuts import render
from .models import Event

# Create your views here.

def home(request):
    context = {
        'events': Event.objects.all()
    }
    return render(request, 'events/events.html', context)


