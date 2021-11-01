from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Film(models.Model):
    name = models.CharField(max_length=128)
    users = models.ManyToManyField(User, related_name='films')