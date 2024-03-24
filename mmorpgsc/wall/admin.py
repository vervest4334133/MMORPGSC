from django.contrib import admin
from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'time_of_creation', 'update_time', 'content')
    list_filter = ('name', 'category', 'author', 'time_of_creation', 'update_time')
    search_fields = ('name', 'category__name')


class ReplyAdmin(admin.ModelAdmin):
    list_display = ('reply_text', 'user', 'reply_date')
    list_filter = ('reply_text', 'user', 'reply_date')
    search_fields = ('reply_text', 'user', 'reply_date')


admin.site.register(Post, PostAdmin)
admin.site.register(Reply, ReplyAdmin)
