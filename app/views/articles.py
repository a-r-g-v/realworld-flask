from flask_jwt_extended import jwt_required
from flask_classful import FlaskView, route

from webargs import fields
from webargs.flaskparser import parser

from app.models import Article, db
from . import api
from .schemas import article_schema, articles_schema

class ArticlesView(FlaskView):
    def index(self):
        """
            List Articles
        """
        pass

    def feed(self):
        """
            Feed Articles
        """
        pass

    def get(self, slug):
        """
            Get Article
        """
        pass

    def post(self):
        """
            Post Article
        """
        pass

    def update(self, slug):
        """
            Update Article
        """
        pass

    def delete(self, slug):
        """
            Update Article
        """
        pass

    @route('<username>/favorite', methods=['POST', 'DELETE'])
    @jwt_required
    def follow(self, slug):
        """
            Follow And Unfollow Article
        """
        pass

ArticlesView.register(api, trailing_slash=False)
