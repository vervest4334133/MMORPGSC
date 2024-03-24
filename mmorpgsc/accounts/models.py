from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, blank=True, null=True, default=None, unique=True)
