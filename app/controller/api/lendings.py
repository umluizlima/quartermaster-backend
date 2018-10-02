"""Lendings API.

This module maps the API endpoints for the Lending data model, implementing
the POST, GET, PUT and DELETE http methods for its CRUD operations,
respectively.

Endpoints
---------
    GET - /lendings - return the collection of all lendings.
    GET - /lendings/<id> - return a lending with given id number.
    POST - /lendings - register a new lending.
    PUT - /lendings/<id> - modify a lending with given id number.
    DELETE - /lendings/<id> - remove a lending with id number.

"""
from flask import (
    jsonify, request
)
from app.model import (
    db, Lending, User, Thirdparty, Item
)
from app.controller.errors import (
    bad_request, internal_server, not_found
)
from app.controller.api import api
from app.controller.api.auth import token_required


# Create
@api.route('/lendings', methods=['POST'])
@token_required
def create_lending():
    """Create new lending."""
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


# Read
@api.route('/lendings', methods=['GET'])
@token_required
def get_open_lendings():
    """Return list of lendings."""
    return jsonify(
        [lending.to_dict() for lending
            in Lending.query.filter(Lending.date_return == None)]
    )


# Read
@api.route('/lendings/all', methods=['GET'])
@token_required
def get_all_lendings():
    """Return list of lendings."""
    return jsonify(
        [lending.to_dict() for lending in Lending.query.all()]
    )


# Read
@api.route('/lendings/<int:id>', methods=['GET'])
@token_required
def get_lending(id: int):
    """Return lending with given id."""
    lending = Lending.query.filter_by(id=id).first()
    if lending is None:
        return not_found('empréstimo não encontrado')
    return jsonify(lending.to_dict())


# Update
@api.route('/lendings/<int:id>', methods=['PUT'])
@token_required
def update_lending(id: int):
    """Update given lending, if exists."""
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


# Delete
@api.route('/lendings/<int:id>', methods=['DELETE'])
@token_required
def delete_lending(id: int):
    """Delete given lending, if exists."""
    lending = Lending.query.filter_by(id=id).first()
    if lending is None:
        return not_found('empréstimo não encontrado')

    try:
        db.session.delete(lending)
        db.session.commit()
    except Exception:
        return internal_server()

    return '', 204
