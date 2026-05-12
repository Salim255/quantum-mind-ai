
# ---------------------------------------------------------
# SQLAlchemy Base class
# ---------------------------------------------------------
# declarative_base() is the foundation for all SQLAlchemy ORM models.
# Every model in your project will inherit from this Base class.
#
# Example:
#   class User(Base):
#       __tablename__ = "users"
#       id = Column(Integer, primary_key=True)
#
from sqlalchemy.orm import declarative_base

# Create the Base class used by all models
Base = declarative_base()

# ---------------------------------------------------------
# Import all models so SQLAlchemy knows they exist
# ---------------------------------------------------------
# Why do we import models here?
#
# Because SQLAlchemy needs to be aware of ALL model classes
# before calling Base.metadata.create_all(engine).
#
# If you forget to import a model here:
#   → SQLAlchemy will NOT create its table
#   → No errors, but the table will not exist
#
# This file acts as the "registry" of all your models.
#
# IMPORTANT:
# - Do NOT remove these imports
# - Do NOT use them directly in this file
# - They only need to be imported so SQLAlchemy can register them
#
from app.models.user import User
# from app.models.game import Game
# from app.models.gps import GpsPoint
# Add more models here as your project grows