from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



class Post(models.Model):
  body = models.TextField()
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  created = models.DateTimeField(default=timezone.now)
  
  class Meta:
    ordering = ['-created']

  def __str__(self):
    return self.body[0:50]
  


class Comment(models.Model):
  comment = models.TextField()
  post = models.ForeignKey(Post, on_delete=models.CASCADE)
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  created =models.DateTimeField(default=timezone.now)

  class Meta:
    ordering = ['-created']

  
  def __str__(self):
    return self.comment[0:50]
  

class UserProfile(models.Model):
  user = models.OneToOneField(User, verbose_name='user', related_name='profile', on_delete=models.CASCADE)
  name = models.CharField(max_length=100, null=True, blank=True)
  location = models.CharField(max_length=50, null=True, blank=True)
  birth_date = models.DateField(default=timezone.now, null=True, blank=True)
  bio = models.TextField(max_length=200, null=True, blank=True)
  picture = models.ImageField(default='avatar.svg', null=True)
  followers = models.ManyToManyField(User, related_name='followers', blank=True)


  def __str__(self):
    return self.name
  

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
  if created:
    UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kargs):
  instance.profile.save()