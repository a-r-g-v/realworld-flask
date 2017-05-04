from flask import request
from flask_jwt_extended import jwt_required
from flask_classful import FlaskView, route

from webargs import fields
from webargs.flaskparser import parser

from app.models import Article, db, User
from . import api
from .schemas import article_schema, articles_schema
from app.utils import jwt_optional

class ArticlesView(FlaskView):
    def index(self):
        """
            List Articles
        """
        articles = Article.recent()
        return articles_schema.jsonify({'articles': articles})


    def feed(self):
        """
            Feed Articles
        """
        articles = Article.feed()
        return articles_schema.jsonify({'articles': articles})

    @jwt_optional
    def get(self, slug):
        """
            Get Article
        """
        article = Article.find_by_slug(slug)
        logged_user = User.get_logged_user(raise_exceptipn=False)
        if logged_user:
            article.favorited = article.is_favorited_by(logged_user)
        return article_schema.jsonify({'article': article})

    create_article_args = {
        'article':
        fields.Nested(
            {
                'title': fields.Str(required=True),
                'description': fields.Str(required=True),
                'body': fields.Str(required=True),
                'tagList': fields.List(fields.Str())
            },
            required=True)
    }

    @jwt_required
    def post(self):
        """
            Post Article
        """
        args = parser.parse(self.create_article_args)
        user = User.get_logged_user()
        new_article = user.create_article(args['article'])
        db.session.add(new_article)
        db.session.commit()
        return article_schema.jsonify({'article': new_article})

    update_article_args = {
        'article':
        fields.Nested(
            {
                'title': fields.Str(),
                'description': fields.Str(),
                'body': fields.Str(),
            },
            required=True)
    }
    @jwt_required
    def put(self, slug):
        """
            Update Article
        """
        args = parser.parse(self.update_article_args)
        user = User.get_logged_user()
        article = user.find_my_article_by_slug(slug)
        article.update(args)
        db.session.add(article)
        db.session.commit()
        return article_schema.jsonify({'article': article})

    @jwt_required
    def delete(self, slug):
        """
            Update Article
        """
        user = User.get_logged_user()
        article = user.find_my_article_by_slug(slug)
        article.delete()
        db.session.commit()
        return '', 200

    @route('<slug>/favorite', methods=['POST', 'DELETE'])
    @jwt_required
    def favorite(self, slug):
        """
            Favorite And Unfavorite Article
        """
        article = Article.find_by_slug(slug)
        logged_user = User.get_logged_user()
        if request.method == 'POST':
            logged_user.favorite_article(article)

        elif request.method == 'DELETE':
            logged_user.unfavorite_article(article)

        db.session.commit()
        return self.get(slug)


    @route('<slug>/comments', methods=['GET', 'POST'])
    def get_and_post_comment(self, slug):
        """
            Get Comments from an Article And Add Comments to an Article
        """
        pass
    
    @route('<slug>/comments/<id>', methods=['DELETE'])
    @jwt_required
    def delete_comment(self, slug, comment_id):
        """
            Delete Comment
        """
        pass

ArticlesView.register(api, trailing_slash=False)
