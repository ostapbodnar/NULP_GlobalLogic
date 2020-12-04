from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Boolean


engine = create_engine("postgresql://postgres:1914@localhost:5432/test")
BaseModel = declarative_base()
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)


class User(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    user_name = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)
    phone = Column(String)
    place_id = Column(Integer, ForeignKey('places.id'))

    place = relationship("Place")


class Advertisment(BaseModel):
    __tablename__ = "advertisements"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    quantity = Column(Integer)
    createdate = Column(String)
    updatedate = Column(String)
    status = Column(Boolean)
    tag = Column(Boolean)
    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship("User")


class Place(BaseModel):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True)
    name = Column(String)
