from django.shortcuts import render, redirect
from .models import Event
from django.contrib.auth.decorators import login_required

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

