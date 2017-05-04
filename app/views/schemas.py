from .. import ma
from app.models import User, Article
from marshmallow import fields

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

class ArticleSchema(ma.Schema):
    slug = fields.String()
    title = fields.String()
    description = fields.String()
    body = fields.String()
    createdAt = fields.DateTime()
    updatedAt = fields.DateTime()
    favorited = fields.Boolean()
    favoritesCount = fields.Integer()
    author = fields.Nested(_UserSchema, only=["username", "bio", "image", "following"])

class ArticlesSchema(ma.Schema):
    articles = fields.Nested(ArticleSchema, many=True)
    articlesCount = fields.Function(lambda obj: len(obj.articles))




user_schema = UserSchema()
profile_schema = ProfileSchema()
article_schema = ArticleSchema()
articles_schema = ArticlesSchema()
