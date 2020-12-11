import sqlalchemy
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from marshmallow import Schema, fields, post_load
from marshmallow_enum import EnumField
import enum
import datetime

BaseModel = declarative_base()


class IntEnum(sqlalchemy.types.TypeDecorator):
    impl = sqlalchemy.Integer

    def __init__(self, enumtype, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._enumtype = enumtype

    def process_bind_param(self, value, dialect):
        return value.value

    def process_result_value(self, value, dialect):
        return self._enumtype(value)


class Tag(enum.Enum):
    Local = 1
    Global = 2


class Status(enum.Enum):
    avaliable = 1
    sold = 2


class User(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    user_name = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)
    phone = Column(String)
    place_id = Column(Integer, ForeignKey('places.id'))

    place = relationship("Place")


class Advertisement(BaseModel):
    __tablename__ = "advertisements"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    quantity = Column(Integer)
    createdate = Column(DateTime,
                        default=datetime.datetime.utcnow)
    updatedate = Column(DateTime,
                        onupdate=datetime.datetime.utcnow)
    status = Column(Enum(Status))
    tag = Column(Enum(Tag))
    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship("User")


class Place(BaseModel):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)


class PlaceSchema(Schema):

    id = fields.Int()
    name = fields.Str()

    @post_load
    def make_place(self, data, **kwargs):
        return Place(**data)


class UserSchema(Schema):
    id = fields.Int()

    user_name = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()
    email = fields.Str()
    password = fields.Str()
    phone = fields.Str()
    place_id = Column(Integer, ForeignKey('places.id'))

    place = fields.Nested(PlaceSchema)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)


class AdvertisementSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    quantity = fields.Int()
    createdate = fields.DateTime(allow_none=True)
    updatedate = fields.DateTime(allow_none=True)
    status = EnumField(Status, load_by=EnumField.VALUE,
                       dump_by=EnumField.VALUE)
    tag = EnumField(Tag,  load_by=EnumField.VALUE, dump_by=EnumField.VALUE)

    owner = fields.Nested(UserSchema)

    @post_load
    def make_advertisement(self, data, **kwargs):
        return Advertisement(**data)
