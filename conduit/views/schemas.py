from .. import ma
from ..models import User
from marshmallow import fields, pre_dump


class _UserSchema(ma.Schema):
    email = fields.Email()
    token = fields.String()
    username = fields.String()
    bio = fields.String()
    image = fields.URL()
    following = fields.Boolean(default=None)

    @pre_dump(pass_many=False)
    def fill_following(self, data):
        logged_user = User.get_logged_user(raise_exceptipn=False)
        if logged_user:
            data.following = data.is_following_by(logged_user)
        return data


class UserSchema(ma.Schema):
    user = fields.Nested(
        _UserSchema, only=["email", "token", "username", "bio", "image"])


class ProfileSchema(ma.Schema):
    profile = fields.Nested(
        _UserSchema, only=["username", "bio", "image", "following"])


class _ArticleSchema(ma.Schema):
    slug = fields.String()
    title = fields.String()
    description = fields.String()
    body = fields.String()
    createdAt = fields.DateTime(attribute='created_at')
    updatedAt = fields.DateTime(attribute='updated_at')
    favorited = fields.Boolean(default=None)
    favoritesCount = fields.Integer(default=0)
    tagList = fields.List(fields.String())
    author = fields.Nested(
        _UserSchema, only=["username", "bio", "image", "following"])

    @pre_dump(pass_many=False)
    def fill_favorited(self, data):
        logged_user = User.get_logged_user(raise_exceptipn=False)
        if logged_user:
            data.favorited = data.is_favorited_by(logged_user)
        return data


class ArticleSchema(ma.Schema):
    article = fields.Nested(_ArticleSchema)


class ArticlesSchema(ma.Schema):
    articles = fields.Nested(_ArticleSchema, many=True)
    articlesCount = fields.Integer(default=0)

    @pre_dump(pass_many=False)
    def calucate_count(self, data):
        if 'articlesCount' not in data:
            data['articlesCount'] = len(data['articles'])
        return data


class TagsSchema(ma.Schema):
    tags = fields.List(fields.String())


class _CommentSchema(ma.Schema):
    id = fields.Integer()
    body = fields.String()
    createdAt = fields.DateTime(attribute='created_at')
    updatedAt = fields.DateTime(attribute='updated_at')
    author = fields.Nested(
        _UserSchema, only=["username", "bio", "image", "following"])


class CommentSchema(ma.Schema):
    comment = fields.Nested(_CommentSchema)


class CommentsSchema(ma.Schema):
    comments = fields.Nested(_CommentSchema, many=True)


user_schema = UserSchema()
profile_schema = ProfileSchema()
article_schema = ArticleSchema()
articles_schema = ArticlesSchema()
tags_schema = TagsSchema()
comment_schema = CommentSchema()
comments_schema = CommentsSchema()
