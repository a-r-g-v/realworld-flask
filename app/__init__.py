from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from app.errors import Errors

migrate = Migrate()
jwt = JWTManager()
errors = Errors()


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    from .models import db

    db.init_app(app)
    migrate.init_app(app, db)

    jwt.init_app(app)

    from .views import api as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # register error handlers
    errors.init_app(app)

    return app
