from passlib.handlers.pbkdf2 import pbkdf2_sha256
from sqlalchemy import create_engine, Column, Integer, String, MetaData, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

connection_string = "mssql+pyodbc://DESKTOP-AK9CJ3C/dbcompany2024?driver=ODBC+Driver+17+for+SQL+Server"
DATABASE_URL = "mssql+pyodbc://localhost/dbcompany2024"
engine = create_engine(connection_string, echo=True)

Base = declarative_base()


class UserCustom(Base):
    __tablename__ = 'userssql'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True)  # Adjust the length as needed
    password_hash = Column(String)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255), unique=True)
    def set_password(self, password):
        # Hash the password using passlib's pbkdf2_sha256
        self.password_hash = pbkdf2_sha256.hash(password)

    def check_password(self, password):
        # Verify the password using passlib's pbkdf2_sha256
        return pbkdf2_sha256.verify(password, self.password_hash)

Base.metadata.create_all(bind=engine)
