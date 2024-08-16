"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_SECRET_KEY'] = 'Er-Pepe'  # Cambia esta clave por una más segura
jwt = JWTManager(app)

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

# ================================================================
# [GET] /people Listar todos los registros de people en la base de datos.
# ================================================================
@app.route('/people', methods=['GET'])
def get_all_people():
    people = People.query.all()
    people_list = [person.serialize() for person in people]
    return jsonify(people_list), 200

# ================================================================
# [GET] /people/<int:people_id> Muestra la información de un solo personaje según su id.
# ================================================================
@app.route('/people/<int:people_id>', methods=['GET'])
def get_a_person(people_id):
    person = People.query.get(people_id)
    if not person:
        return jsonify({"error": "Person not found"}), 404
    return jsonify(person.serialize()), 200

# ================================================================
# [GET] /planets Listar todos los registros de planets en la base de datos.
# ================================================================
@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    planet_list = [planet.serialize() for planet in planets]
    return jsonify(planet_list), 200

# ================================================================
# [GET] /planets/<int:planet_id> Muestra la información de un solo planeta según su id.
# ================================================================
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_a_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"error": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200

# ================================================================
# [GET] /users Listar todos los usuarios del blog.
# ================================================================
@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    users_list = [user.serialize() for user in users]
    return jsonify(users_list), 200

# ================================================================
# [GET] /users/favorites Listar todos los favoritos que pertenecen al usuario actual.
# ================================================================
@app.route('/users/favorites', methods=['GET'])
@jwt_required()
def get_user_favorites():
    current_user_id = get_jwt_identity()
    print("\n\n\n")
    print(current_user_id)

    if current_user_id is None:
        return jsonify({"msg": "User not found"}), 401
    
    user_query = User.query.get(current_user_id)
    print(user_query)

    if user_query is None:
        return jsonify({"msg": "User not found"}), 401

    favorites = {
        "favoritos_planets": [planet.serialize() for planet in user_query.favoritos_planets],
        "favoritos_people": [people.serialize() for people in user_query.favoritos_peoples],
        "favoritos_vehicles": [vehicle.serialize() for vehicle in user_query.favoritos_vehicles]
    }
    return jsonify(favorites), 200

