from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from mmorpgsc import settings
from .forms import RegistrationForm, MyActivationCodeForm

from django.contrib.auth.decorators import login_required

from .models import UserAccount


class SignUp(CreateView):
    model = User
    form_class =
    success_url = '/accounts/login'
    template_name = 'registration/signup.html'

    def confirm_registration(request):  # подтверждение регистрации
        if request.method == 'POST':
            confirmation_code = request.POST.get('confirmation_code')
            user_profile = UserAccount.objects.get(confirmation_code=confirmation_code)
            user = user_profile.user
            user.is_active = True  # Активируем пользователя
            user_profile.save()
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('posts')
        return render(request, 'registration/reg_confirm.html')


@login_required
class LogOutView(TemplateView):
    template_name = "registration/logout.html"
