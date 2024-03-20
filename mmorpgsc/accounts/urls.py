from django.urls import path
from .views import *
from .forms import *
from django.contrib.auth import views as authViews


urlpatterns = [
    path('personal_room/', PersonalRoom, name='personal_room'),
    path('signup/', register, name="signup"),
    path('logout/', authViews.LogoutView.as_view(), name='logout'),
]

# urlpatterns = [
#     path('personal_room/', PersonalRoom.as_view(), name='personal_room'),
#     path('signup/', SignUp.as_view(), name="register"),
#     path('activation_code_form/', views.endreg, name="endreg"),
#     path('',views.activation, name='activation'),
# ]

