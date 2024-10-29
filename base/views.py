from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Post, Comment, UserProfile
from .forms import PostForm, CommentForm



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
      form = CommentForm()
      comments = Comment.objects.filter(post=post)


      context = {
         'post': post,
         'form': form,
         'comments': comments
      }
      return render(request, 'base/post_detail.html', context)
   
   def post(self, request, pk, *args, **kwargs):
      form = CommentForm(request.POST)
      post = Post.objects.get(pk=pk)
      comments = Comment.objects.filter(post=post)

      if form.is_valid():
         comment = form.save(commit=False)
         comment.author = request.user
         comment.post = post
         comment.save()

      context = {
         'form': form,
         'post': post,
         'comments': comments
      }
      return render(request, 'base/post_detail.html', context)


class PostEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
   model = Post
   fields = ['body']
   template_name = 'base/post_edit.html'


   def get_success_url(self):
      pk = self.kwargs['pk']
      return reverse_lazy('post-detail', kwargs={'pk': pk})
   
   def test_func(self):
      post = self.get_object()
      return self.request.user == post.author
   

class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
   model = Post
   template_name = 'base/post_delete.html'
   success_url = reverse_lazy('home')


   def test_func(self):
      post = self.get_object()
      return self.request.user == post.author


class PostLike(View):
   def post(self, request, pk, *args, **Kwargs):
      post = get_object_or_404(Post, pk=pk)
      user = request.user

      if user in post.likes.all():
         post.likes.remove(user)
      if user in post.dislikes.all():
         post.dislikes.remove(user)
         post.likes.add(user)

      next = request.POST.get('next')
      return HttpResponseRedirect(next)

class PostDislike(View):
   def post(self, request, pk, *args, **kwargs):
      post = get_object_or_404(Post, pk=pk)
      user = request.user

      if user in post.dislikes.all():
         post.dislikes.remove(user)
      if user in post.likes.all():
         post.likes.remove(user)
         post.dislikes.add(user)

      next = request.POST.get('next')
      return HttpResponseRedirect(next)

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

