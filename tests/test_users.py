from . import BaseTestCase, make_client_kwargs, generate_user
from flask import url_for


class UserUseCase(object):
    def register(self, json):
        return self.client.post(
            url_for('api.UsersView:post'), **make_client_kwargs(json=json))

    def login(self, json):
        return self.client.post(
            url_for('api.UsersView:login'), **make_client_kwargs(json=json))

    def get_my_user(self, token):
        return self.client.get(
            url_for('api.UserView:index'), **make_client_kwargs(token=token))

    def update_my_user(self, token, json):
        return self.client.put(
            url_for('api.UserView:put'), **make_client_kwargs(
                token=token, json=json))


class UsersTestCase(BaseTestCase, UserUseCase):
    def test_register(self):
        new_user = generate_user()
        assert 'user' in self.register(new_user).json

    def test_login(self):
        new_user = generate_user()
        assert 'user' in self.register(new_user).json

        logged_user = self.login(new_user).json
        assert 'user' in logged_user
        assert logged_user['user']['username'] == new_user['user']['username']

    def test_get_my_user(self):
        new_user = generate_user()
        registerd_user = self.register(new_user).json
        token = registerd_user['user']['token']
        user = self.get_my_user(token).json
        assert 'user' in user
        assert user['user']['username'] == new_user['user']['username']

    def test_update_my_user(self):
        new_user = generate_user()
        registerd_user = self.register(new_user).json
        token = registerd_user['user']['token']

        update_user = generate_user()
        updated_user = self.update_my_user(token, update_user).json
        assert 'user' in updated_user
        assert updated_user['user']['username'] == update_user['user'][
            'username']