# ================================================================
# [POST] /favorite/planet/<int:planet_id> Añade un nuevo planet favorito al usuario actual con el id = planet_id.
# ================================================================

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
@jwt_required()
def add_planet_favorite(planet_id):
    
    current_user_id = get_jwt_identity()
    print("\n\n\n")
    print(current_user_id)

    if current_user_id is None:
        return jsonify({"msg": "User not found"}), 401
    
    user_query = User.query.get(current_user_id)
    print(user_query)

    if user_query is None:
        return jsonify({"msg": "User not found"}), 401


    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404
    
    if planet in user_query.favoritos_planets:
        return jsonify({"error": "Planet already in favorites"}), 400

    try:
        user_query.favoritos_planets.append(planet)
        db.session.commit()
        return jsonify(planet.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    

# ================================================================
# [POST] /favorite/people/<int:people_id> Añade un nuevo people favorito al usuario actual con el id = people_id.
# ================================================================

@app.route('/favorite/peoples/<int:people_id>', methods=['POST'])
@jwt_required()
def add_people_favorite(people_id):
        
        current_user_id = get_jwt_identity()
        print("\n\n\n")
        print(current_user_id)

        if current_user_id is None:
            return jsonify({"msg": "User not found"}), 401
        
        user_query = User.query.get(current_user_id)
        print(user_query)

        if user_query is None:
            return jsonify({"msg": "User not found"}), 401


        person = People.query.get(people_id)
        if person is None:
            return jsonify({"error": "Person not found"}), 404
        
        if person in user_query.favoritos_peoples:
            return jsonify({"error": "Person already in favorites"}), 400
        
        try:
            user_query.favoritos_peoples.append(person)
            db.session.commit()
            return jsonify(person.serialize()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
        

# ================================================================
# [PUT] /people/<int:people_id> Modificar la información de un personaje según su ID.
# ================================================================

@app.route('/people/<int:people_id>', methods=['PUT'])
def people_edit(people_id):
    person = People.query.get(people_id)
    if person is None:
        return jsonify({"error": "Person not found"}), 404

    nombre = request.json.get('nombre')
    birth_year = request.json.get('birth_year')
    species = request.json.get('species')
    height = request.json.get('height')
    mass = request.json.get('mass')
    gender = request.json.get('gender')
    hair_color = request.json.get('hair_color')
    skin_color = request.json.get('skin_color')
    homeworld = request.json.get('homeworld')

    if nombre:
        person.nombre = nombre
    if birth_year:
        person.birth_year = birth_year
    if species:
        person.species = species
    if height:
        person.height = height
    if mass:
        person.mass = mass
    if gender:
        person.gender = gender
    if hair_color:
        person.hair_color = hair_color
    if skin_color:
        person.skin_color = skin_color
    if homeworld:
        person.homeworld = homeworld
    
    try:
        db.session.commit()
        return jsonify(person.serialize()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    


# ================================================================
# [PUT] /planet/<int:planet_id Modificar la información de un planeta según su ID.
# ================================================================

@app.route('/planet/<int:planet_id>', methods=['PUT'])
def planet_edit(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404

    nombre = request.json.get('nombre')
    population = request.json.get('population')
    rotation_period = request.json.get('rotation_period')
    orbital_period = request.json.get('orbital_period')
    diameter = request.json.get('diameter')
    gravity = request.json.get('gravity')
    terrain = request.json.get('terrain')
    surface = request.json.get('surface')
    climate = request.json.get('climate')

    if nombre:
        planet.nombre = nombre
    if population:
        planet.population = population
    if rotation_period:
        planet.rotation_period = rotation_period
    if orbital_period:
        planet.orbital_period = orbital_period
    if diameter:
        planet.diameter = diameter
    if gravity:
        planet.gravity = gravity
    if terrain:
        planet.terrain = terrain
    if surface:
        planet.surface = surface
    if climate:
        planet.climate = climate
    
    try:
        db.session.commit()
        return jsonify(planet.serialize()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
        

# ================================================================
# [DELETE] /favorite/planet/<int:planet_id> Elimina un planet favorito con el id = planet_id.
# ================================================================

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
@jwt_required()
def delete_planet_favorite(planet_id):

    current_user_id = get_jwt_identity()
    print("\n\n\n")
    print(current_user_id)

    if current_user_id is None:
        return jsonify({"msg": "User not found"}), 401
        
    user_query = User.query.get(current_user_id)
    print(user_query)

    if user_query is None:
        return jsonify({"msg": "User not found"}), 401


    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404
    
    if planet not in user_query.favoritos_planets:
        return jsonify({"error": "Planet not in favorites"}), 400

    try:
        user_query.favoritos_planets.remove(planet)
        db.session.commit()
        return jsonify(planet.serialize()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    

# ================================================================
# [DELETE] /favorite/people/<int:people_id> Elimina un people favorito con el id = people_id.
# ================================================================

@app.route('/favorite/peoples/<int:people_id>', methods=['DELETE'])
@jwt_required()
def delete_people_favorite(people_id):

    current_user_id = get_jwt_identity()
    print("\n\n\n")
    print(current_user_id)

    if current_user_id is None:
        return jsonify({"msg": "User not found"}), 401
        
    user_query = User.query.get(current_user_id)
    print(user_query)

    if user_query is None:
        return jsonify({"msg": "User not found"}), 401


    person = People.query.get(people_id)
    if person is None:
        return jsonify({"error": "Person not found"}), 404
    
    if person not in user_query.favoritos_peoples:
        return jsonify({"error": "Person not in favorites"}), 400

    try:
        user_query.favoritos_peoples.remove(person)
        db.session.commit()
        return jsonify(person.serialize()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
