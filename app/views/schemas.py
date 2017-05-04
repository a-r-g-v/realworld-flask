from .. import ma
from app.models import User, Article
from marshmallow import fields

class _UserSchema(ma.ModelSchema):
    class Meta:
        model = User

class UserSchema(ma.Schema):
    user = fields.Nested(_UserSchema, only=["email", "token", "username", "bio", "image"])

class ProfileSchema(ma.Schema):
    profile = fields.Nested(_UserSchema, only=["username", "bio", "image", "following"])

class ArticleSchema(ma.ModelSchema):
    class Meta:
        model = Article



user_schema = UserSchema()
profile_schema = ProfileSchema()
article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)
