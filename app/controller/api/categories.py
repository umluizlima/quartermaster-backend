"""Categories API.

This module maps the API endpoints for the Category data model, implementing
the POST, GET, PUT and DELETE http methods for its CRUD operations,
respectively.

Endpoints
    GET - /categories - return the collection of all categories.
    GET - /categories/<id> - return a category with given id number.
    POST - /categories - register a new category.
    PUT - /categories/<id> - modify a category with given id number.
    DELETE - /categories/<id> - remove a category with id number.

"""
import re
from flask import (
    jsonify, request)

from app.model import db, Category
from app.controller.api.errors import bad_request, not_found
from app.controller.api import bp


# Create
@bp.route('/categories', methods=['POST'])
def create_category():
    """Create new category."""
    data = request.get_json() or {}

    error = check_category_data(data=data, new=True)
    if error:
        return bad_request(error)

    # Check if unique attributes collide.
    if Category.query.filter_by(name=data['name']).first():
        return bad_request('please use a different name')

    # Create new instance and commit to database.
    category = Category()
    category.from_dict(data)
    db.session.add(category)
    db.session.commit()
    return jsonify(category.to_dict()), 201


# Read
@bp.route('/categories', methods=['GET'])
def get_categories():
    """Return list of categories."""
    return jsonify(
        [category.to_dict() for category in Category.query.all()])


# Read
@bp.route('/categories/<int:id>', methods=['GET'])
def get_category(id: int):
    """Return category with given id."""
    category = Category.query.filter_by(id=id).first()
    if category is None:
        return not_found('category not found')
    return jsonify(category.to_dict())


@bp.route('/categories/<int:id>', methods=['PUT'])
def update_category(id: int):
    """Update given category, if exists."""
    category = Category.query.filter_by(id=id).first()
    if category is None:
        return not_found('category not found')

    data = request.get_json() or {}

    error = check_category_data(data=data)
    if error:
        return bad_request(error)

    # Check for unique key compliance
    if 'name' in data and data['name'] != category.name and \
            Category.query.filter_by(name=data['name']).first() is not None:
        return bad_request('please use a different name')

    category.from_dict(data)
    db.session.commit()
    return jsonify(category.to_dict())


# Delete
@bp.route('/categories/<int:id>', methods=['DELETE'])
def delete_category(id: int):
    """Delete given category, if exists."""
    category = Category.query.filter_by(id=id).first()
    if category is None:
        return not_found('category not found')

    db.session.delete(category)
    db.session.commit()
    return '', 204


def check_category_data(data: dict, new: bool = False) -> str or None:
    """Verify Category data for correct keys and types."""
    # Check if data is empty.
    if len(data.keys()) == 0:
        return 'empty request'
    # Check if data contains any unexpected keys.
    all_keys = ['name', 'description']
    if any([key not in all_keys for key in data.keys()]):
        return 'invalid attributes'

    # Check if data contains all required keys for new category.
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

    return None
