from flask import request
from flask_jwt_extended import jwt_required
from flask_classful import FlaskView, route

from sqlalchemy.exc import IntegrityError

from ..models import User, db
from . import api
from .schemas import profile_schema
from ..utils import jwt_optional


class ProfilesView(FlaskView):
    @jwt_optional
    def index(self, username):
        """
            Get Profile
        """
        user = User.find_by_username(username)
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
