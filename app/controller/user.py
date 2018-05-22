import functools
from flask import (
    Blueprint, request, abort, jsonify
)
from app.model import db, User
from app.controller.auth import login_required, is_admin

bp = Blueprint('users', __name__, url_prefix='/user')


@bp.route('', methods=["POST"])
@login_required
def create():
    """Create a new user."""
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user:
        response = {
            'message': 'User already exists.'
        }
        return jsonify(response), 202
    try:
        user = User()
        for key in data.keys():
            exec(f"user.{key} = data['{key}']")
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_dict()), 201
    except Exception as e:
        abort(400)


@bp.route('', methods=["GET"])
@login_required
def read_all():
    """Return a JSON of all existing users."""
    return jsonify([user.to_dict() for user in User.query.all()])


@bp.route('/<int:id>', methods=["GET"])
@login_required
def read(id):
    """Return user with given id."""
    user = User.query.filter_by(id=id).first()
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@bp.route('/<int:id>', methods=["PUT"])
@login_required
def update(id):
    """Update an user's entry."""
    user = User.query.filter_by(id=id).first()
    if not user:
        abort(404)
    data = request.get_json()
    for key in data.keys():
        if key not in user.to_dict().keys():
            abort(400)
        exec(f"user.{key} = data['{key}']")
    db.session.commit()
    return jsonify(user.to_dict())


@bp.route('/<int:id>', methods=["DELETE"])
@login_required
def delete(id):
    """Delete an user."""
    user = User.query.filter_by(id=id).first()
    if not user:
        abort(404)
    db.session.delete(user)
    db.session.commit()
    return '', 204
