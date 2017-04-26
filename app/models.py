from sqlalchemy import Column, DateTime, Integer, Text, func, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship, backref
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token, get_jwt_identity
from .exceptions import Unauthorized, Forbidden

db = SQLAlchemy()


class DatetimeMixin(object):
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Profile(db.Model, DatetimeMixin):
    __tablename__ = 'profiles'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True, autoincrement=False)
    image = Column(Text)
    bio = Column(Text)

    def update(self, arg):
        user = args['user']
        self.__dict__.update(user)

    @classmethod
    def new(cls, user):
        return cls(user_id=user.id)

class Follow(db.Model, DatetimeMixin):
    __tablename__ = 'follows'
    followee_user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    follower_user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)


class User(db.Model, DatetimeMixin):
    __tablename__ = 'users'
    __table_args__ = (UniqueConstraint(
        "email", "password", name="unique_username_email"), )
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    follows = relationship("User", secondary="follows", primaryjoin=Follow.followee_user_id==id,
            secondaryjoin=Follow.follower_user_id==id, backref="followers")
    profile = relationship("Profile", uselist=False, backref=backref("user", uselist=False))

    @classmethod
    def get_logged_user(cls):
        user_id = get_jwt_identity()
        user = db.session.query(cls).filter_by(id=user_id).first()
        if not user:
            raise Unauthorized
        return user

    @classmethod
    def check_already_exist_user(cls, email, password):
        if db.session.query(cls).filter_by(email=email, password=password).count():
            raise Forbidden

    @classmethod
    def new(cls, args):
        user = args['user']
        cls.check_already_exist_user(user['email'], user['password'])
        user = cls(
            username=user['username'],
            email=user['email'],
            password=user['password'])

        profile = Profile.new(user)
        db.session.add(profile)
        return user

    @classmethod
    def authenticate(cls, email, password):
        user = db.session.query(cls).filter_by(email=email, password=password).first()
        if not user:
            raise Unauthorized
        return user

    @property
    def token(self):
        return self._generate_jwt_token()

    @property
    def bio(self):
        return self.profile.bio

    @property
    def image(self):
        return self.profile.image

    def _generate_jwt_token(self):
        return create_access_token(identity=self.id)

    def update(self, args):
        user = args['user']
        self.__dict__.update(user)
        self.profile.update(user)

    def to_dict(self):
        return {
            "user": {
                "email": self.email,
                "token": self.token,
                "username": self.username,
                "bio": self.bio,
                "image": self.image
            }
        }


    def follow_user(self, user_id):
        pass

    def unfollow_user(self, user_id):
        pass
