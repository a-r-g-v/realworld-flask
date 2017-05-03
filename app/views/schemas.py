from .. import ma
from app.models import User
from marshmallow import fields

class _UserSchema(ma.ModelSchema):
    class Meta:
        model = User

class UserSchema(ma.Schema):
    user = fields.Nested(_UserSchema, only=["email", "token", "username", "bio", "image"])

class ProfileSchema(ma.Schema):
    profile = fields.Nested(_UserSchema, only=["username", "bio", "image", "following"])

user_schema = UserSchema()
profile_schema = ProfileSchema()
