from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

favoritos_planets = db.Table('favoritos_planets',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('planet_id', db.Integer, db.ForeignKey('planet.id'), primary_key=True),
    db.Column('fecha_de_favorito', db.DateTime, nullable=True, default=datetime.utcnow)
)

# Tabla de asociación para los favoritos de personas
favoritos_peoples = db.Table('favoritos_peoples',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('people_id', db.Integer, db.ForeignKey('people.id'), primary_key=True),
    db.Column('fecha_de_favorito', db.DateTime, nullable=True, default=datetime.utcnow)
)

# Tabla de asociación para los favoritos de vehículos
favoritos_vehicles = db.Table('favoritos_vehicles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('vehicle_id', db.Integer, db.ForeignKey('vehicle.id'), primary_key=True),
    db.Column('fecha_de_favorito', db.DateTime, nullable=True, default=datetime.utcnow)
)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    nombre = db.Column(db.String(250), nullable=False)
    apellido = db.Column(db.String(250), nullable=False)
    fecha_de_subscripcion = db.Column(db.DateTime, nullable=False)
    favoritos_planets = db.relationship('Planet', secondary=favoritos_planets, backref=db.backref('users', lazy='dynamic'))
    favoritos_peoples = db.relationship('People', secondary=favoritos_peoples, backref=db.backref('users', lazy='dynamic'))
    favoritos_vehicles = db.relationship('Vehicle', secondary=favoritos_vehicles, backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return '<User %r>' % self.nombre

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "fecha_de_subscripcion": self.fecha_de_subscripcion,
            "favoritos_planets": [planet.serialize() for planet in self.favoritos_planets],
            "favoritos_peoples": [people.serialize() for people in self.favoritos_peoples],
            "favoritos_vehicles": [vehicle.serialize() for vehicle in self.favoritos_vehicles],
        }

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False)
    population = db.Column(db.BigInteger , nullable=False)
    rotation_period = db.Column(db.Integer, nullable=False)
    orbital_period = db.Column(db.Integer, nullable=False)
    diameter = db.Column(db.Integer, nullable=False)
    gravity = db.Column(db.String(250), nullable=False)
    terrain = db.Column(db.String(250), nullable=False)
    surface = db.Column(db.String(250), nullable=False)
    climate = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return '<Planet %r>' % self.nombre

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "population": self.population,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "terrain": self.terrain,
            "surface": self.surface,
            "climate": self.climate,
        }

class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False)
    birth_year = db.Column(db.String(250), nullable=False)
    species = db.Column(db.String(250), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    mass = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(250), nullable=False)
    hair_color = db.Column(db.String(250), nullable=False)
    skin_color = db.Column(db.String(250), nullable=False)
    homeworld = db.Column(db.Integer, db.ForeignKey('planet.id'))

    def __repr__(self):
        return '<People %r>' % self.nombre

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "birth_year": self.birth_year,
            "species": self.species,
            "height": self.height,
            "mass": self.mass,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "homeworld": self.homeworld,
        }

class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False)
    model = db.Column(db.String(250), nullable=False)
    manufacturer = db.Column(db.String(250), nullable=False)
    clase = db.Column(db.String(250), nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    speed = db.Column(db.Integer, nullable=False)
    length = db.Column(db.Integer, nullable=False)
    cargo_capacity = db.Column(db.Integer, nullable=False)
    mimimum_crew = db.Column(db.Integer, nullable=False)
    passengers = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Vehicle %r>' % self.nombre

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "clase": self.clase,
            "cost": self.cost,
            "speed": self.speed,
            "length": self.length,
            "cargo_capacity": self.cargo_capacity,
            "mimimum_crew": self.mimimum_crew,
            "passengers": self.passengers,
        }