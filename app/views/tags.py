from flask_jwt_extended import jwt_required
from flask_classful import FlaskView, route

from webargs import fields
from webargs.flaskparser import parser

from app.models import User, db
from . import api
from .schemas import user_schema

class TagsView(FlaskView):
    def index(self):
        pass

TagsView.register(api, trailing_slash=False)
