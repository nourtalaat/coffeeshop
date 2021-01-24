import json
import os

from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from icecream import ic
from sqlalchemy import exc

from .auth.auth import AuthError, requires_auth
from .database.models import Drink, db_drop_and_create_all, setup_db

app = Flask(__name__)
setup_db(app)
CORS(app)

# Drops and recreates the database, must be run at least the first time
db_drop_and_create_all()

## ROUTES

# GET route that returns drinks to all users publically in the short representation
@app.route('/drinks', methods=['GET'])
def get_drinks():
    try:
        rawDrinks = Drink.query.all()
        drinks = [rawDrink.short() for rawDrink in rawDrinks]
        return jsonify({
            'success': True,
            'drinks': drinks
        })
    except Exception as e:
        abort(400)

# GET route that returns drinks to users who have the 'get:drinks-detail' permission (e.g. Baristas) in the long representation
@app.route('/drinks-detail', methods=['GET'])
@requires_auth(permission='get:drinks-detail')
def get_drinks_detail():
    try:
        rawDrinks = Drink.query.all()
        drinks = [rawDrink.long() for rawDrink in rawDrinks]
        return jsonify({
            'success': True,
            'drinks': drinks
        })
    except Exception as e:
        abort(400)

# POST route that adds a drink to the database from a user that has the 'post:drinks' permission (e.g. Manager)
@app.route('/drinks', methods=['POST'])
@requires_auth(permission='post:drinks')
def insert_drink():
    try:
        data = request.get_json()
        newDrink = Drink(title=data['title'], recipe=json.dumps(data['recipe']))
        newDrink.insert()
        return jsonify({
            'success': True,
            'drinks': [newDrink.long()]
        })
    except Exception as e:
        Drink.rollback(None)
        abort(400)


# PATCH route that updates a drink given its 'id' in the URL, given that the user has the 'patch:drinks' permission (e.g. Manager)
@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth(permission='patch:drinks')
def patch_drink(id):
    drink = Drink.query.get(id)
    try:
        data = request.get_json()
        if "title" in data:
            drink.title = data['title']
        if "recipe" in data:
            drink.recipe = data['recipe']
        drink.update()
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
            })
    except Exception as e:
        ic(e)
        abort(400)
    

# DELETE route that deletes a drink given its 'id' in the URL, given that the user has the 'delete:drinks' permission (e.g. Manager)
@app.route('/drinks/<id>', methods=['DELETE'])
@requires_auth(permission='delete:drinks')
def delete_drink(id):
    drink = Drink.query.get(id)
    try:
        drink.delete()
        return jsonify({
            'success': True,
            'delete': id
        })
    except Exception:
        Drink.rollback(None)
        abort(400)

## Error Handling

# Handles status code 400, bad request
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
                    "success": False, 
                    "error": 400,
                    "message": "bad request"
                    }), 400

# Handles status code 401, unauthorized
@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
                    "success": False, 
                    "error": 401,
                    "message": "unauthorized"
                    }), 401

# Handles status code 403, forbidden
@app.errorhandler(403)
def forbidden(error):
    return jsonify({
                    "success": False, 
                    "error": 403,
                    "message": "forbidden"
                    }), 403

# Handles status code 404, not found
@app.errorhandler(404)
def not_found(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "not found"
                    }), 404

# Handles status code 405, method not allowed
@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
                    "success": False, 
                    "error": 405,
                    "message": "method not allowed"
                    }), 405

# Handles status code 422, unprocessable entity
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

# Handles exception 'AuthError', returns 401
@app.errorhandler(AuthError)
def autherror(error):
    return jsonify({
                    "success": False, 
                    "error": 401,
                    "message": "unauthorized"
                    }), 401