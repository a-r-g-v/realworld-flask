from .. import ma
from app.models import User, Article
from marshmallow import fields, pre_dump

class _UserSchema(ma.Schema):
    email = fields.Email()
    token = fields.String()
    username = fields.String()
    bio =  fields.String()
    image = fields.URL()
    following = fields.Boolean(default=None)

class UserSchema(ma.Schema):
    user = fields.Nested(_UserSchema, only=["email", "token", "username", "bio", "image"])

class ProfileSchema(ma.Schema):
    profile = fields.Nested(_UserSchema, only=["username", "bio", "image", "following"])

class _ArticleSchema(ma.Schema):
    slug = fields.String()
    title = fields.String()
    description = fields.String()
    body = fields.String()
    createdAt = fields.DateTime()
    updatedAt = fields.DateTime()
    favorited = fields.Boolean()
    favoritesCount = fields.Integer()
    tagList = fields.List(fields.String())
    author = fields.Nested(_UserSchema, only=["username", "bio", "image", "following"])

class ArticleSchema(ma.Schema):
    article = fields.Nested(_ArticleSchema)

class ArticlesSchema(ma.Schema):
    articles = fields.Nested(_ArticleSchema, many=True)
    articlesCount =  fields.Integer()

    @pre_dump(pass_many=False)
    def calucate_count(self, data):
        if 'articlesCount' not in data:
            data['articlesCount'] = len(data['articles'])
        return data




class TagsSchema(ma.Schema):
    tags = fields.List(fields.String())




user_schema = UserSchema()
profile_schema = ProfileSchema()
article_schema = ArticleSchema()
articles_schema = ArticlesSchema()
tags_schema = TagsSchema()
