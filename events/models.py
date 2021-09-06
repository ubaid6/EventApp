from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    shouldAttend = models.BooleanField(default=False)
    subscribed = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('events-home')


class UserEventInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    isAttending = models.BooleanField(default=False)
    isCreator = models.BooleanField(default=False)

    def function(self):
        if self.isCreator == True:
            self.user = self.event.author
            self.save()

