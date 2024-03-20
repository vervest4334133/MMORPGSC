from django.contrib import admin
from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'time_of_creation', 'update_time', 'content')
    list_filter = ('name', 'category', 'author', 'time_of_creation', 'update_time')
    search_fields = ('name', 'category__name')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']


class ForumUserAdmin(admin.ModelAdmin):
    list_display = ('f_user', 'email')
    list_filter = ('f_user', 'email')
    search_fields = ('f_user', 'email')


class ReplyAdmin(admin.ModelAdmin):
    list_display = ('reply_text', 'user', 'reply_date')
    list_filter = ('reply_text', 'user', 'reply_date')
    search_fields = ('reply_text', 'user', 'reply_date')


class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('post', 'category')
    list_filter = ('post', 'category')
    search_fields = ('post', 'category')


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ForumUser, ForumUserAdmin)
admin.site.register(Reply, ReplyAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)