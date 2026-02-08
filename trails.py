from datetime import datetime


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
