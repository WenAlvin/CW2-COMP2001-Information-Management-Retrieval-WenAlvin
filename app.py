import connexion
from flask import request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields as ma_fields, validate, ValidationError
import requests


# Controller functions (linked to operationIds in YAML)
def get_trails():
    email = validate_auth()
    with db.session() as session:
        rows = session.execute("SELECT TrailID, Name FROM Trails").fetchall()
        trails = [{'id': row[0], 'name': row[1]} for row in rows]
    return jsonify(trails)

def create_trail(body):
    email = validate_auth()
    try:
        validated_data = trail_schema.load(body)  # Additional Marshmallow validation
    except ValidationError as err:
        abort(400, str(err.messages))

    with db.session() as session:
        try:
            result = session.execute(
                "EXEC CreateTrail @Name=:name, @Description=:description, @OwnerEmail=:email, @NewTrailID=:new_id",
                {'name': validated_data['name'], 'description': validated_data.get('description', ''), 'email': email, 'new_id': 0}
            )
            new_id = result.fetchone()[0]  # Get OUTPUT
            for loc in validated_data.get('locations', []):
                session.execute(
                    "INSERT INTO Locations (TrailID, Latitude, Longitude, SequenceOrder) VALUES (:trail_id, :lat, :lon, :seq)",
                    {'trail_id': new_id, 'lat': loc['latitude'], 'lon': loc['longitude'], 'seq': loc['sequence_order']}
                )
            session.commit()
            return jsonify({'id': new_id, 'message': 'Trail created'})
        except Exception as e:
            session.rollback()
            abort(500, str(e))

def get_trail(trail_id):
    email = validate_auth()
    with db.session() as session:
        result = session.execute(
            "EXEC ReadTrail @TrailID=:trail_id, @RequesterEmail=:email, @IsLimited=0",
            {'trail_id': trail_id, 'email': email}
        )
        row = result.fetchone()
        if not row:
            abort(404, "Trail not found")
        trail = {'id': row[0], 'name': row[1], 'description': row[2]}  # Adjust based on proc output
    return jsonify(trail)

def update_trail(trail_id, body):
    email = validate_auth()
    try:
        validated_data = trail_schema.load(body)  # Additional Marshmallow validation
    except ValidationError as err:
        abort(400, str(err.messages))

    with db.session() as session:
        try:
            session.execute(
                "EXEC UpdateTrail @TrailID=:trail_id, @Name=:name, @Description=:description, @RequesterEmail=:email",
                {'trail_id': trail_id, 'name': validated_data['name'], 'description': validated_data.get('description', ''), 'email': email}
            )
            session.commit()
            return jsonify({'message': 'Trail updated'})
        except Exception as e:
            session.rollback()
            abort(403 if 'Unauthorized' in str(e) else 500, str(e))

def delete_trail(trail_id):
    email = validate_auth()
    with db.session() as session:
        try:
            session.execute(
                "EXEC DeleteTrail @TrailID=:trail_id, @RequesterEmail=:email",
                {'trail_id': trail_id, 'email': email}
            )
            session.commit()
            return jsonify({'message': 'Trail deleted'})
        except Exception as e:
            session.rollback()
            abort(403 if 'Unauthorized' in str(e) else 500, str(e))

if __name__ == '__main__':
    app.run(port=5000, debug=True)