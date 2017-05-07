from flask import request, jsonify
from flask_jwt_extended import jwt_required
from flask_classful import FlaskView, route

from webargs import fields
from webargs.flaskparser import parser

from ..models import Article, db, User
from . import api
from .schemas import article_schema, articles_schema, comment_schema, comments_schema
from ..utils import jwt_optional


class ArticlesView(FlaskView):

    index_article_args = {
        'tag': fields.Str(),
        'author': fields.Str(),
        'favorited': fields.Str(),
        'limit': fields.Integer(),
        'offset': fields.Integer()
    }

    @jwt_optional
    def index(self):
        """
            List Articles
        """
        args = parser.parse(self.index_article_args)
        articles = Article.recent(**args)
        return articles_schema.jsonify({'articles': articles})

    feed_article_args = {'limit': fields.Integer(), 'offset': fields.Integer()}

    @jwt_required
    def feed(self):
        """
            Feed Articles
        """
        args = parser.parse(self.feed_article_args)
        logged_user = User.get_logged_user()
        articles = logged_user.feed_article(**args)
        return articles_schema.jsonify({'articles': articles})

    @jwt_optional
    def get(self, slug):
        """
            Get Article
        """
        article = Article.find_by_slug(slug)
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
        return jsonify(), 200

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

    post_comment_args = {
        'comment':
        fields.Nested({
            'body': fields.Str(required=True)
        }, required=True)
    }

    @route('<slug>/comments', methods=['GET'])
    @jwt_optional
    def get_comment(self, slug):
        """
            Get Comments from an Article
        """
        article = Article.find_by_slug(slug)
        comments = article.comments
        return comments_schema.jsonify({'comments': comments})

    @route('<slug>/comments', methods=['POST'])
    @jwt_required
    def post_comment(self, slug):
        """
            Add Comments to an Article
        """
        args = parser.parse(self.post_comment_args)
        logged_user = User.get_logged_user()
        article = Article.find_by_slug(slug)
        comment = logged_user.create_comment(article, args['comment'])
        db.session.add(comment)
        db.session.commit()
        return comment_schema.jsonify({'comment': comment})

    @route('<slug>/comments/<comment_id>', methods=['DELETE'])
    @jwt_required
    def delete_comment(self, slug, comment_id):
        """
            Delete Comment
        """
        # pylint: disable=unused-argument
        logged_user = User.get_logged_user()
        comment = logged_user.find_my_comment_by_id(comment_id)
        comment.delete()
        db.session.commit()
        return jsonify(), 200


ArticlesView.register(api, trailing_slash=False)
