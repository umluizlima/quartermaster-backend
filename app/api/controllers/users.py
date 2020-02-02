from flask import (
    jsonify, request
)
from app.models import (
    db, User
)
from app.api.errors import (
    bad_request, internal_server, not_found
)
from app.api import api
from app.api.controllers.auth import (
    admin_required, token_required
)


@api.route('/users', methods=['POST'])
@admin_required
def create_user():
    data = request.get_json() or {}

    error = User.check_data(data=data, new=True)
    if 'email' in data and \
            User.query.filter_by(email=data['email']).first() is not None:
        error = 'email já existe'
    if error:
        return bad_request(error)

    user = User()
    user.from_dict(data, new_user=True)

    try:
        db.session.add(user)
        db.session.commit()
    except Exception:
        return internal_server()

    return jsonify(user.to_dict()), 201


@api.route('/users', methods=['GET'])
@token_required
def get_users():
    return jsonify(
        [user.to_dict() for user in User.query.all()]
    )


@api.route('/users/<int:id>', methods=['GET'])
@token_required
def get_user(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        return not_found('usuário não encontrado')
    return jsonify(user.to_dict())


@api.route('/users/<int:id>', methods=['PUT'])
@admin_required
def update_user(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        return not_found('usuário não encontrado')
    data = request.get_json() or {}

    error = User.check_data(data)
    if 'email' in data and data['email'] != user.email and \
            User.query.filter_by(email=data['email']).first() is not None:
        error = 'email já existe'
    if error:
        return bad_request(error)

    user.from_dict(data)
    try:
        db.session.commit()
    except Exception:
        return internal_server()

    return jsonify(user.to_dict())


@api.route('/users/<int:id>', methods=['DELETE'])
@admin_required
def delete_user(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        return not_found('usuário não encontrado')

    try:
        db.session.delete(user)
        db.session.commit()
    except Exception:
        return internal_server()

    return '', 204
