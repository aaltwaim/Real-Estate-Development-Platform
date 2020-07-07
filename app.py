import os
from flask import Flask, request, abort, jsonify, render_template, session, redirect, url_for
from werkzeug.exceptions import HTTPException
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import json
import sys
from os import environ as env
from auth import AuthError, requires_auth, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_CALLBACK_URL, AUTH0_DOMAIN, AUTH0_AUDIENCE
# , requires_signed_in
from jose import jwt
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode
import constants


AUTH0_CLIENT_ID = constants.AUTH0_CLIENT_ID
AUTH0_CLIENT_SECRET = constants.AUTH0_CLIENT_SECRET
AUTH0_CALLBACK_URL = constants.AUTH0_CALLBACK_URL
AUTH0_DOMAIN = constants.AUTH0_DOMAIN
AUTH0_AUDIENCE = constants.AUTH0_AUDIENCE
AUTH0_BASE_URL = 'https://' + constants.AUTH0_DOMAIN

# create and configure the app

app = Flask(__name__)
app.secret_key = 'super hard'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://aaltwaim@localhost:5432/estate'
# app.config.from_object(env['APP_SETTINGS'])
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Building, Unit

oauth = OAuth(app)
auth0 = oauth.register(
    'auth0',
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    api_base_url=AUTH0_BASE_URL,
    access_token_url=AUTH0_BASE_URL + '/oauth/token',
    authorize_url=AUTH0_BASE_URL + '/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    }
)


# main page
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL,
                                    audience=AUTH0_AUDIENCE)


@app.route('/login-results')
def callback_handling():
    res = auth0.authorize_access_token()
    token = res.get('access_token')
    session['jwt_token'] = token

    return redirect('/buildings')


# implement endpoint
# Get /buildings
@app.route('/buildings', methods=['GET'])
def get_buildings():
    try:
        buildings = Building.query.all()
        return jsonify({
            'success': True,
            'buildings': [building.show() for building in buildings],
        })

    except Exception:
        abort(404)


# implement endpoint
# Get /buildings/<id>
@app.route('/buildings/<id>', methods=['GET'])
@requires_auth("get:building-by-id")
def get_building_by_id(jwt, id):
    try:
        building = Building.query.filter(Building.id == id).one_or_none()
        return jsonify({
            'success': True,
            'building': [building.show()]
        })
    except Exception:
        print(jwt)
        abort(404)


# implement endpoint
# Post /buildings
@app.route('/buildings', methods=['POST'])
@requires_auth('post:buildings')
def add_building(jwt):
    body = request.get_json()
    ownerID = body.get('ownerID')
    name = body.get('name')
    address = body.get('address')
    description = body.get('description')
    number_of_units = body.get('number_of_units')
    building_image = body.get('building_image')

    if not ('ownerID' in body and 'name' in body and 'address' in body
            and 'description' in body and 'number_of_units' in body
            and 'building_image' in body):
        abort(422)
    try:
        new_building = Building(ownerID=ownerID, name=name, address=address,
                                description=description,
                                number_of_units=number_of_units,
                                building_image=building_image)
        new_building.insert()
        return jsonify({
            'success': True,
            'created': [new_building.show()],
        })
    except Exception:
        abort(422)


# implement endpoint
# Patch /buildings
@app.route('/buildings/<id>', methods=['PATCH'])
@requires_auth('patch:buildings')
def update_building(jwt, id):

    building = Building.query.filter(Building.id == id).one_or_none()
    if building:
        try:
            body = request.get_json()
            ownerID = body.get('ownerID')
            name = body.get('name')
            address = body.get('address')
            description = body.get('description')
            number_of_units = body.get('number_of_units')
            building_image = body.get('building_image')
            if ownerID:
                building.ownerID = ownerID
            if name:
                building.name = name
            if address:
                building.address = address
            if description:
                building.description = description
            if number_of_units:
                building.number_of_units = number_of_units
            if building_image:
                building.building_image = building_image
            building.update()
            return jsonify({
                'success': True,
                'buildings': [building.show()],
            })
        except Exception:
            abort(422)
    else:
        abort(404)


# implement endpoint
# delete /buildings/<id>
@app.route('/buildings/<id>', methods=['DELETE'])
@requires_auth('delete:buildings')
def delete_building(jwt, id):
    building = Building.query.get(id)
    if building:
        try:
            building.delete()
            return jsonify({
                'success': True,
                'delete': id,
            })
        except Exception:
            abort(422)
    else:
        abort(404)


# implement endpoint
# Get /buildings/<id>/units
@app.route('/buildings/<int:building_id>/units', methods=['GET'])
def get_units_based_on_building(building_id):
    try:
        units_by_building = Unit.query.filter(
            Unit.building_id == building_id).all()
        return jsonify({
            'success': True,
            'buildings': [unit.show() for unit in units_by_building],
        })

    except Exception:
        abort(404)


# implement error handler 422
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False,
                    "error": 422,
                    "message": "unprocessable"
                    }), 422


# implement error handler 404
@app.errorhandler(404)
def not_found(error):
    return jsonify({
                    "success": False,
                    "error": 404,
                    "message": "not found"
                    }), 404


# implement error handler for AuthError
@app.errorhandler(AuthError)
def auth_error_handler(ex):
    return jsonify({
                    "success": False,
                    "error": ex.status_code,
                    "message": ex.error,
                    }), 401


# implement error handler 400
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
                    "success": False,
                    "error": 400,
                    "message": "bad request"
                    }), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
