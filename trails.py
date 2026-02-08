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
        new_trail = Trail(
            Name=Name,
            Description=trail.get("Description"),
            OwnerID=trail.get("OwnerID")
        )
    Description=trail.get("Description")
    Locations=trail.get("Locations", [])
    if not Name or not OwnerID:
        abort(400, "Trail must have a name and owner ID")
def read_one(name):
    trail = Trail.query.filter(Trail.Name == name).one_or_none()
    if trail is not None:
        return trail_schema.dump(trail)
    else:
        abort(404, f"Trail with name {name} not found")
def update(trail_id, trail):
    if trail_id in TRAILS:
        trail["id"] = trail_id
        trail["CreatedDate"] = get_timestamp()
        TRAILS[trail_id] = trail
        return trail
    else:
        abort(404, f"Trail with id {trail_id} not found")
def delete(trail_id):
    if trail_id in TRAILS:
        del TRAILS[trail_id]
        return f"Trail {trail_id} successfully deleted", 204
    else:
        abort(404, f"Trail with id {trail_id} not found")