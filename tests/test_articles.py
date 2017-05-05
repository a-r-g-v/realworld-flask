from . import BaseTestCase, make_client_kwargs, generate_user, generate_article, generate_comment
from .test_users import UserUseCase
from flask import url_for

class ArticlesUseCase(object):

    def list_articles(self, token=None, **kwargs):
        return self.client.get(url_for('api.ArticlesView:index'), **make_client_kwargs(query_string=kwargs, token=token))

    def feed_articles(self, token, **kwargs):
        return self.client.get(url_for('api.ArticlesView:feed'), **make_client_kwargs(query_string=kwargs, token=token))

    def get_article(self, slug, token=None):
        return self.client.get(url_for('api.ArticlesView:get', slug=slug), **make_client_kwargs(token=token))

    def post_article(self, token, article):
        return self.client.post(url_for('api.ArticlesView:post'), **make_client_kwargs(token=token, json=article))

    def update_article(self, token, slug, article):
        return self.client.put(url_for('api.ArticlesView:put', slug=slug), **make_client_kwargs(token=token, json=article))
    
    def delete_article(self, token, slug):
        return self.client.delete(url_for('api.ArticlesView:delete', slug=slug), **make_client_kwargs(token=token))

    def favorite_article(self, token, slug):
        return self.client.post(url_for('api.ArticlesView:favorite', slug=slug), **make_client_kwargs(token=token))

    def unfavorite_article(self, token, slug):
        return self.client.delete(url_for('api.ArticlesView:favorite', slug=slug), **make_client_kwargs(token=token))

    def post_comment(self, token, slug, comment):
        return self.client.post(url_for('api.ArticlesView:post_comment', slug=slug), **make_client_kwargs(token=token, json=comment))

    def delete_comment(self, token, slug, comment_id):
        return self.client.delete(url_for('api.ArticlesView:delete_comment', slug=slug, comment_id=comment_id), **make_client_kwargs(token=token))

    def get_comments(self, slug, token=None):
        return self.client.get(url_for('api.ArticlesView:get_comment', slug=slug), **make_client_kwargs(token=token))

class ArticlesTestCase(BaseTestCase, UserUseCase, ArticlesUseCase):

    def test_crud_article(self):
        new_user = generate_user()
        user = self.register(new_user).json

        new_article = generate_article()
        article = self.post_article(user['user']['token'], new_article).json
        assert 'article' in article

        get_article = self.get_article(article['article']['slug']).json
        assert 'article' in get_article
        assert get_article['article']['title'] == article['article']['title']

        new_article = generate_article()
        updated_article = self.update_article(user['user']['token'], article['article']['slug'], new_article).json
        assert 'article' in updated_article
        assert updated_article['article']['title'] == new_article['article']['title']

        result = self.delete_article(user['user']['token'], updated_article['article']['slug'])
        assert result.status_code == 200

    def test_crud_comment(self):
        new_user = generate_user()
        user = self.register(new_user).json

        new_article = generate_article()
        article = self.post_article(user['user']['token'], new_article).json
        assert 'article' in article

        new_comment = generate_comment()
        comment = self.post_comment(user['user']['token'], article['article']['slug'], new_comment).json
        get_comments = self.get_comments(article['article']['slug']).json
        assert len(get_comments['comments']) == 1

        result = self.delete_comment(user['user']['token'], article['article']['slug'], comment['comment']['id'])
        assert result.status_code == 200

        get_comments = self.get_comments(article['article']['slug']).json
        assert len(get_comments['comments']) == 0


