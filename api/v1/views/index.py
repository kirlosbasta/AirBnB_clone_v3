#!/usr/bin/python3
'''app_views module'''
from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
from flask import jsonify


classes = {"amenities": Amenity, "cities": City, "places": Place,
           "reviews": Review, "states": State, "users": User}


@app_views.route('/status', strict_slashes=False)
def status():
    '''return status'''
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    '''return stats about the objects in storage'''
    stats = {}
    for key, value in classes.items():
        stats[key] = storage.count(value)
    return jsonify(stats)
