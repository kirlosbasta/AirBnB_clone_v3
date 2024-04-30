#!/usr/bin/python3
''' cities module '''
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET'])
def cities(state_id):
    '''Return all the cities of state'''
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def city(city_id):
    '''Return a city by id'''
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['DELETE'])
def delete_city(city_id):
    '''Delete a city by id'''
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    return jsonify({})


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def create_city(state_id):
    '''Create a city'''
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400
    params = request.get_json()
    if 'name' not in params:
        return jsonify({"error": "Missing name"}), 400
    city = City(**params)
    city.state_id = state_id
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    '''Update a city'''
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400
    params = request.get_json()
    for key, value in params.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict())
