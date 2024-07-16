from django.db import models

from users.models import MyUser


class Post(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, to_field='email')
    context = models.CharField(max_length=2000)
    created_at = models.DateField(auto_now_add=True)

    def as_dict(self):
        return {
            'id': self.id,
            'context': self.context,
            'author': self.author.email,
            'created_at': self.created_at.isoformat()
        }


class Comment(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, default=None)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    context = models.CharField(max_length=2000, default=None)
    created_at = models.DateField(auto_now_add=True)

    def as_dict(self):
        return {
            'id': self.id,
            'context': self.context,
            'author': self.author.email,
            'post': self.post.id,
            'created_at': self.created_at.isoformat()
        }


class CommentStatistic(models.Model):
    created_at = models.DateField(auto_now_add=True)
    blocked = models.BooleanField(default=False)