import functools
from flask import (
    Blueprint, request, abort, jsonify, render_template, redirect,
    url_for, flash
)
from app.model import db, Thirdparty
from app.controller.auth import login_required, is_admin

bp = Blueprint('thirdparties', __name__, url_prefix='/thirdparties')


@bp.route('/new', methods=["GET", "POST"])
@login_required
def create():
    """Create a new thirdparty."""
    if request.method == "POST":
        data = request.form
        message = None
        # Check if no required key is missing from data
        keys = ['first_name', 'last_name', 'email']
        if not all([key in data.keys() for key in keys]):
            message = 'Deve conter nome, sobrenome e email'
        # Check if unique attributes collide
        if Thirdparty.query.filter_by(email=data['email']).first():
            message = 'Email já existe'

        if message is None:
            # Create new instance and commit to database
            thirdparty = Thirdparty()
            thirdparty.from_dict(data)
            db.session.add(thirdparty)
            db.session.commit()
            return redirect(url_for('thirdparties.read_all'))
        flash(message)
    return render_template('thirdparty/create.html')


@bp.route('', methods=["GET"])
@login_required
def read_all():
    """Return all existing thirdparties."""
    return render_template('thirdparty/list.html', rows=Thirdparty.query.all())


# @bp.route('/<int:id>', methods=["GET"])
# @login_required
# def read(id):
#     """Return thirdparty with given id."""
#     return jsonify(Thirdparty.query.get_or_404(id).to_dict())


@bp.route('/edit/<int:id>', methods=["GET", "POST"])
@login_required
def update(id):
    """Update an thirdparty's entry."""
    thirdparty = Thirdparty.query.get_or_404(id)
    if request.method == "POST":
        data = request.form
        message = None
        # Check if unique attributes collide
        if 'email' in data and data['email'] != thirdparty.email and \
                Thirdparty.query.filter_by(email=data['email']).first():
            message = 'Email já existe'

        if message is None:
            thirdparty.from_dict(data)
            db.session.commit()
            return redirect(url_for('thirdparties.read_all'))
        flash(message)
    return render_template('thirdparty/edit.html', thirdparty=thirdparty)


@bp.route('/delete/<int:id>')
@is_admin
def delete(id):
    """Delete a thirdparty."""
    thirdparty = Thirdparty.query.get_or_404(id)
    db.session.delete(thirdparty)
    db.session.commit()
    return redirect(url_for('thirdparties.read_all'))
