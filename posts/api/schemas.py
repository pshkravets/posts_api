from ninja import Schema, ModelSchema
from .models import Post, Comment


class PostsSchema(Schema):
    id: int
    context: str
    author: str
    created_at: str


class CommentsSchema(Schema):
    id: int
    context: str
    author: str
    post: int
    created_at: str



class PostCreateSchema(Schema):
    context: str


class CommentCreateSchema(Schema):
    context: str
