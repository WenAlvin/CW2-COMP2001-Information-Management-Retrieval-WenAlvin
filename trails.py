from flask import make_response, abort

from config import db
from models import Trail, User, Location, trail_schema, trails_schema, LocationSchema

def read_all():
    trails = Trail.query.all()
    return trails_schema.dump(trails)
def create(trail):
    Name=trail.get("Name")
    existing_trail = Trail.query.filter(Trail.Name == Name).one_or_none()
    if existing_trail is None:
        new_trail = trail_schema.load(trail, session=db.session)
        db.session.add(new_trail)
        db.session.commit()
        return trail_schema.dump(new_trail), 201
    else:
        abort(406, f"Trail with name {Name} already exists")
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
        existing_trail.Owner_id = update_trail.Owner_id
        db.session.merge(existing_trail)
        db.session.commit()
        return trail_schema.dump(existing_trail), 201
    else:
        abort(404, f"Trail with name {trail_Name} not found")
def delete(trail_id):
    existing_trail = Trail.query.filter(Trail.TrailID == trail_id).one_or_none()
    if existing_trail:
        db.session.delete(existing_trail)
        db.session.commit()
        return make_response(f"Trail with id {trail_id} successfully deleted", 200)
    else:      
        abort(404, f"Trail with id {trail_id} not found")