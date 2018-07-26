import functools
from flask import (
    request, jsonify, g
)
from app.model import User
from app.controller.errors import bad_request, unauthorized
from app.controller.api import api


def token_required(view):
    """Require user authentication."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return unauthorized('token required')

        return view(**kwargs)

    return wrapped_view


@api.route('/login', methods=['POST'])
def login():
    """Validate user's credentials."""
    data = request.get_json() or {}

    if 'email' not in data or 'password' not in data:
        return bad_request('missing fields')

    user = User.query.filter_by(email=data['email']).first()

    if user is None:
        return bad_request('invalid email address')
    elif not user.check_password(data['password']):
        return bad_request('incorrect password')

    response = {
        'message': 'use this token as the Authentication header',
        'token': user.get_token()
    }
    return jsonify(response), 200


@api.route('/logout', methods=['GET'])
@token_required
def logout():
    """Log out from every device."""
    g.user.revoke_token()
    return '', 204


@api.before_app_request
def load_logged_in_user():
    """Get logged user before every request."""
    token = request.headers.get('Authorization')
    print(token)

    if token is None:
        g.user = None
    else:
        g.user = User.check_token(token.split()[-1])
