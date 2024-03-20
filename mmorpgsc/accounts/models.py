from django.contrib.auth.models import User
from django.db import models


class UserAccount(models.Model):
    user = models.OneToOneField(User, related_name='user_account',
                                default=None, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, blank=True, null=True, default=None, unique=True)
    date = models.DateField(blank=True, null=True, auto_now_add=True)
