from flask import request, jsonify
from functools import wraps
from authorization.models import User


def token_check(function_to_decorate):
    @wraps(function_to_decorate)
    def decorator(*args, **kwargs):
        token = None
        if request.cookies.get('token'):
            token = request.cookies.get('token')
        get_user = User.query.filter(User.token == token).one()
        if get_user.is_active == 0:
            return {'error': 'User not found'}, 401
        if not token:
            return jsonify({'error': 'You are not authorized!'}), 401
        return function_to_decorate(token, *args, **kwargs)
    return decorator
