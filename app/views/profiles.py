from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_classful import FlaskView, route

from sqlalchemy.exc import IntegrityError

from webargs import fields
from webargs.flaskparser import parser


from app.models import User, db
from . import api
from .. import ma
from .schemas import profile_schema
from app.utils import jwt_optional


class ProfilesView(FlaskView):

    @jwt_optional
    def index(self, username):
        """
i           Get Profile
        """
        user = User.find_by_username(username)
        logged_user = User.get_logged_user(raise_exceptipn=False)
        if logged_user:
            user.following = user.is_following_by(logged_user)
        return profile_schema.jsonify({'profile': user})

    @route('<username>/follow', methods=['POST', 'DELETE'])
    @jwt_required
    def follow(self, username):
        """
            Follow And Unfollow User
        """
        user = User.find_by_username(username)
        logged_user = User.get_logged_user()
        if request.method == 'POST':
            logged_user.follow(user)

        elif request.method == 'DELETE':
            logged_user.unfollow(user)

        try:
            db.session.commit()
        except IntegrityError:
            # When the user tries to follow the already followee user, 
            # SQLAlchemy raise IntegrityError.
            # I should ignore this exception this time.
            db.session.rollback()
    
        return self.index(username)


ProfilesView.register(api, trailing_slash=False)
