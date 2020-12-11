from flask import Flask
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from flask_bcrypt import Bcrypt


__version__ = '0.1.0'
app = Flask(__name__)
bcrypt = Bcrypt(app)

engine = create_engine("postgresql://postgres:1914@localhost:5432/db")
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)
session = Session()

from . import urls
from . import models