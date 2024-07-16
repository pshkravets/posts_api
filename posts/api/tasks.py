from celery import shared_task

from .models import Comment, Post
from users.models import MyUser
from .utils import create_auto_comment


@shared_task
def auto_reply_comment(post_id):
    author = MyUser.objects.get(email='auto_replier@gmail.com')
    post = Post.objects.get(id=post_id)
    comment_text = create_auto_comment(post.context)
    Comment.objects.create(author=author, post=post, context=comment_text)
    