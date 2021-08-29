from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Event(models.Model):
    title = models.charField(max_length=100)
    content = models.textField()
    date_posted = models.DateTimeField(auto_now_add=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
