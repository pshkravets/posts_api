import json

from django.test import TestCase, Client
from ninja.testing import TestClient

from ..api import api, router
from ..models import Post, Comment, CommentStatistic
from ..utils import comments_statistic_counting
from users.models import MyUser


class TestAPI(TestCase):

    def setUp(self):
        self.client = TestClient(router)
        self.user = MyUser.objects.create_user(
            email='pashkevuchpasha@gmail.com',
            password='qwe123',
            date_of_birth='2222-12-22'
        )
        self.another_user = MyUser.objects.create_user(
            email='something@gmail.com',
            password='qwe123',
            date_of_birth='2222-12-22'
        )
        self.post = Post.objects.create(author=self.user, context='this post is for testing')
        self.comment = Comment.objects.create(author=self.user, post=self.post, context='this comment is for testing')

    def test_GET_list_posts(self):
        response = self.client.get('/v1/posts/')
        assert response.status_code == 200

    def test_GET_post(self):
        response = self.client.get(f'/v1/posts/{self.post.id}')
        response_post = json.loads(response.content.decode('utf-8'))
        assert response.status_code == 200
        assert self.post.context == response_post['context']
        assert self.post.author.email == MyUser.objects.get(email=response_post['author']).email

    def test_POST_create_post(self):
        payload = {'context': 'testing post request'}
        response = self.client.post(f'/v1/posts?jwt_token={self.user.jwt_token}', json=payload)
        assert response.status_code == 200
        post_id = json.loads(response.content.decode('utf-8'))['id']
        created_post = Post.objects.get(id=post_id)
        assert created_post.context == payload['context']
        assert created_post.author.email == self.user.email

    def test_PUT_post(self):
        payload = {'context': 'changing context of post to a new value'}
        response = self.client.put(f'/v1/posts/{self.post.id}?jwt_token={self.user.jwt_token}', json=payload)
        response_from_another_user = self.client.put(
            f'/v1/posts/{self.post.id}?jwt_token={self.another_user.jwt_token}', json={'context': 'should show 403'}
        )
        updated_post = Post.objects.get(id=self.post.id)
        assert response.status_code == 200
        assert updated_post.context == payload['context']
        assert response_from_another_user.status_code == 403

    def test_DELETE_post(self):
        from_another_user_response = self.client.delete(
            f'/v1/posts/{self.post.id}?jwt_token={self.another_user.jwt_token}'
        )
        assert from_another_user_response.status_code == 403
        assert Post.objects.filter(id=self.post.id).exists()
        response = self.client.delete(
            f'/v1/posts/{self.post.id}?jwt_token={self.user.jwt_token}'
        )
        assert response.status_code == 200
        assert not Post.objects.filter(id=self.post.id).exists()

    def test_GET_list_comments(self):
        response = self.client.get(f'/v1/posts/{self.post.id}/comments')
        assert response.status_code == 200

    def test_GET_comment(self):
        response = self.client.get(f'/v1/comments/{self.comment.id}')
        response_comment = json.loads(response.content.decode('utf-8'))
        assert response.status_code == 200
        assert response_comment['context'] == self.comment.context

    def test_POST_comment(self):
        response = self.client.post(
            f'/v1/posts/{self.post.id}/comments?jwt_token={self.user.jwt_token}',
            json={'context': 'this is new comment'}
        )
        response_comment = json.loads(response.content.decode('utf-8'))
        comment_created = Comment.objects.get(id=response_comment['id'])
        assert response.status_code == 200
        assert comment_created.author.email == self.user.email
        assert comment_created.context == 'this is new comment'

    def test_PUT_comment(self):
        response_from_another_user = self.client.put(
            f'/v1/comments/{self.comment.id}?jwt_token={self.another_user.jwt_token}',
            json={'context': 'This is changed comment'}
        )
        response = self.client.put(
            f'/v1/comments/{self.comment.id}?jwt_token={self.user.jwt_token}',
            json={'context': 'This is changed comment'}
        )
        updated_comment = Comment.objects.get(id=self.comment.id)
        assert response_from_another_user.status_code == 403
        assert response.status_code == 200
        assert updated_comment.context == 'This is changed comment'

    def test_DELETE_comment(self):
        from_another_user_response = self.client.delete(
            f'/v1/comments/{self.comment.id}?jwt_token={self.another_user.jwt_token}'
        )
        assert from_another_user_response.status_code == 403
        assert Comment.objects.filter(id=self.comment.id).exists()
        response = self.client.delete(
            f'/v1/comments/{self.comment.id}?jwt_token={self.user.jwt_token}'
        )
        assert response.status_code == 200
        assert not Comment.objects.filter(id=self.comment.id).exists()

    def test_comments_daily_breakdown(self):
        date_from = '2024-07-01'
        date_to = '2024-07-09'
        response = self.client.get(f'/v1/comments-daily-breakdown?date_from={date_from}&date_to={date_to}')
        response_result = json.loads(response.content.decode('utf-8'))
        result = comments_statistic_counting(date_from, date_to)
        assert response.status_code == 200
        assert response_result == result