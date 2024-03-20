from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.urls import reverse_lazy

from ckeditor.fields import RichTextField


class ForumUser(models.Model):
    f_user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True, blank=True)


class Post(models.Model):
    author = models.ForeignKey(ForumUser, on_delete=models.CASCADE, related_name='authors')

    TYPE = [
        ('Tanks', 'Танки'),
        ('Healers', 'Хилы'),
        ('DD', 'ДД'),
        ('Traders', 'Торговцы'),
        ('GM', 'Гилдмастеры'),
        ('QG', 'Квестгиверы'),
        ('Smiths', 'Кузнецы'),
        ('Leatherworkers', 'Кожевники'),
        ('Potions', 'Зельевары'),
        ('Spell', 'Мастера заклинаний')]

    category = models.CharField(max_length=16, choices=TYPE, verbose_name='Category')
    name = models.CharField(max_length=128, help_text='post_name')
    content = RichTextField(config_name='awesome_ckeditor')
    time_of_creation = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def preview(self):
        return f'{self.content[0:123]}...'

    def __str__(self):
        return self.name.title()

    def get_absolute_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')


class Reply(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply_text = models.TextField()
    reply_date = models.DateTimeField(auto_now_add=True)

    CONFIRMATION = [
        ('null', 'На рассмотрении'),
        ('confirmed', 'Принят'),
        ('not_confirmed', 'Отклонен')]

    confirm = models.CharField(max_length=16, choices=CONFIRMATION, default='null')

    def __str__(self):
        return self.reply_text

    def get_absolute_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.post_id})
