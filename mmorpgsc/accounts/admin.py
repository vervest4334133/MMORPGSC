from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    list_filter = ('user',)
    search_fields = ('user',)


admin.site.register(User, UserAdmin)
