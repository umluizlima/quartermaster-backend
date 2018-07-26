"""Categories API.

This module maps the API endpoints for the Category data model, implementing
the POST, GET, PUT and DELETE http methods for its CRUD operations,
respectively.

Endpoints
---------
    GET - /categories - return the collection of all categories.
    GET - /categories/<id> - return a category with given id number.
    POST - /categories - register a new category.
    PUT - /categories/<id> - modify a category with given id number.
    DELETE - /categories/<id> - remove a category with id number.

"""
from flask import (
    jsonify, request
)
from app.model import (
    db, Category
)
from app.controller.errors import (
    bad_request, internal_server, not_found
)
from app.controller.api import api
from app.controller.api.auth import token_required


# Create
@api.route('/categories', methods=['POST'])
def create_category():
    """Create new category."""
    data = request.get_json() or {}

    error = Category.check_data(data=data, new=True)
    if 'name' in data \
            and Category.query.filter_by(name=data['name']).first() is not None:
        error = 'nome já existe'
    if error:
        return bad_request(error)

    category = Category()
    category.from_dict(data)

    try:
        db.session.add(category)
        db.session.commit()
    except Exception:
        return internal_server()

    return jsonify(category.to_dict()), 201


# Read
@api.route('/categories', methods=['GET'])
@token_required
def get_categories():
    """Return list of categories."""
    return jsonify(
        [category.to_dict() for category in Category.query.all()]
    )


# Read
@api.route('/categories/<int:id>', methods=['GET'])
def get_category(id: int):
    """Return category with given id."""
    category = Category.query.filter_by(id=id).first()
    if category is None:
        return not_found('categoria não encontrada')
    return jsonify(category.to_dict())


# Update
@api.route('/categories/<int:id>', methods=['PUT'])
def update_category(id: int):
    """Update given category, if exists."""
    category = Category.query.filter_by(id=id).first()
    if category is None:
        return not_found('categoria não encontrada')

    data = request.get_json() or {}

    error = Category.check_data(data=data)
    if 'name' in data and data['name'] != category.name and \
            Category.query.filter_by(name=data['name']).first() is not None:
        error = 'nome já existe'
    if error:
        return bad_request(error)

    category.from_dict(data)
    try:
        db.session.commit()
    except Exception:
        return internal_server()

    return jsonify(category.to_dict())


# Delete
@api.route('/categories/<int:id>', methods=['DELETE'])
def delete_category(id: int):
    """Delete given category, if exists."""
    category = Category.query.filter_by(id=id).first()
    if category is None:
        return not_found('categoria não encontrada')

    try:
        db.session.delete(category)
        db.session.commit()
    except Exception:
        return internal_server()

    return '', 204
