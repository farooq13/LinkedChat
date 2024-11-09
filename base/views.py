from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Post, Comment, UserProfile, Notification
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

         notification =  Notification(
            notification_type=2,
            from_user=comment.author,
            to_user=post.author,
            post=post
         )

      context = {
         'form': form,
         'post': post,
         'comments': comments,
         'notification': notification
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


class PostLike(LoginRequiredMixin, View):
  def post (self, request, pk, *args, **kwargs):
    post = get_object_or_404(Post, pk=pk)
    user = request.user

    if user in post.likes.all():
      post.likes.remove(user)
    if user in post.dislikes.all():
      post.dislikes.remove(request.user)
    else:
      post.likes.add(user)

      notification = Notification(
         notification_type=1,
         from_user=request.user,
         to_user=post.author
      )

    next = request.POST.get('next')
    return HttpResponseRedirect(next)
  
class PostDislike(LoginRequiredMixin, View):
  def post(self, request, pk, *args, **kwargs):
    post = get_object_or_404(Post, pk=pk)
    user = request.user

    if user in post.dislikes.all():
      post.dislikes.remove(user)
    if user in post.likes.all():
      post.likes.remove(user)
    else:
      post.dislikes.add(user)

    next = request.POST.get('next')
    return HttpResponseRedirect(next)


class Profile(View):
   def get(self, request, pk, *args, **kwargs):
      profile = UserProfile.objects.get(pk=pk)
      user = profile.user
      posts = Post.objects.filter(author=user)
      followers = profile.followers.all()
      number_of_followers = len(followers)

      is_following = False

      for follower in followers:
         if followers == request.user:
            is_following = True
         is_following = True

      context = {
         'profile': profile,
         'user': user,
         'posts': posts,
         'followers': followers,
         'number_of_followers': number_of_followers,
         'is_following': is_following
      }
      return render(request, 'base/profile.html', context)



class ProfileEdit(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
      model = UserProfile
      fields = ['picture', 'name', 'location', 'bio', 'birth_date']
      template_name = 'base/profile_edit.html'


      def get_success_url(self):
         pk = self.kwargs['pk']
         return reverse_lazy('profile', kwargs={'pk': pk})
      

      def test_func(self):
         profile = self.get_object()
         return self.request.user == profile.user


class Follow(LoginRequiredMixin, View):
   def post(self, request, pk, *args, **kwargs):
      profile = UserProfile.objects.get(pk=pk)
      profile.followers.add(request.user)

      notification = Notification(
         notification_type=3, 
         from_user=request.user, 
         to_user=profile.user
         )

      return redirect('profile', pk=profile.pk)


class UnFollow(LoginRequiredMixin, View):
   def post(self, request, pk, *args, **kwargs):
      profile = UserProfile.objects.get(pk=pk)
      profile.followers.remove(request.user)

      return redirect('profile', pk=profile.pk)



class PostNotification(View):
   def get(self, request, notification_pk, post_pk, *args, **kwargs):
      notification = Notification.objects.get(pk=notification_pk)
      post = Post.objects.get(pk=post_pk)
      notification.user_has_seen = True
      notification.save()
      
      return   redirect('post-detail', pk=post.pk)
   


class FollowNotification(View):
   def get(self, request, notification_pk, profile_pk, *args, **kwargs):
      notification = Notification.objects.get(pk=notification_pk)
      profile = UserProfile.objects.get(pk=profile_pk)

      notification.user_has_seen = True
      notification.save()
      return redirect('profile', pk=profile_pk)
   


class userSearch(View):
   def get(self, request, *args, **kwargs):
      query = request.GET.get('query')
      profile_list = UserProfile.objects.filter(
         Q(user__username__icontains=query)
      )

      context = {
         'query': query,
         'profile_list': profile_list
      }
      return render(request, 'base/search.html', context)

