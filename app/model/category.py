"""
Data model for categories.

Every category has a name and description.
"""

from app.model import db


class Category(db.Model):
    """Data model for categories."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text)
    items = db.relationship('Item', backref='category', lazy=True)

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
