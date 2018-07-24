"""Items API.

This module maps the API endpoints for the Item data model, implementing
the POST, GET, PUT and DELETE http methods for its CRUD operations,
respectively.

Endpoints
---------
    GET - /items - return the collection of all items.
    GET - /items/<id> - return an item with given id number.
    POST - /items - register a new item.
    PUT - /items/<id> - modify an item with given id number.
    DELETE - /items/<id> - remove an item with id number.

"""
from flask import (
    jsonify, request
)
from app.model import (
    db, Item, Category
)
from app.controller.errors import (
    bad_request, internal_server, not_found
)
from app.controller.api import api


# Create
@api.route('/items', methods=['POST'])
def create_item():
    """Create new item."""
    data = request.get_json() or {}

    error = Item.check_data(data=data, new=True)
    if 'registry' in data and data['registry'] is not None and \
            Item.query.filter_by(registry=data['registry']).first():
        error = 'tombo já existe'
    if 'category_id' in data and data['category_id'] is not None and \
            Category.query.get(data['category_id']) is None:
        error = 'category_id não existe'
    if error:
        return bad_request(error)

    item = Item()
    item.from_dict(data)

    try:
        db.session.add(item)
        db.session.commit()
    except Exception:
        return internal_server()

    return jsonify(item.to_dict()), 201


# Read
@api.route('/items', methods=['GET'])
def get_items():
    """Return list of items."""
    return jsonify(
        [item.to_dict() for item in Item.query.all()]
    )


# Read
@api.route('/items/<int:id>', methods=['GET'])
def get_item(id: int):
    """Return item with given id."""
    item = Item.query.filter_by(id=id).first()
    if item is None:
        return not_found('item não encontrado')
    return jsonify(item.to_dict())


# Update
@api.route('/items/<int:id>', methods=['PUT'])
def update_item(id: int):
    """Update given item, if exists."""
    item = Item.query.filter_by(id=id).first()
    if item is None:
        return not_found('item não encontrado')

    data = request.get_json() or {}

    error = Item.check_data(data=data)
    if 'registry' in data and data['registry'] is not None \
            and data['registry'] != item.registry and \
            Item.query.filter_by(registry=data['registry']).first() is not None:
        error = 'tombo já existe'
    if 'category_id' in data and data['category_id'] is not None and \
            Category.query.get(data['category_id']) is None:
        error = 'category_id não existe'
    if error:
        return bad_request(error)

    item.from_dict(data)
    try:
        db.session.commit()
    except Exception:
        return internal_server()

    return jsonify(item.to_dict())


# Delete
@api.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id: int):
    """Delete given item, if exists."""
    item = Item.query.filter_by(id=id).first()
    if item is None:
        return not_found('item não encontrado')

    try:
        db.session.delete(item)
        db.session.commit()
    except Exception:
        return internal_server()

    return '', 204
