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
from models import db, User, Person, Planet, Favorite,Vehicle
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
def get_people():
    people_db = Person.query.all()
    response_body = [person.identify() for person in people_db]
    return jsonify(response_body), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_data(people_id):
    person_db = Person.query.get(people_id)
    if person_db is not None:
        response_body = person_db.serialize()
        return jsonify(response_body), 200
    return jsonify('Bad Request: Character not found'), 400

@app.route('/planets', methods=['GET'])
def get_planets():
    planets_db = Planet.query.all()
    response_body = [planet.identify() for planet in planets_db]
    return jsonify(response_body), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_data(planet_id):
    planet_db = Planet.query.get(planet_id)
    if planet_db is not None:
        response_body = planet_db.serialize()
        return jsonify(response_body), 200
    return jsonify('Bad Request: Planet not found'), 400

@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles_db = Vehicle.query.all()
    response_body = [vehicle.identify() for vehicle in vehicles_db]
    return jsonify(response_body), 200

@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle_data(vehicle_id):
    vehicle_db = Vehicle.query.get(vehicle_id)
    if vehicle_db is not None:
        response_body = vehicle_db.serialize()
        return jsonify(response_body), 200
    return jsonify('Bad Request: Vehicle not found'), 400

@app.route('/users/favorites', methods=['GET'])
def get_favorites():
    active_user = User.query.filter_by(is_active=True).first()
    if active_user is not None:
        fav_list = Favorite.query.filter_by(user = active_user.id)
        response_body = [active_user.serialize()]
        for item in fav_list:
            if item.planet_id:
                planet = Planet.query.get(item.planet_id)
                response_body.append(planet.identify())
            elif item.person_id:
                person = Person.query.get(item.person_id)
                response_body.append(person.identify())
            elif item.vehicle_id:
                vehicle = Vehicle.query.get(item.vehicle_id)
                response_body.append(vehicle.identify())
        return jsonify(response_body), 200
    return jsonify('Bad request: Please login to view list'),400

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    active_user = User.query.filter_by(is_active=True).first()
    if active_user is None:
        return jsonify('Bad Request: Please login to add planet'),400
    planet = Planet.query.get(planet_id)
    if planet is not None:
        fav_add = Favorite(user=active_user.id, planet_id = planet.id)
        db.session.add(fav_add)
        db.session.commit()
        response_body = planet.serialize()
        return jsonify(f'Success, planet added to favorites: {response_body}'), 200
    return jsonify('Bad Request: Planet not found in database'),400

@app.route('/favorite/people/<int:person_id>', methods=['POST'])
def add_favorite_person(person_id):
    active_user = User.query.filter_by(is_active=True).first()
    if active_user is None:
        return jsonify('Bad Request: Please login to add person'),400
    person = Person.query.get(person_id)
    if person is not None:
        fav_add = Favorite(user=active_user.id,person_id = person.id)
        db.session.add(fav_add)
        db.session.commit()
        response_body = person.serialize()
        return jsonify(f'Success, person added to favorites {response_body}'), 200
    return jsonify('Bad Request: Person not found in database'),400

@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['POST'])
def add_favorite_vehicle(vehicle_id):
    active_user = User.query.filter_by(is_active=True).first()
    if active_user is None:
        return jsonify('Bad Request: Please login to add vehicle'),400
    vehicle = Vehicle.query.get(vehicle_id)
    if vehicle is not None:
        fav_add = Favorite(user=active_user.id, vehicle_id = vehicle.id)
        db.session.add(fav_add)
        db.session.commit()
        response_body = vehicle.serialize()
        return jsonify(f'Success, vehicle added to favorites: {response_body}'), 200
    return jsonify('Bad Request: Vehicle not found in database'),400

@app.route('/favorite/planet/<int:planet_del_id>', methods=['DELETE'])
def delete_favorite_planet(planet_del_id):
    active_user = User.query.filter_by(is_active=True).first()
    if active_user is None:
        return jsonify('Bad Request: Please login to remove planet'),400
    planet = Favorite.query.filter_by(user = active_user.id, planet_id = planet_del_id).first()
    if planet is not None:
        db.session.delete(planet)
        db.session.commit()
        return jsonify('Success, planet deleted from favorites list'), 200
    return jsonify('Bad Request: Planet not found in favorites'),400

@app.route('/favorite/people/<int:person_del_id>', methods=['DELETE'])
def delete_favorite_person(person_del_id):
    active_user = User.query.filter_by(is_active=True).first()
    if active_user is None:
        return jsonify('Bad Request: Please login to remove person'),400
    person = Favorite.query.filter_by(user = active_user.id, person_id = person_del_id).first()
    if person is not None:
        db.session.delete(person)
        db.session.commit()
        return jsonify('Success, person deleted from favorites list'), 200
    return jsonify('Bad Request: Person not found in favorites'),400

