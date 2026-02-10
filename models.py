from datetime import datetime
from marshmallow_sqlalchemy import fields
import pytz
from config import db, ma

class User(db.Model):
    __tablename__ = 'Users'
    __table_args__ = {'schema': 'CW2'}
    UserID = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(255), unique=True, nullable=False)
    UserName = db.Column(db.String(100), nullable=False)
    Role = db.Column(db.String(50), nullable=False)

class Location(db.Model):
    __tablename__ = 'Locations'
    __table_args__ = {'schema': 'CW2'}
    LocationID = db.Column(db.Integer, primary_key=True)
    TrailID = db.Column(db.Integer, db.ForeignKey('CW2.Trails.TrailID'), nullable=False)
    Latitude = db.Column(db.Float, nullable=False)
    Longitude = db.Column(db.Float, nullable=False)
    SequenceOrder = db.Column(db.Integer, nullable=False)

class LocationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Location
        load_instance = True
        sql_session = db.session
        include_fk = True

class Trail(db.Model):
    __tablename__ = 'Trails'
    __table_args__ = {'schema': 'CW2'}
    TrailID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255), nullable=False)
    Description = db.Column(db.Text)
    ElevationGain = db.Column(db.Integer)
    Length = db.Column(db.Float)
    RouteType = db.Column(db.String(50))
    EstimatedTime = db.Column(db.Integer)
    Features = db.Column(db.String(255))
    OwnerID = db.Column(db.Integer, db.ForeignKey('CW2.Users.UserID'), nullable=False)
    CreatedDate = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Europe/London')), 
                         onupdate=lambda: datetime.now(pytz.timezone('Europe/London')))
    locations = db.relationship('Location', backref='trail', cascade='all, delete-orphan', single_parent=True, order_by='Location.SequenceOrder')


class TrailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trail
        load_instance = True
        sql_session = db.session
        include_fk = True
        include_relationships = True
    locations = fields.Nested(LocationSchema, many=True)
    

trail_schema = TrailSchema()
trails_schema = TrailSchema(many=True)
location_schema = LocationSchema()

