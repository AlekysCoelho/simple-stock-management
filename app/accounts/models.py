from django.contrib.auth.models import AbstractUser
from django.db import models


class Users(AbstractUser):
    bio = models.TextField(blank=True)