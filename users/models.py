from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    emailAuthenticated = models.BooleanField(default=False)
    class Meta:
        db_table = 'user'

# Create your models here.
