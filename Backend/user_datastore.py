from flask_security import SQLAlchemyUserDatastore
from database import db
from models import User, Role

user_datastore = SQLAlchemyUserDatastore(db, User, Role)