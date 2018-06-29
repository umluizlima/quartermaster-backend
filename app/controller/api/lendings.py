"""Lendings API.

This module maps the API endpoints for the Lending data model, implementing
the POST, GET, PUT and DELETE http methods for its CRUD operations,
respectively.

Endpoints
    GET - /lendings - return the collection of all lendings.
    GET - /lendings/<id> - return a lending with given id number.
    POST - /lendings - register a new lending.
    PUT - /lendings/<id> - modify a lending with given id number.
    DELETE - /lendings/<id> - remove a lending with id number.

"""
import re
from flask import (
    jsonify, request)

from app.model import db, Lending
from app.controller.api.errors import bad_request, not_found
from app.controller.api import bp


# Create
@bp.route('/lendings', methods=['POST'])
def create_lending():
    """Create new lending."""
    data = request.get_json() or {}

    error = check_lending_data(data=data, new=True)
    if error:
        return bad_request(error)

    # Check if unique attributes collide.
    # if 'registry' in data and data['registry'] is not None and \
    #         Lending.query.filter_by(registry=data['registry']).first():
    #     return bad_request('please use a different registry')

    # Create new instance and commit to database.
    lending = Lending()
    lending.from_dict(data)
    db.session.add(lending)
    db.session.commit()
    return jsonify(lending.to_dict()), 201


# Read
@bp.route('/lendings', methods=['GET'])
def get_lendings():
    """Return list of lendings."""
    return jsonify([lending.to_dict() for lending in Lending.query.all()])


# Read
@bp.route('/lendings/<int:id>', methods=['GET'])
def get_lending(id: int):
    """Return lending with given id."""
    lending = Lending.query.filter_by(id=id).first()
    if lending is None:
        return not_found('lending not found')
    return jsonify(lending.to_dict())


# Update
@bp.route('/lendings/<int:id>', methods=['PUT'])
def update_lending(id: int):
    """Update given lending, if exists."""
    lending = Lending.query.filter_by(id=id).first()
    if lending is None:
        return not_found('lending not found')

    data = request.get_json() or {}

    error = check_lending_data(data=data)
    if error:
        return bad_request(error)

    # Check for unique key compliance
    # if 'registry' in data and data['registry'] is not None \
    #         and data['registry'] != lending.registry and \
    #         Lending.query.filter_by(registry=data['registry']).first() is not None:
    #     return bad_request('please use a different registry')

    lending.from_dict(data)
    db.session.commit()
    return jsonify(lending.to_dict())


# Delete
@bp.route('/lendings/<int:id>', methods=['DELETE'])
def delete_lending(id: int):
    """Delete given lending, if exists."""
    lending = Lending.query.filter_by(id=id).first()
    if lending is None:
        return not_found('lending not found')

    db.session.delete(lending)
    db.session.commit()
    return '', 204


def check_lending_data(data: dict, new: bool = False) -> str or None:
    """Verify Lending data for correct keys and types."""
    return None
    # Check if data is empty.
    if len(data.keys()) == 0:
        return 'empty request'
    # Check if data contains any unexpected keys.
    all_keys = ['date_start', 'date_end', 'date_return', 'item_id',
                'user_id', 'thirdparty_id']
    if any([key not in all_keys for key in data.keys()]):
        return 'invalid attributes'

    # Check if data contains all required keys for new lending.
    required_keys = ['date_start', 'date_end', 'item_id',
                     'user_id', 'thirdparty_id']
    if new and any([key not in data.keys() for key in required_keys]):
        return 'missing required attributes'

    # Validate each present key.
    if 'date_start' in data:
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
