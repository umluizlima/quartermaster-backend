from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()

from app.model.user import User
from app.model.thirdparty import Thirdparty
from app.model.category import Category
from app.model.item import Item
from app.model.lending import Lending
from app.model.reservation import Reservation
