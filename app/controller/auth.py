import functools, os

from flask import (
    Blueprint, g, request, session, jsonify, render_template, redirect,
    url_for, abort, flash
)

from app.model import User

bp = Blueprint('auth', __name__, url_prefix='')


@bp.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""
    if request.method == "POST":
        data = request.form
        message = None

        user = User.query.filter_by(email=data['email']).first()
        if user is None:
            message = 'Email inválido'
        elif not user.check_password(data['password']):
            message = 'Senha incorreta'

        if message is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('main.index'))
        flash(message)
    return render_template('auth/login.html', title="Login")


@bp.route('/logout', methods=["GET"])
def logout():
    """Clear logged user from session."""
    session.clear()
    return redirect(url_for('main.index'))


def login_required(view):
    """Protect content from non-logged users."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            message = 'Você precisa entrar para acessar este recurso'
            flash(message)
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


def is_admin(view):
    """Protect content from non-admin users."""
    @functools.wraps(view)
    @login_required
    def wrapped_view(**kwargs):
        if not g.user.admin:
            message = 'Você precisa ser administrador para acessar este recurso'
            flash(message)
            return redirect(url_for('main.index'))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """Load logged user into context."""
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()
