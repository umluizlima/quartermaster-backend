import functools
from flask import (
    Blueprint, request, abort, jsonify
)
from app.model import db, Category
from app.controller.error import bad_request
from app.controller.auth import login_required, is_admin

bp = Blueprint('categories', __name__, url_prefix='/categories')


@bp.route('', methods=["POST"])
@login_required
def create():
    """Create a new category."""
    data = request.get_json() or {}
    # Check if no required key is missing from data
    keys = ['name']
    if not all([key in data.keys() for key in keys]):
        return bad_request('must include name field')
    # Check if unique attributes collide
    if Category.query.filter_by(name=data['name']).first():
        return bad_request('please use a different name')
    # Create new instance and commit to database
    category = Category()
    category.from_dict(data)
    db.session.add(category)
    db.session.commit()
    return jsonify(category.to_dict()), 201


@bp.route('', methods=["GET"])
@login_required
def read_all():
    """Return a JSON of all existing categories."""
    return jsonify([category.to_dict() for category in Category.query.all()])


@bp.route('/<int:id>', methods=["GET"])
@login_required
def read(id):
    """Return category with given id."""
    return jsonify(Category.query.get_or_404(id).to_dict())


@bp.route('/<int:id>', methods=["PUT"])
@login_required
def update(id):
    """Update an category's entry."""
    category = Category.query.get_or_404(id)
    data = request.get_json() or {}
    # Check if unique attributes collide
    if 'name' in data and data['name'] != category.name and \
            Category.query.filter_by(name=data['name']).first():
        return bad_request('please use a different name')
    category.from_dict(data)
    db.session.commit()
    return jsonify(category.to_dict())


@bp.route('/<int:id>', methods=["DELETE"])
@login_required
def delete(id):
    """Delete an category."""
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return '', 204
