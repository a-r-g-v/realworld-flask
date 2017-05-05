from flask_classful import FlaskView
from ..models import Tag
from . import api
from .schemas import tags_schema


class TagsView(FlaskView):
    def index(self):
        tag_names = [tag.name for tag in Tag.all()]
        return tags_schema.jsonify({'tags': tag_names})


TagsView.register(api, trailing_slash=False)
