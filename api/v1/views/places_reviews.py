#!/usr/bin/python3
'''review model that handles all default RestFul API actions'''
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
import os


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['GET'])
def place_reviews(place_id):
    '''Return reviews of a place by place id'''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['GET'])
def review(review_id):
    '''Return a review by id'''
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_review(review_id):
    '''Delete review by id'''
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    return jsonify({})


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['POST'])
def create_review(place_id):
    '''Create a review'''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.is_json:
        return jsonify({'error': 'Not a JSON'}), 400
    params = request.get_json()
    if 'user_id' not in params:
        return jsonify({'error': 'Missing user_id'}), 400
    user = storage.get(User, params['user_id'])
    if not user:
        abort(404)
    if 'text' not in params:
        return jsonify({'error': 'Missing text'}), 400
    params['place_id'] = place_id
    rev = Review(**params)
    rev.save()
    return jsonify(rev.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['PUT'])
def update_review(review_id):
    '''Update a review'''
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not request.is_json:
        return jsonify({'error': 'Not a JSON'}), 400
    params = request.get_json()
    for key, value in params.items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict())
