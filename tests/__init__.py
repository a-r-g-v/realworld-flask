import unittest
import os
import json as _json
from datetime import timedelta 
from conduit import create_app
from conduit.models import db
from faker import Faker

class TestConfig(object):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS =False
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SECRET_KEY = "change_me"
    JWT_ALGORITHM = "HS256"
    JWT_HEADER_TYPE = "Token"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=60)
    SERVER_NAME="localhost"

class JSONResponseMixin(object):
    """
        referred to flask-testing
    """
    @property
    def json(self):
        if self.content_type in ['application/json', 'text/javascript']:
            return _json.loads(self.data)

def make_response_class(response_class):
    class ResponseClass(response_class, JSONResponseMixin):
        pass
    return ResponseClass

def make_auth_header(token):
    return {"Authorization": "{type} {token}".format(type=TestConfig.JWT_HEADER_TYPE, token=token)}

def make_client_kwargs(token=None, json=None, query_string=None):
    result = {}
    if json:
        result.update({'data': _json.dumps(json), 'content_type': 'application/json'})
    if token:
        result.update({'headers': make_auth_header(token)})
    if query_string:
        result.update({'query_string': query_string})

    return result

def generate_user():
    fake = Faker()
    profile = fake.simple_profile()
    return {
            'user': {
                'username': profile['username'], 
                'email': profile['mail'],
                'password': profile['username']
                }
            }

def generate_article():
    fake = Faker()
    return {
            'article': {
                'title': fake.sentence(nb_words=4),
                'description': fake.sentence(nb_words=12),
                'body': fake.paragraph(nb_sentences=6),
                'tagList': fake.words(nb=4)
                }
            }

def generate_comment():
    fake = Faker()
    return {
            'comment': {
                'body': fake.paragraph(nb_sentences=6)
                }
            }


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_object='tests.TestConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.response_class = make_response_class(self.app.response_class)
        self.client = self.app.test_client()
        db.create_all(app=self.app)

    def tearDown(self):
        db.drop_all(app=self.app)
        self.app_context.pop()

