from random import random

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django_registration.forms import RegistrationForm
from django.contrib.auth.models import Group, User

from accounts.models import UserProfile
from mmorpgsc.settings import DEFAULT_FROM_EMAIL


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


def register(request):  # Регистрация
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Деактивируем пользователя
            user.save()

            # Добавляем пользователю группу "авторы"
            authors_group = Group.objects.get(name='USERS')
            user.groups.add(authors_group)

            # Генерируем и сохраняем код подтверждения
            confirmation_code = generate_confirmation_code()
            profile = UserProfile(user=user, confirmation_code=confirmation_code)
            profile.save()

            # Отправляем код подтверждения по электронной почте
            send_confirmation_email(user.email, confirmation_code)

            return redirect('confirm')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def generate_confirmation_code():  # Генерируем код подтверждения
    random.seed()
    return str(random.randint(100000, 999999))


def send_confirmation_email(email, confirmation_code):  # Отправляем код подтверждения
    subject = 'Подтверждение регистрации'
    message = (f'Ваш код подтверждения: {confirmation_code}')
    from_email = DEFAULT_FROM_EMAIL
    to_email = [email]
    send_mail(subject, message, from_email, to_email)




# def generate_code():
#     random.seed()
#     return str(random.randint(100000, 999999))
#
#
# class MyActivationCodeForm(forms.Form):
#     error_css_class = 'has-error'
#     error_messages = {'password_incorrect':
#                           ("Старый пароль не верный. Попробуйте еще раз."),
#                       'password_mismatch':
#                           ("Пароли не совпадают."),
#                       'cod-no':
#                           ("Код не совпадает."),}
#
#     def __init__(self, *args, **kwargs):
#         super(MyActivationCodeForm, self).__init__(*args, **kwargs)
#
#     code = forms.CharField(required=True, max_length=50,
#                            label='Код подтвержения', widget=forms.PasswordInput(attrs={'class': 'form-control'}),
#                            error_messages={'required': 'Введите код!','max_length': 'Максимальное количество символов 50'})
#
#     def save(self, commit=True):
#         profile = super(MyActivationCodeForm, self).save(commit=False)
#         profile.code = self.cleaned_data['code']
#
#         if commit:
#             profile.save()
#         return profile
#
#
# class RegistrationForm(UserCreationForm):
#     email = forms.EmailField(required=True, label='Email')
#     username = forms.CharField(required=True, max_length=15, label='Логин',  min_length=2)
#     password1 = forms.CharField(required=True, max_length=30, label='Пароль', min_length=8)
#     password2 = forms.CharField(required=True, max_length=30, label='Повторите пароль')
#
#     class Meta:
#         model = User
#         fields = (
#             'username',
#             'email',
#             'password1',
#             'password2'
#        )
#
#     def clean_username(self):
#         username = self.cleaned_data.get("username")
#         try:
#             User._default_manager.get(username=username)
#             # if the user exists, then let's raise an error message
#             raise forms.ValidationError(
#                 self.error_messages['username_exists'],  # my error message
#                 code='username_exists',  # set the error message key
#             )
#         except User.DoesNotExist:
#             return username  # if user does not exist so we can continue the registration process
#
#     def save(self, commit=True):
#         user = super(RegistrationForm, self).save(commit=False)
#         user.email = self.cleaned_data['email']
#         user.password1 = self.cleaned_data['password1']
#         user.password2 = self.cleaned_data['password2']
#         user.is_active = False
#
#         if commit:
#             user.save()
#         return user


