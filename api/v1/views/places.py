#!/usr/bin/python3
'''places model that handles all default RestFul API actions'''
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User
import os


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['GET'])
def city_places(city_id):
    '''Return places of a city by city id'''
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        places = [place.to_dict() for place in city.places]
    else:
        places = [place.to_dict() for place in storage.all(Place).values()
                  if place.city_id == city_id]
    return jsonify(places)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def places(place_id):
    '''Return a place by id'''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_place(place_id):
    '''Delete place by id'''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    return jsonify({})


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['POST'])
def create_place(city_id):
    '''Create a place'''
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.is_json:
        return jsonify('Not a JSON'), 400
    params = request.get_json()
    if 'user_id' not in params:
        return jsonify('Missing user_id'), 400
    if 'name' not in params:
        return jsonify('Missing name'), 400
    user = storage.get(User, params['user_id'])
    if not user:
        abort(404)
    params['city_id'] = city_id
    place = Place(**params)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def update_place(place_id):
    '''Update a place'''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.is_json:
        return jsonify('Not a JSON'), 400
    params = request.get_json()
    for key, value in params.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict())
