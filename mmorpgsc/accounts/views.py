from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm
from .models import UserProfile


class SignUp(CreateView):
    model = User
    form_class = SignUpForm
    success_url = '/accounts/reg_confirm'
    template_name = 'registration/signup.html'


def confirm_registration(request):  # подтверждение регистрации
    if request.method == 'POST':
        confirmation_code = request.POST.get('confirmation_code')
        user_profile = UserProfile.objects.get(confirmation_code=confirmation_code)
        user = user_profile.user
        user.is_active = True  # Активируем пользователя
        user_profile.save()
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('posts')
    return render(request, 'registration/reg_confirm.html')


@login_required
class PersonalRoom(TemplateView):
    template_name = "account/personal_room.html"


@login_required
class LogOutView(TemplateView):
    template_name = "registration/logout.html"


# def generate_code():
#     random.seed()
#     return str(random.randint(10000,99999))
#
#
# def register(request):
#     if not request.user.is_authenticated:
#         if request.POST:
#             form = RegistrationForm(request.POST or None)
#             if form.is_valid():
#                 form.save()
#                 username = form.cleaned_data.get('username')
#                 email = form.cleaned_data.get('email')
#                 my_password1 = form.cleaned_data.get('password1')
#                 u_f = User.objects.get(username=username, email=email, is_active=False)
#                 code = generate_code()
#                 if UserProfile.objects.filter(code=code):
#                     code = generate_code()
#
#                 message = code
#                 user = authenticate(username=username, password=my_password1)
#                 now = datetime.datetime.now()
#
#                 UserProfile.objects.create(user=u_f, code=code, date=now)
#
#                 send_mail('код подтверждения', message,
#                 settings.EMAIL_HOST_USER,
#                 [email],
#                 fail_silently=False)
#                 if user and user.is_active:
#                     login(request, user)
#                     return redirect('/personal_room/')
#                 else:
#                     form.add_error(None, 'Аккаунт не активирован')
#                     return redirect('/reg_confirm/')
#
#             else:
#                 return render(request, 'registration/signup.html', {'form': form})
#         else:
#             return render(request, 'registration/signup.html', {'form':
#             RegistrationForm()})
#     else:
#         return redirect('/personal_room/')
#
#
# def endreg(request):
#     if request.user.is_authenticated:
#         return redirect('/personal_room/')
#     else:
#         if request.method == 'POST':
#             form = MyActivationCodeForm(request.POST)
#             if form.is_valid():
#                 code_use = form.cleaned_data.get("code")
#                 if UserProfile.objects.filter(code=code_use):
#                     profile = UserProfile.objects.get(code=code_use)
#                 else:
#                     form.add_error(None, "Код подтверждения не совпадает.")
#                     return render(request, 'registration/reg_confirm.html', {'form': form})
#                 if profile.user.is_active == False:
#                     profile.user.is_active = True
#                     profile.user.save()
#                     login(request, profile.user)
#                     profile.delete()
#                     return redirect('/personal_room/')
#                 else:
#                     form.add_error(None, '1Unknown or disabled account')
#                     return render(request, 'registration/reg_confirm.html', {'form': form})
#             else:
#                 return render(request, 'registration/reg_confirm.html', {'form': form})
#         else:
#             form = MyActivationCodeForm()
#             return render(request, 'registration/reg_confirm.html', {'form': form})
