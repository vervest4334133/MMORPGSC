from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.contrib.auth.models import Group
from django.core.mail import EmailMultiAlternatives


def generate_code():
    random.seed()
    return str(random.randint(100000, 999999))


def register(request):
    if not request.user.is_authenticated:
        if request.POST:
            form = RegistrationForm(request.POST or None)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                email = form.cleaned_data.get('email')
                my_password1 = form.cleaned_data.get('password1')
                u_f = User.objects.get(username=username, email=email, is_active=False)
                code = generate_code()
                if UserAccount.objects.filter(code=code):
                    # for p in Profile.objects.filter(code=code):
                    #     p.delete()
                    code = generate_code()

                message = code
                user = authenticate(username=username, password=my_password1)
                now = datetime.datetime.now()

                UserAccount.objects.create(user=u_f, code=code, date=now)

                send_mail('код подтверждения', message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False)
                if user and user.is_active:
                    login(request, user)
                    return redirect('/personalArea/')
                else: #тут добавить редирект на страницу с формой для ввода кода.
                    form.add_error(None, 'Аккаунт не активирован')
                    return redirect('/reg_confirm/')
                    # return render(request, 'registration/register.html', {'form': form})

            else:
                return render(request, 'registration/signup.html', {'form': form})
        else:
            return render(request, 'registration/signup.html', {'form':
            RegistrationForm()})
    else:
        return redirect('/personalArea/')


def endreg(request):
    if request.user.is_authenticated:
        return redirect('/personalArea/')
    else:
        if request.method == 'POST':
            form = MyActivationCodeForm(request.POST)
            if form.is_valid():
                code_use = form.cleaned_data.get("code")
                if UserAccount.objects.filter(code=code_use):
                    profile = UserAccount.objects.get(code=code_use)
                else:
                    form.add_error(None, "Код подтверждения не совпадает.")
                    return render(request, 'registration/reg_confirm.html', {'form': form})
                if profile.user.is_active == False:
                    profile.user.is_active = True
                    profile.user.save()
                    # user = authenticate(username=profile.user.username, password=profile.user.password)
                    login(request, profile.user)
                    profile.delete()
                    return redirect('/personalArea/')
                else:
                    form.add_error(None, 'Unknown or disabled account')
                    return render(request, 'registration/reg_confirm.html', {'form': form})
            else:
                return render(request, 'registration/reg_confirm.html', {'form': form})
        else:
            form = MyActivationCodeForm()
            return render(request, 'registration/reg_confirm.html', {'form': form})

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    username = forms.CharField(required=True, max_length=15, label='Логин',  min_length=2)
    password1 = forms.CharField(required=True, max_length=30, label='Пароль', min_length=8)
    password2 = forms.CharField(required=True, max_length=30, label='Повторите пароль')

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2'
       )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        try:
            User._default_manager.get(username=username)
            # if the user exists, then let's raise an error message
            raise forms.ValidationError(
                self.error_messages['Пользователь с таким именем уже зарегистрирован!!!'],  # my error message
                code='username_exists',  # set the error message key
            )
        except User.DoesNotExist:
            return username  # if user does not exist so we can continue the registration process

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.password1 = self.cleaned_data['password1']
        user.password2 = self.cleaned_data['password2']
        user.is_active = False

        if commit:
            user.save()
        return user


class MyActivationCodeForm(forms.Form):
    error_css_class = 'has-error'
    error_messages = {'password_incorrect':
                          ("Старый пароль не верный. Попробуйте еще раз."),
                      'password_mismatch':
                          ("Пароли не совпадают."),
                      'cod-no':
                          ("Код не совпадает."),}

    def __init__(self, *args, **kwargs):
        super(MyActivationCodeForm, self).__init__(*args, **kwargs)

    code = forms.CharField(required=True, max_length=50, label='Код подтвержения',
                           widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                           error_messages={'required': 'Введите код!','max_length': 'Максимальное количество символов 50'})

    def save(self, commit=True):
        profile = super(MyActivationCodeForm, self).save(commit=False)
        profile.code = self.cleaned_data['code']

        if commit:
            profile.save()
        return profile






# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(label="Email")
#     first_name = forms.CharField(label="Имя")
#     last_name = forms.CharField(label="Фамилия")
#
#     class Meta:
#         model = User
#         fields = (
#             "username",
#             "first_name",
#             "last_name",
#             "email",
#             "password1",
#             "password2",
#         )
#
#         def save(self, request):
#             user = super().save(request)
#
#             USERS = Group.objects.get(name="USERS")
#             user.groups.add(USERS)
#
#             subject = 'Добро пожаловать на новостной портал MMORPG Social Community Project!'
#             text = f'{user.username}, вы успешно зарегистрировались на сайте!'
#             html = (
#                 f'<b>{user.username}</b>, вы успешно зарегистрировались на '
#                 f'<a href="http://127.0.0.1:8000/">сайте</a>!'
#             )
#             msg = EmailMultiAlternatives(
#                 subject=subject, body=text, from_email=None, to=[user.email]
#             )
#             msg.attach_alternative(html, "text/html")
#             msg.send()
#
#             return user
#
#
#
#
#
#
# from django.contrib.auth.models import Group
# from django.shortcuts import render, redirect
# from django.core.mail import send_mail
# from django_registration.forms import RegistrationForm
#
# import random
# import string
#
# from MMORPG.settings import DEFAULT_FROM_EMAIL
# from .models import UserProfile
#
#
# def register(request):  # Регистрация
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False  # Деактивируем пользователя
#             user.save()
#
#             # Добавляем пользователю группу "авторы"
#             authors_group = Group.objects.get(name='authors')
#             user.groups.add(authors_group)
#
#             # Генерируем и сохраняем код подтверждения
#             confirmation_code = generate_confirmation_code()
#             profile = UserProfile(user=user, confirmation_code=confirmation_code)
#             profile.save()
#
#             # Отправляем код подтверждения по электронной почте
#             send_confirmation_email(user.email, confirmation_code)
#
#             return redirect('confirm')
#     else:
#         form = RegistrationForm()
#     return render(request, 'registration/register.html', {'form': form})
#
#
# def generate_confirmation_code():  # Генерируем код подтверждения
#     characters = string.ascii_letters + string.digits
#     code = ''.join(random.choice(characters) for _ in range(10))
#     return code
#
#
# def send_confirmation_email(email, confirmation_code):  # Отправляем код подтверждения
#     subject = 'Подтверждение регистрации'
#     message = (f'Ваш код подтверждения: {confirmation_code}')
#     from_email = DEFAULT_FROM_EMAIL
#     to_email = [email]
#     send_mail(subject, message, from_email, to_email)