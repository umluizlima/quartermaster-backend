from flask import (
    jsonify, request
)
from app.models import (
    db, Lending, User, Thirdparty, Item
)
from app.api.errors import (
    bad_request, internal_server, not_found
)
from app.api import api
from app.api.controllers.auth import token_required


@api.route('/lendings', methods=['POST'])
@token_required
def create_lending():
    data = request.get_json() or {}

    error = Lending.check_data(data=data, new=True)
    if 'user_id' in data and data['user_id'] is not None and \
            User.query.get(data['user_id']) is None:
        error = 'usuário não existe'
    if 'thirdparty_id' in data and data['thirdparty_id'] is not None and \
            Thirdparty.query.get(data['thirdparty_id']) is None:
        error = 'terceiro não existe'
    if 'item_id' in data and data['item_id'] is not None:
        item = Item.query.get(data['item_id'])
        if item is None:
            error = 'item não existe'
        if not item.available:
            error = 'item não está disponível'
    if error:
        return bad_request(error)

    lending = Lending()
    lending.from_dict(data)

    try:
        db.session.add(lending)
        db.session.commit()
    except Exception:
        return internal_server()

    return jsonify(lending.to_dict()), 201


@api.route('/lendings', methods=['GET'])
@token_required
def get_open_lendings():
    return jsonify(
        [lending.to_dict() for lending
            in Lending.query.filter(Lending.date_return == None)]
    )


@api.route('/lendings/all', methods=['GET'])
@token_required
def get_all_lendings():
    return jsonify(
        [lending.to_dict() for lending in Lending.query.all()]
    )


@api.route('/lendings/<int:id>', methods=['GET'])
@token_required
def get_lending(id: int):
    lending = Lending.query.filter_by(id=id).first()
    if lending is None:
        return not_found('empréstimo não encontrado')
    return jsonify(lending.to_dict())


@api.route('/lendings/<int:id>', methods=['PUT'])
@token_required
def update_lending(id: int):
    lending = Lending.query.filter_by(id=id).first()
    if lending is None:
        return not_found('empréstimo não encontrado')

    data = request.get_json() or {}

    error = Lending.check_data(data=data)
    if 'user_id' in data and data['user_id'] is not None and \
            User.query.get(data['user_id']) is None:
        error = 'usuário não existe'
    if 'thirdparty_id' in data and data['thirdparty_id'] is not None and \
            Thirdparty.query.get(data['thirdparty_id']) is None:
        error = 'terceiro não existe'
    if 'item_id' in data and data['item_id'] != lending.item_id and \
            data['item_id'] is not None:
        item = Item.query.get(data['item_id'])
        if item is None:
            error = 'item não existe'
        if not item.available:
            error = 'item não está disponível'
        else:
            item.available = False
    if error:
        return bad_request(error)

    lending.from_dict(data)
    try:
        db.session.commit()
    except Exception:
        return internal_server()

    return jsonify(lending.to_dict())


@api.route('/lendings/<int:id>', methods=['DELETE'])
@token_required
def delete_lending(id: int):
    lending = Lending.query.filter_by(id=id).first()
    if lending is None:
        return not_found('empréstimo não encontrado')

    try:
        db.session.delete(lending)
        db.session.commit()
    except Exception:
        return internal_server()

    return '', 204
