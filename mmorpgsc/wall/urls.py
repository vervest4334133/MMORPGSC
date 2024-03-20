from django.conf.urls.static import static
from django.urls import path

from mmorpgsc import settings

from .views import *


urlpatterns = [
   path('', PostList.as_view()),
   path('<int:pk>', PostDetails.as_view(), name='post_detail'),
   path('post_create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('<int:pk>/reply/create', ReplyCreate.as_view(), name='reply_create'),
   path('posts_profile/', UserPostList.as_view(), name='user_posts'),
   path('replies/', ReplyList.as_view(), name='replies_to_user'),
   path('replies/<int:reply_id>/reply_confirm/<str:action>/', reply_confirm, name='reply_confirm'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)