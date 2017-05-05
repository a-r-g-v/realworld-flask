from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from .errors import Errors

migrate = Migrate()
jwt = JWTManager()
errors = Errors()
ma = Marshmallow()


def create_app(config_filename=None, config_object=None):
    app = Flask(__name__)

    if config_filename:
        app.config.from_pyfile(config_filename)

    if config_object:
        app.config.from_object(config_object)

    from .models import db

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    jwt.init_app(app)

    from .views import api as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # register error handlers
    errors.init_app(app)

    return app
