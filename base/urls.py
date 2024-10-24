from django.urls import path
from .views import Home, PostDetail, Profile


urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('post/<str:pk>/', PostDetail.as_view(), name='post-detail'),


  path('profile/<str:pk>/', Profile.as_view(), name='profile'),
]