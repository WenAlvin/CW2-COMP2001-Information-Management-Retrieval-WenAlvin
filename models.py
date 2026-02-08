from datetime import datetime
import pytz
from marshmallow import Schema, fields as ma_fields, validate, ValidationError
from config import db, ma

class User(db.Model):
    __tablename__ = 'Users'
    UserID = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(255), unique=True, nullable=False)
    UserName = db.Column(db.String(100), nullable=False)
    Role = db.Column(db.String(50), nullable=False)

class Trail(db.Model):
    __tablename__ = 'Trails'
    TrailID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255), nullable=False)
    Description = db.Column(db.Text)
    OwnerID = db.Column(db.Integer, db.ForeignKey('Users.UserID'), nullable=False)
    CreatedDate = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Europe/London')), 
                            onupdate=lambda: datetime.now(pytz.timezone('Europe/London')))

class Location(db.Model):
    __tablename__ = 'Locations'
    LocationID = db.Column(db.Integer, primary_key=True)
    TrailID = db.Column(db.Integer, db.ForeignKey('Trails.TrailID'), nullable=False)
    Latitude = db.Column(db.Float, nullable=False)
    Longitude = db.Column(db.Float, nullable=False)
    SequenceOrder = db.Column(db.Integer, nullable=False)

class LocationSchema(Schema):
    latitude = ma_fields.Float(required=True)
    longitude = ma_fields.Float(required=True)
    sequence_order = ma_fields.Integer(required=True, validate=validate.Range(min=1))

class TrailSchema(Schema):
    name = ma_fields.String(required=True, validate=validate.Length(min=1, max=255))
    description = ma_fields.String()
    locations = ma_fields.List(ma_fields.Nested(LocationSchema))

trail_schema = TrailSchema()
trails_schema = TrailSchema(many=True)