@app.route('/favorite/vehicle/<int:vehicle_del_id>', methods=['DELETE'])
def delete_favorite_vehicle(vehicle_del_id):
    active_user = User.query.filter_by(is_active=True).first()
    if active_user is None:
        return jsonify('Bad Request: Please login to remove vehicle'),400
    vehicle = Favorite.query.filter_by(user = active_user.id, vehicle_id = vehicle_del_id).first()
    if vehicle is not None:
        db.session.delete(vehicle)
        db.session.commit()
        return jsonify('Success, vehicle deleted from favorites list'), 200
    return jsonify('Bad Request: vehicle not found in favorites'),400

#Extra task
@app.route('/planets', methods=['POST'])
def add_planet():
    request_body = request.get_json()
    name = request_body.get('name')
    url = request_body.get('url')
    rotation = request_body.get('rotation_period')
    orbit = request_body.get('orbital_period')
    population = request_body.get('population')
    diameter = request_body.get('diameter')
    climate = request_body.get('climate')
    surface_water = request_body.get('surface_water')
    terrain = request_body.get('terrain')
    if name is None or url is None:
        return jsonify('Bad Request: Incomplete data, name or url missing'),400
    try:
        new_planet = Planet(name=name,url=url,rotation=rotation,orbit=orbit,population=population,
                            diameter=diameter,climate=climate,surface_water=surface_water,terrain=terrain)
        db.session.add(new_planet)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return(f'Bad Request: Something went wrong, check your inputs'),400
    return jsonify(f'Success, planet {new_planet.name} has been assigned id number {new_planet.id}'),200
#Include a planet_id as part of the request, the id must be already in db Planet.
@app.route('/people', methods=['POST'])
def add_person():
    request_body = request.get_json()
    name = request_body.get('name')
    url = request_body.get('url')
    gender = request_body.get('gender','N/A')
    hair = request_body.get('hair_color')
    skin = request_body.get('skin_color')
    eyes = request_body.get('eye_color')
    weight = request_body.get('mass')
    height = request_body.get('height')
    birth = request_body.get('birth_year')
    planet_id = request_body.get('planet_id')

    if name is None or url is None:
        return jsonify('Bad Request: Incomplete data, name and/or url missing'),400
    try:
        new_person = Person(name=name,url=url,gender=gender,skin=skin,hair=hair,weight=weight,height=height,eyes=eyes,birth=birth,planet_id=planet_id)
        db.session.add(new_person)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return(f'Bad Request: Something went wrong, check your input type'),400
    return jsonify(f'Success, {new_person.name} has been assigned id number {new_person.id}'),200

@app.route('/vehicles', methods=['POST'])
def add_vehicle():
    request_body = request.get_json()
    name = request_body.get('name')
    url = request_body.get('url')
    vehicle_class= request_body.get('vehicle_class')
    model = request_body.get('model')
    manufacturer = request_body.get('manufacturer')
    crew = request_body.get('crew')
    length = request_body.get('length')
    passengers = request_body.get('passengers')
    cargo = request_body.get('cargo_capacity')
    cost = request_body.get('cost_in_credits')
    consumables = request_body.get('consumables')
    max_atm_speed = request_body.get('max_atmosphering_speed')

    if name is None or url is None:
        return jsonify('Bad Request: Incomplete data, name and/or url missing'),400
    try:
        new_vehicle = Vehicle(name=name,url=url,vehicle_class=vehicle_class,model=model,manufacturer=manufacturer,crew=crew,
                              cargo=cargo,cost=cost,consumables=consumables,max_atm_speed=max_atm_speed,passengers=passengers,length=length)
        db.session.add(new_vehicle)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return(f'Bad Request: Something went wrong, check your input type'),400
    return jsonify(f'Success, the {new_vehicle.name} has been assigned id number {new_vehicle.id}'),200

@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is not None:
        db.session.delete(planet)
        db.session.commit()
        return jsonify('Success, planet deleted from database'), 200
    return jsonify('Bad Request: Planet not found in database'),400

@app.route('/people/<int:people_id>', methods=['DELETE'])
def delete_person(people_id):
    person = Person.query.get(people_id)
    if person is not None:
        db.session.delete(person)
        db.session.commit()
        return jsonify('Success, person deleted from database'), 200
    return jsonify('Bad Request: Person not found in database'),400

@app.route('/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if vehicle is not None:
        db.session.delete(vehicle)
        db.session.commit()
        return jsonify('Success, vehicle deleted from database'), 200
    return jsonify('Bad Request: Vehicle not found in database'),400
    
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
