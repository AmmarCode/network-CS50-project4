from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields import BooleanField, CharField
from django.db.models.fields.related import ForeignKey
from django.utils import timezone


class User(AbstractUser):
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username
        }


class Following(models.Model):
    followed = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followed_users')
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followers')

    def serialize(self):
        return {
            "followed": self.followed,
            "follower": self.follower
        }


class Post(models.Model):
    content = models.CharField(max_length=600)
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               default=None, related_name='user_post')
    like_status = models.BooleanField(default=False)
    like = models.ManyToManyField(User, blank=True, related_name='liked_posts')

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "date": self.date,
            "author": self.author,
            "like_status": self.like_status,
            "like": [user.username for user in self.like.all()]
        }
