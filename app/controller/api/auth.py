import os
import functools
from flask import (
    request, jsonify, g
)
from app.model import User
from app.controller.errors import (
    bad_request, unauthorized
)
from app.controller.api import api


class Admin:
    admin = True


def token_required(view):
    """Require user authentication."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return unauthorized('token necessário')

        return view(**kwargs)

    return wrapped_view


def admin_required(view):
    """Require user authentication."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return unauthorized('token necessário')
        elif not g.user.admin:
            return unauthorized('admin necessário')

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
        return bad_request('email incorreto')
    elif not user.check_password(data['password']):
        return bad_request('senha incorreta')

    response = {
        'message': 'use este token no cabeçalho Authentication',
        'token': user.get_token(),
        'id': user.id
    }
    return jsonify(response), 200


@api.route('/changepassword', methods=['PUT'])
@token_required
def change_password():
    """Validate user's credentials."""
    data = request.get_json() or {}

    if 'old_password' not in data \
            or 'new_password' not in data \
            or 'new_confirm' not in data:
        return bad_request('missing fields')

    if g.user is None:
        return bad_request('é necessário estar logado')
    elif not g.user.check_password(data['old_password']):
        return bad_request('senha incorreta')
    elif data['new_password'] != data['new_confirm']:
        return bad_request('nova senha e confirmação devem ser iguais')

    g.user.set_password(data['new_password'])

    return '', 204


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

    if token is None:
        g.user = None
    else:
        token = token.split()[-1]
        if token == os.environ.get('SECRET_KEY'):
            g.user = Admin()
        else:
            g.user = User.check_token(token.split()[-1])
