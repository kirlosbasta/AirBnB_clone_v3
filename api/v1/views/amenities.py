#!/usr/bin/python3
'''Amenity model that handles all default RestFul API actions'''
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def amenities():
    '''Return all the amenities'''
    amenities = [amenity.to_dict() for amenity in storage.all(
        Amenity).values()]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET'])
def amenities_id(amenity_id):
    '''Return an amenity by id'''
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity(amenity_id):
    '''Delete an amenity by id'''
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    return jsonify({})


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def create_amenity():
    '''Create an amenity'''
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400
    params = request.get_json()
    if 'name' not in params:
        return jsonify({"error": "Missing name"}), 400
    amenity = Amenity(**params)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def update_amenity(amenity_id):
    '''Update an amenity'''
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400
    params = request.get_json()
    for key, value in params.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict())
