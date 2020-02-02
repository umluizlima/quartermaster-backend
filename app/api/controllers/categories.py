from flask import (
    jsonify, request
)
from app.models import (
    db, Category
)
from app.api.errors import (
    bad_request, internal_server, not_found
)
from app.api import api
from app.api.controllers.auth import token_required


@api.route('/categories', methods=['POST'])
@token_required
def create_category():
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


@api.route('/categories', methods=['GET'])
@token_required
def get_categories():
    return jsonify(
        [category.to_dict() for category in Category.query.all()]
    )


@api.route('/categories/<int:id>', methods=['GET'])
@token_required
def get_category(id: int):
    category = Category.query.filter_by(id=id).first()
    if category is None:
        return not_found('categoria não encontrada')
    return jsonify(category.to_dict())


@api.route('/categories/<int:id>', methods=['PUT'])
@token_required
def update_category(id: int):
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


@api.route('/categories/<int:id>', methods=['DELETE'])
@token_required
def delete_category(id: int):
    category = Category.query.filter_by(id=id).first()
    if category is None:
        return not_found('categoria não encontrada')

    try:
        db.session.delete(category)
        db.session.commit()
    except Exception:
        return internal_server()

    return '', 204
