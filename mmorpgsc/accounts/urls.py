from django.urls import path
from .views import *
from django.contrib.auth import views as authViews


urlpatterns = [
    path('personalArea/', views.personalArea, name='personalArea'),
    path('register/', views.register, name="register"),
    path('activation_code_form/', views.endreg, name="endreg"),
    path('',views.activation, name='activation'),
]

# urlpatterns = [
#     path('signup/', SignUp.as_view(), name='signup'),
#     path('logout/', authViews.LogoutView.as_view(), name='logout'),
# ]

# from . import views
# from django.urls import path
#
#
# from accounts.forms import register
# from .views import confirm_registration
#
# urlpatterns = [
#     path('register/', register, name='register'),
# ]