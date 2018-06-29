"""
Data model for users.

Every user has a firstname, lastname, email and password.
A user might be admin.
"""

import os
import re
import jwt
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from app.model import db


class User(db.Model):
    """Data model for users."""

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    token = db.Column(db.Text, unique=True)
    token_exp = db.Column(db.DateTime)
    reservations = db.relationship('Reservation',
                                   backref='user',
                                   lazy=True)
    lendings = db.relationship('Lending',
                               backref='user',
                               lazy=True)

    def set_password(self, password):
        """Set user password."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check if user password matches given password."""
        return check_password_hash(self.password, password)
    #
    # def get_token(self, expires_in=3600):
    #     """Get user's token, or generates a new one."""
    #     now = datetime.utcnow()
    #     # Return current token if still valid
    #     if self.token and self.token_exp > now + timedelta(seconds=60):
    #         return self.token
    #     # Generate a new token
    #     payload = {
    #         'user_id': self.id
    #     }
    #     self.token = jwt.encode(payload,
    #                             os.environ.get('SECRET_KEY') or 'secret')
    #     self.token_exp = now + timedelta(seconds=expires_in)
    #     db.session.add(self)
    #     return self.token.decode('UTF-8')
    #
    # def revoke_token(self):
    #     """Instantly revokes user's current token."""
    #     self.token_exp = datetime.utcnow() - timedelta(seconds=1)
    #
    # @staticmethod
    # def check_token(token):
    #     """Return user whom token belongs to."""
    #     print(token)
    #     try:
    #         payload = jwt.decode(token,
    #                              os.environ.get('SECRET_KEY') or 'secret')
    #     except:
    #         return None
    #     print(payload)
    #     user = User.query.filter_by(id=payload['user_id']).first()
    #     print(user)
    #     print(user.to_dict())
    #     print(user.password)
    #     print(user.token_exp)
    #     if user is None or user.token_exp < datetime.utcnow():
    #         return None
    #     return user
    #
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

    @staticmethod
    def check_data(data: dict, new: bool = False):
        """Verify User data for correct keys and types."""
        # Check if data is empty.
        if len(data.keys()) == 0:
            return 'empty request'
        # Check if data contains any unexpected keys.
        all_keys = ['first_name', 'last_name', 'email', 'password',
                    'confirm', 'admin']
        if any([key not in all_keys for key in data.keys()]):
            return 'invalid attributes'

        # Check if data contains all required keys for new lending.
        required_keys = ['first_name', 'last_name', 'email',
                         'password', 'confirm']
        if new and any([key not in data.keys() for key in required_keys]):
            return 'missing required attributes'

        # Validate each present key.
        if 'first_name' in data:
            # Check for type.
            if type(data['first_name']) is not str:
                return 'first name must be string'
            # Check for expected regex pattern.
            first_name = re.compile(r'[a-zA-Z]+( [a-zA-Z]+)*')
            if re.fullmatch(first_name, data['first_name']) is None:
                return 'invalid first name'

        if 'last_name' in data:
            # Check for type.
            if type(data['last_name']) is not str:
                return 'last name must be string'
            # Check for expected regex pattern.
            last_name = re.compile(r'[a-zA-Z]+( [a-zA-Z]+)*')
            if re.fullmatch(last_name, data['last_name']) is None:
                return 'invalid last name'

        if 'email' in data:
            # Check for type.
            if type(data['email']) is not str:
                return 'email address must be string'
            # Check for expected regex pattern.
            email = re.compile(
                        r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')
            if re.fullmatch(email, data['email']) is None:
                return 'invalid email address'

            if new and User.query.filter_by(email=data['email']).first():
                return 'please use a different email address'

        if new:
            if 'password' in data:
                # Check for type.
                if type(data['password']) is not str:
                    return 'password must be string'
            if 'confirm' in data:
                # Check for type.
                if type(data['confirm']) is not str:
                    return 'confirm must be string'
            if data['password'] != data['confirm']:
                return 'password and confirm must match'

        if 'admin' in data:
            # Check for type.
            if type(data['admin']) is not bool:
                return 'admin must be bool'

        return None
