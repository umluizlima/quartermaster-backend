import functools
from flask import (
    Blueprint, request, abort, jsonify, redirect, url_for, render_template,
    flash
)
from app.model import db, Category
from app.controller.auth import login_required, is_admin

bp = Blueprint('categories', __name__, url_prefix='/categories')


@bp.route('new', methods=["GET", "POST"])
@login_required
def create():
    """Create a new category."""
    if request.method == "POST":
        data = request.form
        message = None
        # Check if no required key is missing from data
        keys = ['name']
        if not all([key in data.keys() for key in keys]):
            message = 'Deve conter nome'
        # Check if unique attributes collide
        if Category.query.filter_by(name=data['name']).first():
            message = 'Nome já existe'

        if message is None:
            # Create new instance and commit to database
            category = Category()
            category.from_dict(data)
            db.session.add(category)
            db.session.commit()
            return redirect(url_for('categories.read_all'))
        flash(message)
    return render_template('category/create.html')


@bp.route('', methods=["GET"])
@login_required
def read_all():
    """Return all existing categories."""
    return render_template('category/list.html', rows=Category.query.all())


# @bp.route('/<int:id>', methods=["GET"])
# @login_required
# def read(id):
#     """Return category with given id."""
#     return jsonify(Category.query.get_or_404(id).to_dict())


@bp.route('/edit/<int:id>', methods=["GET", "POST"])
@login_required
def update(id):
    """Update an category's entry."""
    category = Category.query.get_or_404(id)
    if request.method == "POST":
        data = request.form
        message = None
        # Check if unique attributes collide
        if 'name' in data and data['name'] != category.name and \
                Category.query.filter_by(name=data['name']).first():
            message = 'Nome já existe'

        if message is None:
            category.from_dict(data)
            db.session.commit()
            return redirect(url_for('categories.read_all'))
        flash(message)
    return render_template('category/edit.html', category=category)


@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    """Delete an category."""
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('categories.read_all'))
