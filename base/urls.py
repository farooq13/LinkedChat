from django.urls import path
from .views import Home, PostDetail, PostEdit, PostDelete ,PostLike, PostDislike, Profile, ProfileEdit, Follow, UnFollow, PostNotification, FollowNotification


urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('post/<str:pk>/', PostDetail.as_view(), name='post-detail'),
  path('post/edit/<str:pk>/', PostEdit.as_view(), name='edit-post'),
  path('post/delete/<str:pk>/', PostDelete.as_view(), name='delete-post'),
  path('post/<str:pk>/like/', PostLike.as_view(), name='like'),
  path('post/<str:pk>/dislike/', PostDislike.as_view(), name='dislike'),

  path('profile/<str:pk>/', Profile.as_view(), name='profile'),
  path('profile/<str:pk>/followers/add/', Follow.as_view(), name='follow'),
  path('profile/<str:pk>/followers/remove', UnFollow.as_view(), name='unfollow'),
  path('profile/<str:pk>/edit/', ProfileEdit.as_view(), name='profile-edit'),

  path('notification/<str:notification_pk>/post/<str:post_pk>/', PostNotification.as_view(), name='post-notification'),
  path('notification/<str:notification_pk>/profile/<str:profile_pk>/', FollowNotification.as_view(), name='follow-notification'),
]