import functools
from flask import (
    Blueprint, request, abort, jsonify
)
from app.model import db, Item, Category
from app.controller.error import bad_request
from app.controller.auth import login_required, is_admin

bp = Blueprint('items', __name__, url_prefix='/items')


@bp.route('', methods=["POST"])
@login_required
def create():
    """Create a new item."""
    data = request.get_json() or {}
    # Check if no required key is missing from data
    keys = ['name']
    if not all([key in data.keys() for key in keys]):
        return bad_request('must include name field')
    # Check if unique attributes collide
    if 'number' in data and \
            Item.query.filter_by(number=data['number']).first():
        return bad_request('please use a different number')
    # Check if foreignkey exists
    if 'category_id' in data and \
            not Category.query.filter_by(id=data['category_id']).first():
        return bad_request('category does not exist')
    # Create new instance and commit to database
    item = Item()
    item.from_dict(data)
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201


@bp.route('', methods=["GET"])
@login_required
def read_all():
    """Return a JSON of all existing items."""
    return jsonify([item.to_dict() for item in Item.query.all()])


@bp.route('/<int:id>', methods=["GET"])
@login_required
def read(id):
    """Return item with given id."""
    return jsonify(Item.query.get_or_404(id).to_dict())


@bp.route('/<int:id>', methods=["PUT"])
@login_required
def update(id):
    """Update an item's entry."""
    item = Item.query.get_or_404(id)
    data = request.get_json() or {}
    # Check if unique attributes collide
    if 'number' in data and data['number'] != item.number and \
            Item.query.filter_by(number=data['number']).first():
        return bad_request('please use a different number')
    item.from_dict(data)
    db.session.commit()
    return jsonify(item.to_dict())


@bp.route('/<int:id>', methods=["DELETE"])
@login_required
def delete(id):
    """Delete an item."""
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return '', 204
