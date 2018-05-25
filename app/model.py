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
        for field in ['first_name', 'last_name', 'email']:
            if field in data:
                setattr(self, field, data[field])
        if 'admin' in data and bool(data['admin']) is True:
            setattr(self, 'admin', True)
        else:
            setattr(self, 'admin', False)
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


class Item(db.Model):
    """Data model for items."""

    id = db.Column(db.Integer, primary_key=True)
    registry = db.Column(db.String(32), unique=True, nullable=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(80),
                         db.ForeignKey('category.name'),
                         nullable=True)

    def to_dict(self):
        """Return a Item object formatted as dict."""
        obj = {
            "id": self.id,
            "registry": self.registry,
            "name": self.name,
            "description": self.description,
            "category": self.category
        }
        return obj

    def from_dict(self, data):
        """Fill Item attributes from given dictionary."""
        for field in ['registry', 'name', 'description', 'category']:
            if field in data:
                setattr(self, field, data[field])
            if 'category' in data and data['category'] != '':
                setattr(self, 'category', data['category'])
            else:
                setattr(self, 'category', None)


# class Lending(db.Model):
#     """Data model for lendings."""
#
#     id = db.Column(db.Integer, primary_key=True)
#     date_start = db.Column(db.DateTime, nullable=False,
#                            default=datetime.utcnow)
#     date_end = db.Column(db.DateTime, nullable=False)
#     date_return = db.Column(db.DateTime, nullable=True)
#     item_id = db.Column(db.Integer,
#                         db.ForeignKey('item.id'),
#                         nullable=False)
#     user_id = db.Column(db.Integer,
#                         db.ForeignKey('user.id'),
#                         nullable=True,
#                         default=g.get('user_id'))
#     thirdparty_id = db.Column(db.Integer,
#                               db.ForeignKey('thirdparty.id'),
#                               nullable=True)
#
#     def to_dict(self):
#         """Return a Item object formatted as dict."""
#         obj = {
#             "id": self.id,
#             "date_start": self.date_start.isoformat() + 'Z',
#             "date_end": self.date_end.isoformat() + 'Z',
#             "date_return": self.date_return.isoformat() + 'Z',
#             "item_id": self.item_id,
#             "user_id": self.user_id,
#             "thirdparty_id": self.thirdparty_id
#         }
#         return obj
#
#     def from_dict(self, data):
#         """Fill Item attributes from given dictionary."""
#         for field in ['date_start', 'date_end', 'item_id',
#                       'user_id', 'thirdparty_id']:
#             if field in data:
#                 setattr(self, field, data[field])
#
#
# class Reservation(db.Model):
#     """Data model for reservations."""
#
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
#     def to_dict(self):
#         """Return a Reservation object formatted as dict."""
#         obj = {
#             "id": self.id,
#             "name": self.name,
#             "date_start": self.date_start,
#             "date_end": self.date_end,
#             "user_id": self.user_id,
#             "thirdparty_id": self.thirdparty_id
#         }
#         return obj
#
#     def from_dict(self, data):
#         """Fill Reservation attributes from given dictionary."""
#         for field in ['name', 'date_start', 'date_end',
#                       'user_id', 'thirdparty_id']:
#             if field in data:
#                 setattr(self, field, data[field])
