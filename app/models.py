from sqlalchemy import Column, DateTime, Integer, Text, func, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship, backref
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token, get_jwt_identity
from .exceptions import Unauthorized, Forbidden

db = SQLAlchemy()


class DatetimeMixin(object):
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class Tag(db.Model):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    articles = relationship('ArticleTag', backref='tag')

class ArticleTag(db.Model):
    __tablename__ = 'article_tags'
    article_id = Column(Integer, ForeignKey("articles.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)

class Article(db.Model, DatetimeMixin):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(Text, nullable=False)
    slug = Column(Text, nullable=False)
    title = Column(Text, nullable=False)
    author_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    tags = relationship('ArticleTag', backref='article')


class Follow(db.Model, DatetimeMixin):
    __tablename__ = 'follows'
    followee_user_id = Column(
        Integer, ForeignKey("users.id"), primary_key=True)
    follower_user_id = Column(
        Integer, ForeignKey("users.id"), primary_key=True)


class User(db.Model, DatetimeMixin):
    __tablename__ = 'users'
    __table_args__ = (UniqueConstraint(
        "email", "password", name="unique_username_email"), )
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    image = Column(Text)
    bio = Column(Text)
    follows = relationship(
        "User",
        secondary="follows",
        primaryjoin=Follow.followee_user_id == id,
        secondaryjoin=Follow.follower_user_id == id,
        backref="followers")

    articles = relationship("Article", backref=backref("author", uselist=False))

    @classmethod
    def get_logged_user(cls, raise_exceptipn=True):
        user_id = get_jwt_identity()

        if not user_id:
            if raise_exceptipn:
                raise Unauthorized
            else:
                return None

        user = db.session.query(cls).filter_by(id=user_id).first()
        if not user and raise_exceptipn:
            raise Unauthorized
        return user

    @classmethod
    def check_already_exist_user(cls, email, password):
        if db.session.query(cls).filter_by(
                email=email, password=password).count():
            raise Forbidden

    @classmethod
    def new(cls, args):
        user = args['user']
        cls.check_already_exist_user(user['email'], user['password'])
        user = cls(
            username=user['username'],
            email=user['email'],
            password=user['password'])

        return user

    @classmethod
    def authenticate(cls, email, password):
        user = db.session.query(cls).filter_by(
            email=email, password=password).first()
        if not user:
            raise Unauthorized
        return user

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        return create_access_token(identity=self.id)

    def update(self, args):
        user = args['user']
        self.__dict__.update(user)

    @classmethod
    def find_by_username(cls, username):
        return db.session.query(cls).filter_by(
            username=username).first_or_404()

    def is_following_by(self, follower_user):
        return db.session.query(Follow).filter_by(
            followee_user_id=self.id,
            follower_user_id=follower_user.id).count() != 0

    def follow(self, follow_user):
        follow = Follow(
            followee_user_id=follow_user.id, follower_user_id=self.id)
        db.session.add(follow)

    def unfollow(self, followee_user):
        follow = db.session.query(Follow).filter_by(
            followee_user_id=followee_user.id,
            follower_user_id=self.id).first_or_404()
        db.session.delete(follow)
