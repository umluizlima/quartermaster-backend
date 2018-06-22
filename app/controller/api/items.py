"""Items API.

This module maps the API endpoints for the Item data model, implementing
the POST, GET, PUT and DELETE http methods for its CRUD operations,
respectively.

Endpoints
    GET - /items - return the collection of all items.
    GET - /items/<id> - return an item with given id number.
    POST - /items - register a new item.
    PUT - /items/<id> - modify an item with given id number.
    DELETE - /items/<id> - remove an item with id number.

"""
import re
from flask import (
    jsonify, request)

from app.model import db, Item, Category
from app.controller.api.errors import bad_request, not_found
from app.controller.api import bp


# Create
@bp.route('/items', methods=['POST'])
def create_item():
    """Create new item."""
    data = request.get_json() or {}

    error = check_item_data(data=data, new=True)
    if error:
        return bad_request(error)

    # Check if unique attributes collide.
    if 'registry' in data and data['registry'] is not None and \
            Item.query.filter_by(registry=data['registry']).first():
        return bad_request('please use a different registry')

    # Create new instance and commit to database.
    item = Item()
    item.from_dict(data)
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201


# Read
@bp.route('/items', methods=['GET'])
def get_items():
    """Return list of items."""
    return jsonify([item.to_dict() for item in Item.query.all()])


# Read
@bp.route('/items/<int:id>', methods=['GET'])
def get_item(id: int):
    """Return item with given id."""
    item = Item.query.filter_by(id=id).first()
    if item is None:
        return not_found('item not found')
    return jsonify(item.to_dict())


# Update
@bp.route('/items/<int:id>', methods=['PUT'])
def update_item(id):
    """Update given item, if exists."""
    item = Item.query.filter_by(id=id).first()
    if item is None:
        return not_found('item not found')

    data = request.get_json() or {}

    error = check_item_data(data=data)
    if error:
        return bad_request(error)

    # Check for unique key compliance
    if 'registry' in data and data['registry'] is not None \
            and data['registry'] != item.registry and \
            Item.query.filter_by(registry=data['registry']).first() is not None:
        return bad_request('please use a different registry')

    item.from_dict(data)
    db.session.commit()
    return jsonify(item.to_dict())


# Delete
@bp.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id: int):
    """Delete given item, if exists."""
    item = Item.query.filter_by(id=id).first()
    if item is None:
        return not_found('item not found')

    db.session.delete(item)
    db.session.commit()
    return '', 204


def check_item_data(data: dict, new: bool = False) -> str or None:
    """Verify Item data for correct keys and types."""
    # Check if data is empty.
    if len(data.keys()) == 0:
        return 'empty request'
    # Check if data contains any unexpected keys.
    all_keys = ['name', 'description', 'registry', 'available', 'category_id']
    if any([key not in all_keys for key in data.keys()]):
        return 'invalid attributes'

    # Check if data contains all required keys for new item.
    required_keys = ['name']
    if new and any([key not in data.keys() for key in required_keys]):
        return 'missing required attributes'

    # Validate each present key.
    if 'name' in data:
        # Check for type.
        if type(data['name']) is not str:
            return 'name must be string'
        # Check for expected regex pattern.
        name = re.compile(r'\w+( \w+)*')
        if re.fullmatch(name, data['name']) is None:
            return 'invalid name'

    if 'description' in data:
        # Check for type.
        if type(data['description']) is not str and \
                data['description'] is not None:
            return 'description must be string or null'
        # Check for expected regex pattern.
        # description = re.compile(r'')
        # if re.fullmatch(description, data['description']) is None:
        #     return 'invalid description'

    if 'available' in data:
        # Check for type.
        if type(data['available']) is not bool:
            return 'available must be bool'

    if 'category_id' in data:
        # Check for type.
        if type(data['category_id']) is not int and \
                data['category_id'] is not None:
            return 'category id must be int or null'
        # Check for existance.
        if type(data['category_id']) is int and \
                Category.query.get(data['category_id']) is None:
            return 'invalid category_id'

    if 'registry' in data:
        # Check for type.
        if type(data['registry']) is not str and \
                data['registry'] is not None:
            return 'registry must be string or null'

    return None
