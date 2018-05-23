from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
migrate = Migrate()


class User(db.Model):
    """Data model for users."""

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def set_password(self, password):
        """Set user password."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check if user password matches given password."""
        return check_password_hash(self.password, password)

    def to_dict(self):
        """Return a User object formatted as dict."""
        obj = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "admin": self.admin
        }
        return obj

    def from_dict(self, data, new_user=False):
        """Fill User attributes from given dictionary."""
        for field in ['first_name', 'last_name', 'email', 'admin']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])


class Thirdparty(db.Model):
    """Data model for thirdparties."""

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def to_dict(self):
        """Return a Thirdparty object formatted as dict."""
        obj = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }
        return obj

    def from_dict(self, data):
        """Fill Thirdparty attributes from given dictionary."""
        for field in ['first_name', 'last_name', 'email']:
            if field in data:
                setattr(self, field, data[field])


class Category(db.Model):
    """Data model for categories."""

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text)

    def to_dict(self):
        """Return a Category object formatted as dict."""
        obj = {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }
        return obj

    def from_dict(self, data):
        """Fill Category attributes from given dictionary."""
        for field in ['name', 'description']:
            if field in data:
                setattr(self, field, data[field])

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(120), nullable=False)
#     last_name = db.Column(db.String(120), nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(128), nullable=False)
#     admin = db.Column(db.Boolean, nullable=False, default=False)
#     lendings = db.relationship('Lending', backref='user', lazy=True)
#     reservations = db.relationship('Reservation', backref='user', lazy=True)
#
#
# class Item(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     number = db.Column(db.Integer, unique=True, nullable=True)
#     name = db.Column(db.String(120), nullable=False)
#     description = db.Column(db.Text)
#     category_id = db.Column(db.Integer,
#                             db.ForeignKey('category.id'),
#                             nullable=True)
#     lendings = db.relationship('Lending', backref='item', lazy=True)
#
#
# class Thirdparty(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(120), nullable=False)
#     last_name = db.Column(db.String(120), nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     reservations = db.relationship('Reservation', backref='thirdparty', lazy=True)
#     lendings = db.relationship('Lending', backref='thirdparty', lazy=True)
#
#
# class Reservation(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(120), nullable=False)
#     date_start = db.Column(db.DateTime, nullable=False)
#     date_end = db.Column(db.DateTime, nullable=False)
#     user_id = db.Column(db.Integer,
#                         db.ForeignKey('user.id'),
#                         nullable=True)
#     thirdparty_id = db.Column(db.Integer,
#                               db.ForeignKey('thirdparty.id'),
#                               nullable=True)
#
#
# class Lending(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     date_start = db.Column(db.DateTime, nullable=False)
#     date_end = db.Column(db.DateTime, nullable=False)
#     date_return = db.Column(db.DateTime, nullable=True)
#     item_id = db.Column(db.Integer,
#                         db.ForeignKey('item.id'),
#                         nullable=False)
#     user_id = db.Column(db.Integer,
#                         db.ForeignKey('user.id'),
#                         nullable=True)
#     thirdparty_id = db.Column(db.Integer,
#                               db.ForeignKey('thirdparty.id'),
#                               nullable=True)
