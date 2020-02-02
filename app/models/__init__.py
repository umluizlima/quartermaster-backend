from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()

from app.models.user import User
from app.models.thirdparty import Thirdparty
from app.models.category import Category
from app.models.item import Item
from app.models.lending import Lending
from app.models.reservation import Reservation
