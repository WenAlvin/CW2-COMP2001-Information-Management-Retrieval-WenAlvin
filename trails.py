from datetime import datetime
from flask import abort


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

TRAILS = {
    "Plymouth Circular": {
        "name": "Plymouth Circular",
        "Description": "A challenging trail with stunning mountain views.",
        "Length": "5 km",
        "ElevationGain": "500 m",
        "Difficulty": "Hard",
        "Route Type": "Loop",
        "Estimated Time": "3 hours",
        "Features": "Waterfalls, Rocky terrain, Scenic overlooks",
        "CreatedDate": get_timestamp()
},
    "HK Circular": {
        "name": "HK Trail",
        "Description": "A scenic trail that takes you through lush forests and along a beautiful coastline.",
        "Length": "2 km",
        "ElevationGain": "200 m",
        "Difficulty": "Easy",
        "Route Type": "Linear",
        "Estimated Time": "2 hours",
        "Features": "Waterfalls, Rocky terrain, Scenic overlooks",
        "CreatedDate": get_timestamp()
    }
}
def read_all():
    return list(TRAILS.values())
def create(trail):
    if "name" not in trail:
        TRAILS[trail["name"]] = trail
        trail["CreatedDate"] = get_timestamp()
        return trail, 201
    else:
        abort(400, f"Trail with name {trail['name']} already exists")
def read_one(trail_id):
    if trail_id in TRAILS:
        return TRAILS[trail_id]
    else:
        abort(404, f"Trail with id {trail_id} not found")
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