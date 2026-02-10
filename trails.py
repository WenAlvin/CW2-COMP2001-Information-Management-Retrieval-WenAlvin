from flask import make_response, abort

from config import db
from datetime import datetime
from models import Trail, User, Location, trail_schema, trails_schema, LocationSchema

def read_all():
    trails = Trail.query.all()
    return trails_schema.dump(trails)
def create(trail):
    name=trail.get("name")
    existing_trail = Trail.query.filter(Trail.Name == name).one_or_none()
    if existing_trail is None:
        new_trail = trail_schema.load(trail, session=db.session)
        db.session.add(new_trail)
        db.session.commit()
        return trail_schema.dump(new_trail), 201
    else:
        abort(406, f"Trail with name {name} already exists")
def read_one(name):
    trail = Trail.query.filter(Trail.Name == name).one_or_none()
    if trail is not None:
        return trail_schema.dump(trail)
    else:
        abort(404, f"Trail with name {name} not found")
def update(trail_Name, trail):
    existing_trail = Trail.query.filter(Trail.Name == trail_Name).one_or_none()
    if existing_trail:
        update_trail = trail_schema.load(trail, session=db.session)
        existing_trail.Description = update_trail.Description
        existing_trail.Difficulty = update_trail.Difficulty
        existing_trail.Length = update_trail.Length
        existing_trail.RouteType = update_trail.RouteType
        existing_trail.EstimatedTime = update_trail.EstimatedTime
        existing_trail.Features = update_trail.Features
        db.session.merge(existing_trail)
        db.session.commit()
        return trail_schema.dump(existing_trail), 201
    else:
        abort(404, f"Trail with name {trail_Name} not found")
def delete(name):
    existing_trail = Trail.query.filter(Trail.Name == name).one_or_none()
    if existing_trail:
        db.session.delete(existing_trail)
        db.session.commit()
        return make_response(f"Trail with name {name} successfully deleted", 200)
    else:      
        abort(404, f"Trail with name {name} not found")