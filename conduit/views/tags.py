from flask_jwt_extended import jwt_required
from flask_classful import FlaskView, route

from webargs import fields
from webargs.flaskparser import parser

from ..models import Tag, db
from . import api
from .schemas import tags_schema

class TagsView(FlaskView):
    def index(self):
        tag_names = [tag.name for tag in Tag.all()]
        return tags_schema.jsonify({'tags': tag_names})

TagsView.register(api, trailing_slash=False)
