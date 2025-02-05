from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Person(db.Model):
    __tablename__ = 'person'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(250), unique=True,nullable=False)
    name = db.Column(db.String(250), unique=False,nullable=False)
    birth = db.Column(db.String(250), unique=False, nullable=True)
    skin = db.Column(db.String(250), unique=False, nullable=True)
    hair = db.Column(db.String(250), unique=False, nullable=True)
    eyes = db.Column(db.String(250), unique=False, nullable=True)
    gender = db.Column(db.String(250), unique=False, nullable=True)
    weight = db.Column(db.Integer, unique=False, nullable=True)
    height = db.Column(db.Integer, unique=False, nullable=True)
    planet_id = db.Column(db.Integer,db.ForeignKey('planet.id'),unique=False, nullable=True)
    planet = db.Column(db.String(250),unique=False,nullable=True)
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "gender": self.gender,
            "birth": self.birth,
            "hair": self.hair,
            "skin": self.skin,
            "eyes":self.eyes,
            "weight":self.weight,
            "planet":self.planet,
            "height":self.height
        }
    def identify(self):
        return{
            "id": self.id,
            "name": self.name,
            "url": self.url}
    
@event.listens_for(Person, 'before_insert')
def set_home(mapper, connect, target):
    if target.planet_id:
        planet = Planet.query.get(target.planet_id)
        if planet:
            target.planet = planet.name
    

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(250), unique=True,nullable=False)
    name = db.Column(db.String(250), unique=False,nullable=False)
    rotation = db.Column(db.Integer, unique=False, nullable=True)
    orbit = db.Column(db.Integer, unique=False, nullable=True)
    population = db.Column(db.BigInteger, unique=False, nullable=True)
    diameter = db.Column(db.Integer, unique=False, nullable=True)
    climate = db.Column(db.String(500), unique=False, nullable=True)
    surface_water = db.Column(db.String(50), unique=False, nullable=True)
    terrain = db.Column(db.String(500), unique=False, nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "rotation": self.rotation,
            "orbit": self.orbit,
            "population": self.population,
            "diameter":self.diameter,
            "climate":self.climate,
            "surface_water":self.surface_water,
            "terrain":self.terrain
        }
    
    def identify(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url}
    
class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(250), unique=True,nullable=False)
    name = db.Column(db.String(250), unique=False,nullable=False)
    model = db.Column(db.String(250), unique=False,nullable=True)
    passengers = db.Column(db.Integer, unique=False, nullable=True)
    vehicle_class = db.Column(db.String(250), unique=False, nullable=True)
    manufacturer = db.Column(db.String(250), unique=False, nullable=True)
    cost = db.Column(db.String(50), unique=False, nullable=True)
    length = db.Column(db.Numeric(precision=4,scale=2), unique=False, nullable=True)
    crew = db.Column(db.Integer, unique=False, nullable=True)
    cargo = db.Column(db.Integer, unique=False, nullable=True)
    consumables = db.Column(db.String(250), unique=False, nullable=True)
    max_atm_speed = db.Column(db.Integer, unique=False, nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "vehicle_class":self.vehicle_class,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "passengers":self.passengers,
            "crew": self.crew,
            "cargo":self.cargo,
            "cost":self.cost,
            "consumables":self.consumables,
            "max_atm_speed":self.max_atm_speed
        }
    def identify(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url}
    
class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer,db.ForeignKey('planet.id'), unique=False, nullable=True)
    person_id = db.Column(db.Integer,db.ForeignKey('person.id'), unique=False, nullable=True)
    vehicle_id = db.Column(db.Integer,db.ForeignKey('vehicle.id'), unique=False, nullable=True)
    planet = db.Column(db.String(50), unique=False, nullable=True)
    person = db.Column(db.String(50), unique=False, nullable=True)
    vehicle = db.Column(db.String(50), unique=False, nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user,
            "planet_id": self.planet_id,
            "person_id": self.person_id,
            "vehicle_id": self.person_id,
        }
#Para visualizar en admin
@event.listens_for(Favorite, 'before_insert')
def set_favs(mapper, connect, target):
    if target.planet_id:
        planet = Planet.query.get(target.planet_id)
        if planet:
            target.planet = planet.name

    elif target.person_id:
        person = Person.query.get(target.person_id)
        if person:
            target.person = person.name
    
    elif target.vehicle_id:
        vehicle = Vehicle.query.get(target.vehicle_id)
        if vehicle:
            target.vehicle = vehicle.name

