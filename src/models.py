from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
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
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(250), unique=True,nullable=False)
    name = db.Column(db.String(250), unique=False,nullable=False)
    skin = db.Column(db.String(500), unique=False, nullable=True)
    hair = db.Column(db.String(500), unique=False, nullable=True)
    gender = db.Column(db.String(500), unique=False, nullable=True)
    weight = db.Column(db.Integer, unique=False, nullable=True)
    height = db.Column(db.Integer, unique=False, nullable=True)
    home = db.Column(db.String(500), unique=False, nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "gender": self.gender,
            "hair": self.hair,
            "skin": self.skin,
            "weight":self.weight,
            "home":self.home,
            "height":self.height
        }
    
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(250), unique=True,nullable=False)
    name = db.Column(db.String(250), unique=False,nullable=False)
    rotation = db.Column(db.Integer, unique=False, nullable=True)
    orbit = db.Column(db.Integer, unique=False, nullable=True)
    population = db.Column(db.Integer, unique=False, nullable=True)
    diameter = db.Column(db.Integer, unique=False, nullable=True)
    climate = db.Column(db.String(500), unique=False, nullable=True)
    surface_water = db.Column(db.Integer, unique=False, nullable=True)
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
    
class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = Column(db.Integer, ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, unique=False, nullable=True)
    person_id = db.Column(db.Integer, unique=False, nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user,
            "planet_id": self.planet_id,
            "person_id": self.person_id,
        }
