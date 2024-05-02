#!/usr/bin/python3
'''places_amenities module that handles all default RestFul API actions'''
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity
from models import storage_t


@app_views.route('/places/<place_id>/amenities', strict_slashes=False,
                 methods=['GET'])
def get_amenities_by_place(place_id):
    '''Retrieves the list of all Amenity objects of a Place'''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if storage_t == 'db':
        amenities = [amenity.to_dict() for amenity in place.amenities]
        for amenity in amenities:
            if 'place_amenities' in amenity:
                del amenity['place_amenities']
        return jsonify(amenities)
    else:
        amenities = [storage.get(Amenity, amenity_id)
                     for amenity_id in place.amenity_ids]
    return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_amenity_from_place(place_id, amenity_id):
    '''Deletes an Amenity object to a Place'''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if storage_t == 'db':
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['POST'])
def link_amenity_to_place(place_id, amenity_id):
    '''Links an Amenity object to a Place'''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if storage_t == 'db':
        if amenity in place.amenities:
            dict_amenity = amenity.to_dict()
            return jsonify(dict_amenity), 200
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)
    storage.save()
    dict_amenity = amenity.to_dict()
    if storage_t == 'db' and 'place_amenities' in dict_amenity:
        del dict_amenity['place_amenities']
    return jsonify(dict_amenity), 201
