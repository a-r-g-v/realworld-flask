from . import BaseTestCase, make_client_kwargs, generate_user
from .test_users import UserUseCase
from flask import url_for


class ProfilesUseCase(object):
    def get_profile(self, username, token=None):
        return self.client.get(
            url_for('api.ProfilesView:index', username=username),
            **make_client_kwargs(token=token))

    def follow_user(self, username, token):
        return self.client.post(
            url_for('api.ProfilesView:follow', username=username),
            **make_client_kwargs(token=token))

    def unfollow_user(self, username, token):
        return self.client.delete(
            url_for('api.ProfilesView:follow', username=username),
            **make_client_kwargs(token=token))


class ProfilesTestCase(BaseTestCase, UserUseCase, ProfilesUseCase):
    def test_get_profile(self):
        new_user = generate_user()
        assert 'user' in self.register(new_user).json

        profile = self.get_profile(new_user['user']['username']).json
        assert profile['profile']['username'] == new_user['user']['username']
        assert profile['profile']['following'] is None

    def test_follow_and_unfollow_user(self):
        followee = generate_user()
        followee_user = self.register(followee).json

        follower = generate_user()
        follower_user = self.register(follower).json

        profile = self.follow_user(followee_user['user']['username'],
                                   follower_user['user']['token']).json
        assert profile['profile']['following'] is True

        profile = self.unfollow_user(followee_user['user']['username'],
                                     follower_user['user']['token']).json
        assert profile['profile']['following'] is False
