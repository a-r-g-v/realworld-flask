from flask_jwt_extended import jwt_required
from flask_classful import FlaskView, route

from webargs import fields
from webargs.flaskparser import parser

from ..models import User, db
from . import api
from .schemas import user_schema


class UsersView(FlaskView):

    login_args = {
        'user':
        fields.Nested(
            {
                'email': fields.Str(required=True),
                'password': fields.Str(required=True)
            },
            required=True)
    }

    @route('login', methods=['POST'])
    def login(self):
        """
            Authentication
        """
        args = parser.parse(self.login_args).get('user')
        user = User.authenticate(args['email'], args['password'])
        return user_schema.jsonify({'user': user})

    registration_args = {
        'user':
        fields.Nested(
            {
                'username': fields.Str(required=True),
                'email': fields.Str(required=True),
                'password': fields.Str(required=True)
            },
            required=True)
    }

    def post(self):
        """
            Registration
        """
        args = parser.parse(self.registration_args)
        new_user = User.new(args)
        db.session.add(new_user)
        db.session.commit()
        return user_schema.jsonify({'user': new_user})


class UserView(FlaskView):
    decorators = [jwt_required]

    def index(self):
        """
            Get Current User
        """
        return user_schema.jsonify({'user': User.get_logged_user()})

    update_args = {
        'user':
        fields.Nested(
            {
                'username': fields.Str(),
                'email': fields.Str(),
                'password': fields.Str(),
                'image': fields.Str(allow_none=True),
                'bio': fields.Str(allow_none=True)
            },
            required=True, allow_missing=True)
    }

    def put(self):
        """
            Update User
        """
        args = parser.parse(self.update_args)
        user = User.get_logged_user()
        user.update(args)
        db.session.add(user)
        db.session.commit()
        return user_schema.jsonify({'user': user})


UsersView.register(api, trailing_slash=False)
UserView.register(api, trailing_slash=False)
