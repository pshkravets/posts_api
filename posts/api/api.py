from ninja import NinjaAPI, Router
from typing import List
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden

from .schemas import PostsSchema, CommentsSchema, PostCreateSchema, CommentCreateSchema
from .models import Post, Comment, CommentStatistic
from .utils import ApiKey, text_valid, comments_statistic_counting
from users.models import MyUser
from .tasks import auto_reply_comment

api = NinjaAPI()
api_key = ApiKey()
router = Router()


@router.get('/v1/posts/', response=List[PostsSchema])
def list_posts(request):
    posts = Post.objects.all()
    return [post.as_dict() for post in posts]


@router.get('/v1/posts/{post_id}', response=PostsSchema)
def retrieve_post(request, post_id: int):
    post = get_object_or_404(Post, id=post_id)
    return post.as_dict()


@router.post('/v1/posts', auth=api_key)
def create_post(request, payload: PostCreateSchema, jwt_token):
    data = payload.dict()
    if text_valid(data['context']) == 'True':
        return {'error': 'Your post contains obscene language.'}
    author = api_key.authenticate(request, jwt_token)
    post = Post.objects.create(author=author, context=data['context'])
    if author.auto_reply_enabled:
        auto_reply_comment.apply_async((post.id,), countdown=author.reply_delay)
    return {'id': post.id}


@router.put('/v1/posts/{post_id}', auth=api_key)
def update_post(request, post_id: int, payload: PostCreateSchema, jwt_token):
    data = payload.dict()
    if text_valid(data['context']) == 'True':
        return {'error': 'Your post contains obscene language.'}
    post = get_object_or_404(Post, id=post_id)
    sender = api_key.authenticate(request, jwt_token)
    if sender == post.author:
        post.context = data['context']
        post.save()
        return {'success': True}
    return HttpResponseForbidden({'error': 'You are not author of this post'})


@router.delete('/v1/posts/{post_id}', auth=api_key)
def post_delete(request, post_id: int, jwt_token):
    post = get_object_or_404(Post, id=post_id)
    sender = api_key.authenticate(request, jwt_token)
    if sender == post.author:
        post.delete()
        return {'success': True}
    return HttpResponseForbidden({'error': 'You are not author of this post'})


@router.get('/v1/posts/{post_id}/comments', response=List[CommentsSchema])
def comments_list(request, post_id: int):
    comments = Comment.objects.filter(post__id=post_id)
    return [comment.as_dict() for comment in comments]


@router.get('/v1/comments/{comment_id}', response=CommentsSchema)
def retrieve_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    return comment.as_dict


@router.post('/v1/posts/{post_id}/comments', auth=api_key)
def create_comment(request, payload: CommentCreateSchema, jwt_token, post_id):
    data = payload.dict()
    if text_valid(data['context']) == 'True':
        CommentStatistic.objects.create(blocked=True)
        return {'error': 'Your comment contains obscene language.'}
    post = get_object_or_404(Post, id=post_id)
    author = api_key.authenticate(request, jwt_token)
    comment = Comment.objects.create(author=author, post=post,  context=data['context'])
    CommentStatistic.objects.create(blocked=False)

    return {'id': comment.id}


@router.put('/v1/comments/{comment_id}', auth=api_key)
def comment_update(request, comment_id: int, payload: CommentCreateSchema, jwt_token):
    data = payload.dict()
    if text_valid(data['context']) == 'True':
        return {'error': 'Your post comment obscene language.'}
    comment = get_object_or_404(Comment, id=comment_id)
    sender = api_key.authenticate(request, jwt_token)
    if sender == comment.author:
        comment.context = data['context']
        comment.save()
        return {'succes': True}
    return HttpResponseForbidden({'error': 'You are not author of this comment'})


@router.delete('/v1/comments/{comment_id}', auth=api_key)
def comment_delete(request, comment_id: int, jwt_token):
    sender = api_key.authenticate(request, jwt_token)
    comment = get_object_or_404(Comment, id=comment_id)
    if sender == comment.author:
        comment.delete()
        return {'success': True}
    return HttpResponseForbidden({'error': 'You are not author of this comment'})


@router.get('v1/comments-daily-breakdown')
def comments_statistic(request, date_from, date_to):
    result = comments_statistic_counting(date_from, date_to)
    return result


api.add_router("", router)
