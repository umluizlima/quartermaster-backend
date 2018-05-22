import functools

from flask import (
    Blueprint, g, request, session, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.model import User

bp = Blueprint('auth', __name__, url_prefix='')


@bp.route('/login', methods=["POST"])
def login():
    """Handle user login."""
    data = request.get_json()
    message = None

    user = User.query.filter_by(email=data['email']).first()
    if user is None:
        message = 'Wrong email.'
    # elif not check_password_hash(user.password, data['password']):
    elif user.password != data['password']:
        message = 'Wrong password.'

    if message is None:
        session.clear()
        session['user_id'] = user.id
        return '', 204

    response = {
        'message': message
    }
    return jsonify(response), 401


@bp.route('/logout', methods=["GET"])
def logout():
    """Clear logged user from session."""
    session.clear()
    return '', 204


def login_required(view):
    """Protect content from non-logged users."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            response = {
                'message': 'You must be logged in to access this resource.'
            }
            return jsonify(response), 401

        return view(**kwargs)

    return wrapped_view


def is_admin(view):
    """Protect content from non-admin users."""
    @functools.wraps(view)
    @login_required
    def wrapped_view(**kwargs):
        if not g.user.admin:
            response = {
                'message': 'You must be admin to access this resource.'
            }
            return jsonify(response), 401

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """Load logged user into context."""
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()
