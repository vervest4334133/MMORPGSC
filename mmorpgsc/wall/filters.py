import django_filters

from django import forms

from .models import *


class PostFilter(django_filters.FilterSet):
    time_in = django_filters.DateTimeFilter(
        label='Post was created:',
        field_name='time_of_creation',
        lookup_expr='gt',
        widget=forms.DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    class Meta:
        model = Post
        fields = {
            'name': ['icontains'],
            'time_of_creation': [],
            'category': ['exact'],
        }


# class ReplyFilter(django_filters.FilterSet):
#     class Meta:
#         model = Post
#         fields = {
#             'name': ['icontains'],
#             'category': ['exact'],
#         }