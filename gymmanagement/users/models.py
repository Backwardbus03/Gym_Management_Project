from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    role = models.CharField(max_length=100, choices=(('trainer', 'Trainer'), ('trainee', 'Trainee'), ('admin', 'Admin')))
