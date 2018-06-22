"""Thirdparties API.

This module maps the API endpoints for the Thirdpary data model, implementing
the POST, GET, PUT and DELETE http methods for its CRUD operations,
respectively.

Endpoints
    GET - /thirdparties - return the collection of all users.
    GET - /thirdparties/<id> - return a thirdparty with given id number.
    POST - /thirdparties - register a new thirdparty.
    PUT - /thirdparties/<id> - modify a thirdparty with given id number.
    DELETE - /thirdparties/<id> - remove a thirdparty with id number.

"""
import re
from flask import (
    jsonify, request)

from app.model import db, Thirdparty
from app.controller.api.errors import bad_request, not_found
from app.controller.api import bp


# Create
@bp.route('/thirdparties', methods=['POST'])
def create_thirdparty():
    """Create new thirdparty."""
    data = request.get_json() or {}

    error = check_thirdparty_data(data=data, new=True)
    if error:
        return bad_request(error)

    # Check if unique attributes collide
    if Thirdparty.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')

    thirdparty = Thirdparty()
    thirdparty.from_dict(data)
    db.session.add(thirdparty)
    db.session.commit()
    return jsonify(thirdparty.to_dict()), 201


# Read
@bp.route('/thirdparties', methods=['GET'])
def get_thirdparties():
    """Return a JSON of all existing thirdparties."""
    return jsonify(
        [thirdparty.to_dict() for thirdparty in Thirdparty.query.all()])


# Read
@bp.route('/thirdparties/<int:id>', methods=['GET'])
def get_thirdparty(id: int):
    """Return given thirdparty by id, if exists."""
    thirdparty = Thirdparty.query.filter_by(id=id).first()
    if thirdparty is None:
        return not_found('thirdparty not found')

    return jsonify(thirdparty.to_dict())


# Update
@bp.route('/thirdparties/<int:id>', methods=['PUT'])
def update_thirdparty(id: int):
    """Update given thirdparty, if exists."""
    thirdparty = Thirdparty.query.filter_by(id=id).first()
    if thirdparty is None:
        return not_found('thirdparty not found')

    data = request.get_json() or {}

    error = check_thirdparty_data(data=data)
    if error:
        return bad_request(error)

    # Check for unique key compliance
    if 'email' in data and data['email'] != thirdparty.email and \
            Thirdparty.query.filter_by(email=data['email']).first() is not None:
        return bad_request('please use a different email address')

    thirdparty.from_dict(data)
    db.session.commit()
    return jsonify(thirdparty.to_dict())


# Delete
@bp.route('/thirdparties/<int:id>', methods=['DELETE'])
def delete_thirdparty(id: int):
    """Delete given thirdparty, if exists."""
    thirdparty = Thirdparty.query.filter_by(id=id).first()
    if thirdparty is None:
        return not_found('thirdparty not found')

    db.session.delete(thirdparty)
    db.session.commit()
    return '', 204


def check_thirdparty_data(data: dict, new: bool = False) -> str or None:
    """Verify Thirdparty data for correct keys and types."""
    # Check if data is empty.
    if len(data.keys()) == 0:
        return 'empty request'
    # Check if data contains any unexpected keys.
    all_keys = ['first_name', 'last_name', 'email']
    if any([key not in all_keys for key in data.keys()]):
        return 'invalid attributes'

    # Check if data contains all required keys for new thirdparty.
    required_keys = ['first_name', 'last_name', 'email']
    if new and any([key not in data.keys() for key in required_keys]):
        return 'missing required attributes'

    # Validate each present key.
    if 'first_name' in data:
        # Check for type.
        if type(data['first_name']) is not str:
            return 'first_name must be string'
        # Check for expected regex pattern.
        first_name = re.compile(r'(\w+\.?)( \w+\.?)*')
        if re.fullmatch(first_name, data['first_name']) is None:
            return 'invalid first name'

    if 'last_name' in data:
        # Check for type.
        if type(data['last_name']) is not str:
            return 'last_name must be string'
        # Check for expected regex pattern.
        last_name = re.compile(r'(\w+\.?)( \w+\.?)*')
        if re.fullmatch(last_name, data['last_name']) is None:
            return 'invalid last name'

    if 'email' in data:
        # Check for type.
        if type(data['email']) is not str:
            return 'email address must be string'
        # Check for expected regex pattern.
        email = re.compile(
                    r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')
        if re.fullmatch(email, data['email']) is None:
            return 'invalid email address'

    return None
