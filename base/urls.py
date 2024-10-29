from django.urls import path
from .views import Home, PostDetail, PostEdit, PostDelete ,PostLike, PostDislike,Profile


urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('post/<str:pk>/', PostDetail.as_view(), name='post-detail'),
  path('post/edit/<str:pk>/', PostEdit.as_view(), name='edit-post'),
  path('post/delete/<str:pk>/', PostDelete.as_view(), name='delete-post'),
  path('post/<str:pk>/like/', PostLike.as_view(), name='like'),
  path('post/<str:pk>/dislike/', PostDislike.as_view(), name='dislike'),

  path('profile/<str:pk>/', Profile.as_view(), name='profile'),
]