import click
from flask.cli import with_appcontext
from app.models import (
    db, User
)

@click.command('create_admin')
@with_appcontext
def create_admin():
    user = User()
    user.from_dict({
        'first_name': 'Admin',
        'last_name': 'Admin',
        'email': 'admin@admin.com',
        'admin': True
    }, new_user=True)
    try:
        db.session.add(user)
        db.session.commit()
        click.echo("Admin cadastrado com sucesso!")
    except Exception:
        click.echo("Falha ao cadastrar Admin.")
