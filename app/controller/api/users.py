from flask import (
    jsonify, request
)
from app.model import db, User
from app.controller.api.errors import bad_request, not_found
from app.controller.api import bp


@bp.route('/users', methods=['POST'])
def create_user():
    """Create new user."""
    data = request.get_json() or {}

    error = User.check_data(data=data, new=True)
    if error:
        return bad_request(error)

    # Create new instance and commit to database.
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@bp.route('/users', methods=['GET'])
def get_users():
    """Return a JSON of all existing Users."""
    return jsonify([user.to_dict() for user in User.query.all()])


@bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    """Return given user by id, if exists."""
    user = User.query.filter_by(id=id).first()
    if user is None:
        return not_found('user not found')
    return jsonify(user.to_dict())


@bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    """Update given user, if exists."""
    user = User.query.filter_by(id=id).first()
    if user is None:
        return not_found('user not found')
    data = request.get_json() or {}

    # Check for correct keys and types
    error = User.check_data(data)
    if error:
        return bad_request(error)

    # Check for unique key compliance
    if 'email' in data and data['email'] != user.email and \
            User.query.filter_by(email=data['email']).first() is not None:
        return bad_request('please use a different email address')

    user.from_dict(data)
    db.session.commit()
    return jsonify(user.to_dict())


@bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    """Delete given user, if exists."""
    user = User.query.filter_by(id=id).first()
    if user is None:
        return not_found('user not found')

    db.session.delete(user)
    db.session.commit()
    return '', 204


# def check_data(data):
#     """Verify data for correct keys and types."""
#     # Possible keys
#     keys = ['email', 'first_name', 'last_name', 'password', 'confirm']
#     # True if key in data is not in possible keys
#     key_check = [key not in keys for key in data.keys()]
#     # Check for invalid attributes
#     if any(key_check):
#         return 'invalid attributes'
#     # Check key presence and type correctness
#     if 'email' in data and type(data['email']) is not str:
#         return 'email must be string'
#     if 'first_name' in data and type(data['first_name']) is not str:
#         return 'first_name must be string'
#     if 'last_name' in data and type(data['last_name']) is not str:
#         return 'last_name must be string'
#     if 'password' in data and type(data['password']) is not str:
#         return 'password must be string'
#     if 'confirm' in data and type(data['confirm']) is not str:
#         return 'confirm must be string'
#     return None
