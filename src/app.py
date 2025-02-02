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
def get_active_user():
    user_db = User.query.filter_by(is_active = True).first()

    if user_db is None:
        return jsonify('No active user, please login to start'),400
    response_body = user_db.serialize()
    return jsonify(response_body), 200

@app.route('/users', methods=['GET'])
def get_users_list():
    user_db = User.query.all()
    response_body = [(user.serialize()) for user in user_db]
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
    active_user = User.query.filter_by(is_active=True).first()
    if active_user is not None:
        fav_list = Favorite.query.filter_by(user = active_user.id)
        response_body = []
        for item in fav_list:
            if item.planet_id:
                planet = Planet.query.get(item.planet_id)
                response_body.append({"name":planet.name,"url":planet.url})
            elif item.person_id:
                person = Person.query.get(item.person_id)
                response_body.append({"name":person.name,"url":person.url})
        return jsonify(response_body), 200
    return jsonify('Bad request: Please login to view list'),400

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    active_user = User.query.filter_by(is_active=True).first()
    if active_user is None:
        return jsonify('Bad Request: Please login to add planet'),400
    planet = Planet.query.get(planet_id)
    if planet is not None:
        fav_add = Favorite(user=active_user.id,planet_id = planet.id)
        db.session.add(fav_add)
        db.session.commit()
        return jsonify('Success, planet added to favorites'), 200
    return jsonify('Bad Request: Planet not found in database'),400

@app.route('/favorite/person/<int:person_id>', methods=['POST'])
def add_favorite_person(person_id):
    active_user = User.query.filter_by(is_active=True).first()
    if active_user is None:
        return jsonify('Bad Request: Please login to add person'),400
    person = Person.query.get(person_id)
    if person is not None:
        fav_add = Favorite(user=active_user.id,person_id = person.id)
        db.session.add(fav_add)
        db.session.commit()
        return jsonify('Success, person added to favorites'), 200
    return jsonify('Bad Request: Person not found in database'),400

@app.route('/favorite/planet/<int:planet_del_id>', methods=['DELETE'])
def delete_favorite_planet(planet_del_id):
    active_user = User.query.filter_by(is_active=True).first()
    if active_user is None:
        return jsonify('Bad Request: Please login to remove planet'),400
    planet = Favorite.query.filter_by(user = active_user.id, planet_id = planet_del_id).first()
    if planet is not None:
        db.session.delete(planet)
        db.session.commit()
        return jsonify('Success, planet deleted from favorite list'), 200
    return jsonify('Bad Request: Planet not found in favorites'),400

@app.route('/favorite/planet/<int:person_del_id>', methods=['DELETE'])
def delete_favorite_person(person_del_id):
    active_user = User.query.filter_by(is_active=True).first()
    if active_user is None:
        return jsonify('Bad Request: Please login to remove planet'),400
    person = Favorite.query.filter_by(user = active_user.id, person_id = person_del_id).first()
    if person is not None:
        db.session.delete(person)
        db.session.commit()
        return jsonify('Success, person deleted from favorite list'), 200
    return jsonify('Bad Request: Person not found in favorites'),400
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
