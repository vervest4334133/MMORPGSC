from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives, send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseBadRequest, request
from django.template.loader import render_to_string

from wall.filters import PostFilter
from wall.forms import ReplyForm, PostForm
from wall.models import *


def start_page(request):
    t = render_to_string('start.html')
    return HttpResponse(t)


class PostList(ListView):
    model = Post
    ordering = '-time_of_creation'
    template_name = 'wall/wall_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        all_posts = Post.objects.all().values_list('name')
        context['count_posts'] = all_posts
        context['post_count'] = f"Всего постов - {len(all_posts)}"
        context['filterset'] = self.filterset
        return context


class ReplyCreate(CreateView, LoginRequiredMixin):
    raise_exception = True
    form_class = ReplyForm
    model = Reply
    template_name = 'wall/wall_detailed.html'

    def form_valid(self, form):
        reply = form.save(commit=False)
        reply.user = self.request.user
        reply.post_id = self.kwargs.get('pk')
        reply.save()
        return super().form_valid(form)


class PostDetails(DetailView, ReplyCreate):
    model = Post
    template_name = 'wall/wall_detailed.html'
    context_object_name = 'wall_detailed'
    queryset = Post.objects.all()
    reply_form = ReplyForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['replies'] = Reply.objects.filter(post__id=self.kwargs['pk']).order_by('reply_date')
        context['form'] = self.reply_form
        return context

    def form_valid(self, form):
        form.save(commit=False)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('wall.add_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'wall/wall_post_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('wall.change_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'wall/wall_post_update.html'

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.save(commit=False)
        return super().form_valid(form)


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('wall.delete_post',)
    raise_exception = True
    model = Post
    template_name = 'wall/wall_post_delete.html'
    success_url = "/wall/"


class UserPostList(ListView, LoginRequiredMixin):
    model = Post
    ordering = '-time_of_creation'
    template_name = 'wall/user_post_list.html'
    context_object_name = 'user_posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


@login_required
def reply_list(request):
    posts = Post.objects.filter(author=request.user)
    replies = Reply.objects.filter(post__in=posts)
    selected_post_id = request.GET.get('post_id')
    if selected_post_id:
        replies = replies.filter(post_id=selected_post_id)

    return render(request, 'wall/replies_to_user.html', {'posts': posts, 'replies': replies})


# @login_required
# def reply_confirm(request, reply_id, action):
#     reply = get_object_or_404(Reply, id=reply_id)
#     if action == 'confirm':
#         reply.confirm = 'confirmed'
#         subject = 'Ваш отклик принят автором объявления.'
#         message = f'Ваш отклик на объявление "{reply.post.name}" принят!'
#         html = (
#             f'<b>{request.user.username}</b>, Ваш отклик на объявление "{reply.post.name}" принят!'
#             f'<a href="http://127.0.0.1:8000/wall/{reply.post_id}">Просмотреть объявление.</a>!'
#         )
#     elif action == 'cancel':
#         reply.status = 'cancelled'
#         subject = 'Ваш отклик отклонен автором объявления.'
#         message = f'Ваш отклик на объявление "{reply.post.name}" отклонен!'
#         html = (
#             f'<b>{request.user.username}</b>, Ваш отклик на объявление "{reply.post.name}" отклонен!'
#             f'<a href="http://127.0.0.1:8000/wall/{reply.post_id}">Просмотреть объявление.</a>!'
#         )
#     else:
#         return HttpResponseBadRequest('Неправильный запрос!')
#
#     reply.save()
#
#     msg = EmailMultiAlternatives(
#         subject=subject, body=message, from_email=None, to=[request.user.email]
#     )
#     msg.attach_alternative(html, "text/html")
#     msg.send()
#
#     return redirect('post', post_id=reply.post.id)


@login_required
def confirm_reply(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)

    if request.user != reply.post.author:
        messages.error(request, 'Недостаточно прав для выполнения этого действия.')
        return redirect('replies_to_user')

    if reply.confirm != 'unknown':
        messages.error(request, 'Этот запрос уже обработан.')
        return redirect('replies_to_user')

    reply.confirm = 'confirmed'
    reply.save()

    # subject = f'Ваш запрос принят'
    # message = f'Ваш запрос на объявление "{reply.post.name}" был принят.'
    # from_email = settings.DEFAULT_FROM_EMAIL
    # recipient_list = [reply.author.email]
    #
    # send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    #
    # messages.success(request, 'Запрос успешно принят.')
    subject = 'Ваш отклик принят автором объявления.'
    message = f'Ваш отклик на объявление "{reply.post.name}" принят!'
    html = (
        f'<b>{request.user.username}</b>, Ваш отклик на объявление "{reply.post.name}" принят!'
        f'<a href="http://127.0.0.1:8000/wall/{reply.post_id}">Просмотреть объявление.</a>!'
    )
    msg = EmailMultiAlternatives(
        subject=subject, body=message, from_email=None, to=[request.user.email]
    )
    msg.attach_alternative(html, "text/html")
    msg.send()

    return redirect('replies_to_user')


@login_required
def cancel_reply(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)

    if request.user != reply.post.author:
        messages.error(request, 'Недостаточно прав для выполнения этого действия.')
        return redirect('replies_to_user')

    if reply.confirm != 'unknown':
        messages.error(request, 'Этот запрос уже обработан.')
        return redirect('replies_to_user')

    reply.confirm = 'cancelled'
    reply.save()

    # subject = f'Ваш запрос отклонен'
    # message = f'Ваш запрос на объявление "{reply.post.name}" был отклонен.'
    # from_email = settings.DEFAULT_FROM_EMAIL
    # recipient_list = [reply.author.email]
    #
    # send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    #
    # messages.success(request, 'Запрос успешно отклонен.')
    subject = 'Ваш отклик отклонен автором объявления.'
    message = f'Ваш отклик на объявление "{reply.post.name}" отклонен!'
    html = (
        f'<b>{request.user.username}</b>, Ваш отклик на объявление "{reply.post.name}" отклонен!'
        f'<a href="http://127.0.0.1:8000/wall/{reply.post_id}">Просмотреть объявление.</a>!'
    )

    msg = EmailMultiAlternatives(
        subject=subject, body=message, from_email=None, to=[request.user.email]
    )
    msg.attach_alternative(html, "text/html")
    msg.send()

    return redirect('replies_to_user')