from flask import make_response, abort, request, jsonify

from config import db
from models import Trail, User, Location, trail_schema, trails_schema, LocationSchema
import jwt
import requests
from datetime import datetime, timedelta, timezone

AUTH_URL = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"
SECRET_KEY = "secretkeyfortesting"

def validate_auth():
    authorization_header = request.headers.get('Authorization')
    if not authorization_header or not authorization_header.startswith('Bearer '):
        abort(401, "Authorization required (Bearer token)")
    token = authorization_header.split()[1]
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded.get('email')
    except jwt.ExpiredSignatureError:
        abort(401, "Token expired")
    except jwt.InvalidTokenError:
        abort(401, "Invalid token")

def login(body):
    credentials = {
        'email': body.get('email'),
        'password': body.get('password')
    }
    if not credentials['email'] or not credentials['password']:
        abort(400, "Email and password required")
    try:
        response = requests.post(AUTH_URL, json=credentials)
        if response.status_code == 200:
            try:
                json_response = response.json()
                if isinstance(json_response, list) and len(json_response) == 2 and json_response[0] == "Verified" and json_response[1] == "True":
                    # Generate local JWT with email (expires in 1 hour)
                    token = jwt.encode(
                        {
                            'email': credentials['email'],
                            'exp': datetime.now(tz=timezone.utc) + timedelta(hours=1)
                        },
                        SECRET_KEY,
                        algorithm="HS256"
                    )
                    print(token)
                    return jsonify({"token": token}), 200
                else:
                    abort(401, "Verification failed")
            except requests.JSONDecodeError:
                abort(401, "Response is not valid JSON")
        else:
            abort(401, f"Authentication failed with status code {response.status_code}")
    except Exception as e:
        abort(401, f"Auth failed: {str(e)}")

def read_all():
    trails = Trail.query.all()
    return trails_schema.dump(trails)
def create(trail):
    email = validate_auth()
    name=trail.get("name")
    existing_trail = Trail.query.filter(Trail.Name == name).one_or_none()
    if existing_trail is None:
        new_trail = trail_schema.load(trail, session=db.session)
        new_trail.OwnerID = User.query.filter(User.Email == email).one_or_none().UserID
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