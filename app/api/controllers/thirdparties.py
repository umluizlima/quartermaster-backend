from flask import (
    jsonify, request
)
from app.models import (
    db, Thirdparty
)
from app.api.errors import (
    bad_request, internal_server, not_found
)
from app.api import api
from app.api.controllers.auth import token_required


@api.route('/thirdparties', methods=['POST'])
def create_thirdparty():
    data = request.get_json() or {}

    error = Thirdparty.check_data(data=data, new=True)
    if 'email' in data and data['email'] is not None and \
            Thirdparty.query.filter_by(email=data['email']).first():
        error = 'email já existe'
    if error:
        return bad_request(error)

    thirdparty = Thirdparty()
    thirdparty.from_dict(data)

    try:
        db.session.add(thirdparty)
        db.session.commit()
    except Exception:
        return internal_server()

    return jsonify(thirdparty.to_dict()), 201


@api.route('/thirdparties', methods=['GET'])
@token_required
def get_thirdparties():
    return jsonify(
        [thirdparty.to_dict() for thirdparty in Thirdparty.query.all()]
    )


@api.route('/thirdparties/<int:id>', methods=['GET'])
@token_required
def get_thirdparty(id: int):
    thirdparty = Thirdparty.query.filter_by(id=id).first()
    if thirdparty is None:
        return not_found('terceiro não encontrado')
    return jsonify(thirdparty.to_dict())


@api.route('/thirdparties/<int:id>', methods=['PUT'])
@token_required
def update_thirdparty(id: int):
    thirdparty = Thirdparty.query.filter_by(id=id).first()
    if thirdparty is None:
        return not_found('terceiro não encontrado')

    data = request.get_json() or {}

    error = Thirdparty.check_data(data=data)
    if 'email' in data and data['email'] != thirdparty.email and \
            Thirdparty.query.filter_by(email=data['email']).first() is not None:
        error = 'email já existe'
    if error:
        return bad_request(error)

    thirdparty.from_dict(data)
    try:
        db.session.commit()
    except Exception:
        return internal_server()

    return jsonify(thirdparty.to_dict())


@api.route('/thirdparties/<int:id>', methods=['DELETE'])
@token_required
def delete_thirdparty(id: int):
    thirdparty = Thirdparty.query.filter_by(id=id).first()
    if thirdparty is None:
        return not_found('terceiro não encontrado')

    try:
        db.session.delete(thirdparty)
        db.session.commit()
    except Exception:
        return internal_server()

    return '', 204
