#!/usr/bin/python3
'''users model that handles all default RestFul API actions'''
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def users():
    '''Return all the users'''
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def user(user_id):
    '''Return a user by id'''
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['DELETE'])
def delete_user(user_id):
    '''Delete a user by id'''
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    return jsonify({}), 200


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_user():
    '''Create a user'''
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400
    params = request.get_json()
    if 'email' not in params:
        return jsonify({"error": "Missing email"}), 400
    elif 'password' not in params:
        return jsonify({"error": "Missing password"}), 400
    user = User(**params)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def update_user(user_id):
    '''Update a user'''
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400
    params = request.get_json()
    for key, value in params.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
