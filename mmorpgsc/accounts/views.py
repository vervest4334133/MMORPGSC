from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.decorators import login_required

from mmorpgsc import settings

from .models import User


class Login(TemplateView):
    model = User
    success_url = '/accounts/login'
    template_name = 'accounts/signup.html'


class ConfirmUser(UpdateView):
    model = User
    context_object_name = 'reg_confirm'

    def post(self, request, *args, **kwargs):
        if 'code' in request.POST:
            user = User.objects.filter(code=request.POST['code'])
            if user.exists():
                user.update(is_active=True)
                new_user = User.objects.get(code=request.POST['code'])
                user.update(code=None)


                subject = 'Добро пожаловать на портал MMORPG Social Community!'
                text = f'{new_user.username}, вы успешно зарегистрировались на сайте!'
                html = (
                    f'<b>{new_user.username}</b>, вы успешно зарегистрировались на '
                    f'<a href="{settings.SITE_URL}">сайте</a>!'
                )
                msg = EmailMultiAlternatives(
                    subject=subject, body=text, from_email=None, to=[new_user.email]
                )
                msg.attach_alternative(html, "text/html")
                msg.send()

            else:
                return render(self.request, 'account/invalid_code.html')

        return redirect('/accounts/login')


# @login_required
# class PersonalRoom(UpdateView):
#     template_name = "account/personal_room.html"


@login_required
class LogOutView(TemplateView):
    template_name = "account/logout.html"
