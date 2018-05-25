import functools
from flask import (
    Blueprint, request, abort, jsonify, render_template, redirect, url_for,
    flash
)
from app.model import db, User
from app.controller.auth import login_required, is_admin

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('/new', methods=["GET", "POST"])
@is_admin
def create():
    """Create a new user."""
    if request.method == "POST":
        data = request.form
        message = None
        # Check if no required key is missing from data
        keys = ['first_name', 'last_name', 'email', 'password']
        if not all([key in data.keys() for key in keys]):
            message = 'Deve conter nome, sobrenome, email e senha'
        # Check if unique attributes collide
        if User.query.filter_by(email=data['email']).first():
            message = 'Email já existe'

        if message is None:
            # Create new instance and commit to database
            user = User()
            user.from_dict(data, new_user=True)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('users.read_all'))
        flash(message)
    return render_template('user/create.html')


@bp.route('', methods=["GET"])
@is_admin
def read_all():
    """Return all existing users."""
    return render_template('user/list.html', rows=User.query.all())


# @bp.route('/<int:id>', methods=["GET"])
# @login_required
# def read(id):
#     """Return user with given id."""
#     return jsonify(User.query.get_or_404(id).to_dict())


@bp.route('/edit/<int:id>', methods=["GET", "POST"])
@is_admin
def update(id):
    """Update an user's entry."""
    user = User.query.get_or_404(id)
    if request.method == "POST":
        data = request.form
        message = None
        # Check if unique attributes collide
        if 'email' in data and data['email'] != user.email and \
                User.query.filter_by(email=data['email']).first():
            message = 'Email já existe'

        if message is None:
            user.from_dict(data, new_user=False)
            db.session.commit()
            return redirect(url_for('users.read_all'))
        flash(message)
    return render_template('user/edit.html', user=user)


@bp.route('/delete/<int:id>')
@is_admin
def delete(id):
    """Delete an user."""
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users.read_all'))
