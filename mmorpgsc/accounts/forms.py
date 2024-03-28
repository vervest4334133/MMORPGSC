import random

from string import hexdigits

from allauth.account.forms import SignupForm

from django.contrib.auth.models import Group
from django.core.mail import send_mail

from mmorpgsc import settings


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.is_active = False
        code = ''.join(random.sample(hexdigits, 6))
        user.code = code
        user.save()

        users_group = Group.objects.get(name="USERS")
        user.groups.add(users_group)

        send_mail(
            subject=f'Код для подтверждения регистрации',
            message=f'Код для подтверждения регистрации аккаунта: {code}.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return user
