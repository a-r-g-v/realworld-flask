from functools import wraps
from flask import current_app
from flask_jwt_extended.view_decorators import _decode_jwt_from_request
from flask_jwt_extended.exceptions import JWTExtendedException

try:
    from flask import _app_ctx_stack as ctx_stack
except ImportError:
    from flask import _request_ctx_stack as ctx_stack


def depth(x):
    # type: (dict) -> int
    if isinstance(x, dict) and x:
        return 1 + max(depth(i) for i in x.values())
    else:
        return 0


assert depth({}) == 0
assert depth({"a": "a"}) == 1
assert depth({"a": {"a": "b"}}) == 2
assert depth({"a": {"a": "b"}, "b": {"a": {"b": "c"}}}) == 3


# reffred to concept of https://github.com/mattupstate/flask-jwt/issues/106
def jwt_optional(fn):
    @wraps(fn)
    def decorator(*args, **kwargs):
        try:
            jwt_data = _decode_jwt_from_request(request_type='access')
            if jwt_data:
                ctx_stack.top.jwt = jwt_data
        except JWTExtendedException:
            pass
        return fn(*args, **kwargs)

    return decorator
