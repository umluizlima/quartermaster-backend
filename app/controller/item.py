import functools
from flask import (
    Blueprint, request, abort, jsonify, render_template, redirect, url_for,
    flash
)
from app.model import db, Item, Category
from app.controller.auth import login_required, is_admin

bp = Blueprint('items', __name__, url_prefix='/items')


@bp.route('/new', methods=["GET", "POST"])
@login_required
def create():
    """Create a new item."""
    if request.method == "POST":
        data = request.form
        print(data)
        message = None
        # Check if no required key is missing from data
        keys = ['name']
        if not all([key in data.keys() for key in keys]):
            message = 'Deve conter nome'
        # Check if unique attributes collide
        if 'registry' in data and \
                Item.query.filter_by(registry=data['registry']).first():
            message = 'Tombo já existe'
        # Check if foreignkey exists
        if 'category' in data and data['category'] != '' and \
                not Category.query.filter_by(name=data['category']).first():
            message = 'Categoria não existe'

        if message is None:
            # Create new instance and commit to database
            item = Item()
            item.from_dict(data)
            db.session.add(item)
            db.session.commit()
            return redirect(url_for('items.read_all'))
        flash(message)
    return render_template('item/create.html', categories=Category.query.all())


@bp.route('', methods=["GET"])
@login_required
def read_all():
    """Return all existing items."""
    return render_template('item/list.html', rows=Item.query.all())


# @bp.route('/<int:id>', methods=["GET"])
# @login_required
# def read(id):
#     """Return item with given id."""
#     return jsonify(Item.query.get_or_404(id).to_dict())


@bp.route('/edit/<int:id>', methods=["GET", "POST"])
@login_required
def update(id):
    """Update an item's entry."""
    item = Item.query.get_or_404(id)
    if request.method == "POST":
        data = request.form
        message = None
        # Check if unique attributes collide
        if 'registry' in data and data['registry'] != item.registry and \
                Item.query.filter_by(registry=data['registry']).first():
            message = 'Tombo já existe'

        # Check if foreignkey exists
        if 'category' in data and data['category'] != '' and \
                not Category.query.filter_by(name=data['category']).first():
            message = 'Categoria não existe'

        if message is None:
            item.from_dict(data)
            db.session.commit()
            return redirect(url_for('items.read_all'))
        flash(message)
    return render_template('item/edit.html',
                           item=item,
                           categories=Category.query.all())


@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    """Delete an item."""
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('items.read_all'))
