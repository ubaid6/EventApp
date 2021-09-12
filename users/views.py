from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import RegistrationForm, ChangeForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django.contrib.auth.decorators import login_required
from .utils import emailToken
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, force_str
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.conf import settings

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            user = User.objects.get(username=username)
            sendActivationEmail(request, user)
            return redirect('login')
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


def sendActivationEmail(request, user):
    send_mail(
        'Activate your account',
        render_to_string('users/activate.html', {
            'user': user,
            'domain': get_current_site(request),
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': emailToken.make_token(user)
        }),
        settings.EMAIL_FROM_USER,
        [user.email],
        fail_silently=False,
    )


def activateEmail(request, uidb64, token):

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except Exception as e:
        print("Wrong")

    if user and emailToken.check_token(user, token):
        user.emailAuthenticated = True
        user.save()

        messages.success(request, 'Email Verified!')

        return redirect(reverse('events-home'))

    messages.success(request, 'Email Not Verified!')
    return render(request, 'events/events.html')


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user:
            if user.emailAuthenticated:
                auth_login(request, user)
                return redirect('events-home')

            else:
                sendActivationEmail(request, user)
                return redirect('login')

        else:
            return redirect('login')

    form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})





