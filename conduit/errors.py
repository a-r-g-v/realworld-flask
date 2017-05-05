from flask import jsonify
from webargs.flaskparser import parser
from .exceptions import UnprocessableEntity, NotFound, Unauthorized, Forbidden
from .utils import depth


@parser.error_handler
def handle_request_parsing_error(error):
    if depth(error.message) <= 1:
        raise UnprocessableEntity(error.message)

    errors = {}
    for _, v in error.message.items():
        errors.update(v)

    raise UnprocessableEntity(errors)


class Errors(object):
    def __init__(self, app=None):
        if app:
            self._register_error_handlers(app)

    def init_app(self, app):
        self._register_error_handlers(app)

    def _register_error_handlers(self, app):
        @app.errorhandler(422)
        @app.errorhandler(UnprocessableEntity)
        def unprocessable_entity(error):
            # pylint: disable=unused-variable
            return jsonify({"errors": error.message}), 422

        @app.errorhandler(404)
        @app.errorhandler(NotFound)
        def not_found(_):
            # pylint: disable=unused-variable
            return jsonify({"errors": ["NotFound"]}), 404

        @app.errorhandler(401)
        @app.errorhandler(Unauthorized)
        def unauthorized(_):
            # pylint: disable=unused-variable
            return jsonify({"errors": ["Unauthorized"]}), 401

        @app.errorhandler(403)
        @app.errorhandler(Forbidden)
        def forbidden(_):
            # pylint: disable=unused-variable
            return jsonify({"errors": ["Forbidden"]}), 403

        @app.errorhandler(500)
        def server_errror(_):
            # pylint: disable=unused-variable
            return jsonify({"errors": ["Internal Server Error"]}), 500
