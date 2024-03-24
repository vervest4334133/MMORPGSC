from django.urls import path
from django.contrib.auth import views as authViews

from .views import *

urlpatterns = [
    #path('login/', Login.as_view(), name='login'),
    # path('personal_room/', PersonalRoom.as_view(), name='personal_room'),
    path('logout/', authViews.LogoutView.as_view(), name='logout'),
    path('confirm/', ConfirmUser.as_view(), name='reg_confirm')
]
