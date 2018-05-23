import functools
from flask import (
    Blueprint, request, abort, jsonify
)
from app.model import db, Thirdparty
from app.controller.error import bad_request
from app.controller.auth import login_required, is_admin

bp = Blueprint('thirdparties', __name__, url_prefix='/thirdparties')


@bp.route('', methods=["POST"])
@login_required
def create():
    """Create a new thirdparty."""
    data = request.get_json() or {}
    # Check if no required key is missing from data
    keys = ['first_name', 'last_name', 'email']
    if not all([key in data.keys() for key in keys]):
        return bad_request('must include first_name, last_name \
and email fields.')
    # Check if unique attributes collide
    if Thirdparty.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    # Create new instance and commit to database
    thirdparty = Thirdparty()
    thirdparty.from_dict(data)
    db.session.add(thirdparty)
    db.session.commit()
    return jsonify(thirdparty.to_dict()), 201


@bp.route('', methods=["GET"])
@login_required
def read_all():
    """Return a JSON of all existing thirdparties."""
    return jsonify([thirdparty.to_dict() for
                    thirdparty in Thirdparty.query.all()])


@bp.route('/<int:id>', methods=["GET"])
@login_required
def read(id):
    """Return thirdparty with given id."""
    return jsonify(Thirdparty.query.get_or_404(id).to_dict())


@bp.route('/<int:id>', methods=["PUT"])
@login_required
def update(id):
    """Update an thirdparty's entry."""
    thirdparty = Thirdparty.query.get_or_404(id)
    data = request.get_json() or {}
    # Check if unique attributes collide
    if 'email' in data and data['email'] != thirdparty.email and \
            Thirdparty.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    thirdparty.from_dict(data)
    db.session.commit()
    return jsonify(thirdparty.to_dict())


@bp.route('/<int:id>', methods=["DELETE"])
@is_admin
def delete(id):
    """Delete a thirdparty."""
    thirdparty = Thirdparty.query.get_or_404(id)
    db.session.delete(thirdparty)
    db.session.commit()
    return '', 204
