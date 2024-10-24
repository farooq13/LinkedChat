from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from .models import Post, Comment, UserProfile
from .forms import PostForm



class Home(View):
   def get(self, request, *args, **kwargs):
      form = PostForm()
      posts = Post.objects.filter(
         # Q(author__profile__followers_in=[request.user.id])|
         Q(author=request.user)
      )

      context = {
         'form': form,
         'posts': posts
      }
      return render(request, 'base/index.html', context)
   
   def post(self, request, *args, **kwargs):
      form = PostForm(request.POST)

      if form.is_valid():
         post = form.save(commit=False)
         post.author = request.user
         post.save()
         return redirect('home')
      
      context = {
         'form': form
      }
      return render(request, 'base/index.html', context)
   


class PostDetail(View):
   def get(self, request, pk, *args, **kwargs):
      post = Post.objects.get(pk=pk)

      context = {
         'post': post
      }
      return render(request, 'base/post_detail.html', context)
   

class Profile(View):
   def get(self, request, pk, *args, **kwargs):
      profile = UserProfile.objects.get(pk=pk)
      user = profile.user
      posts = Post.objects.filter(author=user)

      context = {
         'profile': profile,
         'user': user,
         'posts': posts
      }
      return render(request, 'base/profile.html', context)

