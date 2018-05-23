import functools
from flask import (
    Blueprint, request, abort, jsonify
)
from app.model import db, User
from app.controller.error import bad_request
from app.controller.auth import login_required, is_admin

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('', methods=["POST"])
@login_required
def create():
    """Create a new user."""
    data = request.get_json() or {}
    # Check if no required key is missing from data
    keys = ['first_name', 'last_name', 'email', 'password']
    if not all([key in data.keys() for key in keys]):
        return bad_request('must include first_name, last_name, \
email and password fields')
    # Check if unique attributes collide
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    # Create new instance and commit to database
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@bp.route('', methods=["GET"])
@login_required
def read_all():
    """Return a JSON of all existing users."""
    return jsonify([user.to_dict() for user in User.query.all()])


@bp.route('/<int:id>', methods=["GET"])
@login_required
def read(id):
    """Return user with given id."""
    return jsonify(User.query.get_or_404(id).to_dict())


@bp.route('/<int:id>', methods=["PUT"])
@login_required
def update(id):
    """Update an user's entry."""
    user = User.query.get_or_404(id)
    data = request.get_json() or {}
    # Check if unique attributes collide
    if 'email' in data and data['email'] != user.email and \
            User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())


@bp.route('/<int:id>', methods=["DELETE"])
@is_admin
def delete(id):
    """Delete an user."""
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return '', 204
