from flask import make_response, abort, request, jsonify

from config import db
from models import Trail, Location, LocationSchema

def create(body):
    new_location = LocationSchema().load(body, session=db.session)
    db.session.add(new_location)
    db.session.commit()
    print(f"Data received: {body}")
    return LocationSchema().dump(new_location), 201 
def read_one(location_id):
    location = Location.query.get(location_id)
    if location is not None:
        return LocationSchema().dump(location)
    else:
        abort(404, f"Location with ID {location_id} not found")

def update(location_id, body):
    existing_location = Location.query.get(location_id)
    if existing_location:
        update_location = LocationSchema().load(body, session=db.session)
        existing_location.TrailID = update_location.TrailID
        existing_location.Latitude = update_location.Latitude
        existing_location.Longitude = update_location.Longitude
        existing_location.SequenceOrder = update_location.SequenceOrder
        db.session.merge(existing_location)
        db.session.commit()
        return LocationSchema().dump(existing_location), 201
    else:
        abort(404, f"Location with ID {location_id} not found")

def delete(location_id):
    existing_location = Location.query.get(location_id)
    if existing_location:
        db.session.delete(existing_location)
        db.session.commit()
        return make_response(jsonify(message=f"Location with ID {location_id} deleted successfully"), 200)
    else:
        abort(404, message=f"Location with ID {location_id} not found")