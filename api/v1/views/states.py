#!/usr/bin/python3
''' states module '''
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['GET'])
def states(state_id=None):
    '''return all the states'''
    if state_id:
        state = storage.get(State, state_id)
        if state:
            return jsonify(state.to_dict())
        else:
            abort(404)
    else:
        states = [state.to_dict() for state in storage.all(State).values()]
        return jsonify(states)


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id):
    '''Delete a state from storage'''
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    else:
        storage.delete(state)
        return jsonify({})


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    '''Create new state'''
    if not request.is_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    params = request.get_json()
    if 'name' not in params:
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_state = State(name=params['name'])
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['PUT'])
def update(state_id):
    '''Update a state with id state_id'''
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.is_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    params = request.get_json()
    for key, value in params.items():
        if key != 'id' or key != 'created_at' or key != 'updated_at':
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict())
