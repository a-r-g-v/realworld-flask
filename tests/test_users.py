from . import BaseTestCase, make_auth_header
from flask import url_for

class UsersTestCase(BaseTestCase):

    def register(self, json):
        return self.client.post(url_for('api.UsersView:post'), json=json)

    def login(self, json):
        return self.client.post(url_for('api.UsersView:login'), json=json)

    def get_my_profile(self, token):
        headers = make_auth_header(token)
        return self.client.get(url_for('api.UserView:index'), headers=headers)

    def update_my_profile(self, token, json):
        headers = make_auth_header(token)
        return self.client.put(url_for('api.UserView:put'), json=json, headers=headers)

