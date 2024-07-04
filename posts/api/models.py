from django.db import models

from users.models import MyUser


class Post(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    context = models.CharField(max_length=2000)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)