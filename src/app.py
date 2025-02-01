"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Person, Planet, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/users', methods=['GET'])
def get_users_list():
    user_db = User.query.all()
    response_body = [(user.email,user.is_active) for user in user_db]
    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def get_people_names():
    people_db = Person.query.all()
    response_body = [person.name for person in people_db]
    return jsonify(response_body), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person_data(people_id):
    person_db = Person.query.get(people_id)
    if person_db is not None:
        response_body = person_db.serialize()
        return jsonify(response_body), 200
    return jsonify('Bad Request: Character not found'), 400

@app.route('/planets', methods=['GET'])
def get_planets_names():
    planets_db = Planet.query.all()
    response_body = [planet.name for planet in planets_db]
    return jsonify(response_body), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_data(planet_id):
    planet_db = Planet.query.get(planet_id)
    if planet_db is not None:
        response_body = planet_db.serialize()
        return jsonify(response_body), 200
    return jsonify('Bad Request: Planet not found'), 400

@app.route('/users/favorites', methods=['GET'])
def get_favorites():
    active_user = User.query.filter_by(is_active=True)
    favs_db = Favorite.query.filter_by(user = active_user.id)
    response_body = [person.name for person in people_db]
    return jsonify(response_body), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
