# auth_backends.py
from django.contrib.auth.backends import ModelBackend
from sqlalchemy import create_engine

from .sqlalchemy_models import UserCustom
from sqlalchemy.orm import sessionmaker
from django.db import connection, connections


class SQLAlchemyBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Connect to the database
        custom_alias = 'custom_alias'  # Use the alias you defined in settings.py
        connection_string = "mssql+pyodbc://DESKTOP-AK9CJ3C/dbcompany2024?driver=ODBC+Driver+17+for+SQL+Server"

        # Create the SQLAlchemy engine
        sqlalchemy_engine = create_engine(connection_string)

        # Use the engine to create a session
        Session = sessionmaker(bind=sqlalchemy_engine)
        session = Session()

        # Query the user by username
        user = session.query(UserCustom).filter_by(username=username).first()

        if user and user.check_password(password):
            return user  # Return the user to authenticate

