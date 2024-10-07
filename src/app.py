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
from models import db, User,Characters,Planets,FavoritesCharacters,FavoritesPlanets
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

@app.route('/users', methods=['GET'])
def get_users():
    all_users = User.query.all()

    all_users = list(map(lambda user:user.serialize(),all_users))

    return jsonify(all_users), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.filter_by(id = user_id).first()
    print(user)
    return jsonify(user.serialize()), 200

@app.route('/users', methods=['POST'])
def post_user():
    new_user = request.get_json()

    new_user = User(username = new_user["username"],email = new_user["email"],password = new_user["password"],is_active = new_user["is_active"])

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.serialize()), 201

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    name_user = User.query.filter_by(id = user_id).first()
    delete_user = User.query.filter_by(id = user_id).first()

    db.session.delete(delete_user)
    db.session.commit()

    return jsonify({"message": f"usuario {name_user.username} fue eliminado con exito"}), 200


@app.route('/characters', methods=['GET'])
def get_characters():
    all_characters = Characters.query.all()

    all_characters = list(map(lambda characters:characters.serialize(),all_characters))

    return jsonify(all_characters), 200

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Characters.query.filter_by(id = character_id).first()

    return jsonify(character.serialize()), 200

@app.route('/characters', methods=['POST'])
def post_characters():
    new_character = request.get_json()

    new_character = Characters(name = new_character["name"],gender = new_character["gender"],birth_year = new_character["birth_year"],hair_color = new_character["hair_color"])

    db.session.add(new_character)
    db.session.commit()

    return jsonify(new_character.serialize()), 201

@app.route('/characters/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    character_name = Characters.query.filter_by(id = character_id).first()
    delete_character = Characters.query.filter_by(id = character_id).first()

    db.session.delete(delete_character)
    db.session.commit()

    return jsonify({"message": f"character {character_name.name} fue eliminado con exito"}), 200


@app.route('/planets', methods=['GET'])
def get_planets():
    all_planets = Planets.query.all()

    all_planets = list(map(lambda all_planet:all_planet.serialize(),all_planets))

    return jsonify(all_planets), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planets.query.filter_by(id = planet_id).first()

    return jsonify(planet.serialize()), 200

@app.route('/planets', methods=['POST'])
def post_planet():
    new_planet = request.get_json()

    new_planet = Planets(name = new_planet["name"],climate = new_planet["climate"],terrain = new_planet["terrain"],population = new_planet["population"])

    db.session.add(new_planet)
    db.session.commit()

    return jsonify(new_planet.serialize()), 201

@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet_name = Planets.query.filter_by(id = planet_id).first()
    delete_planet = Planets.query.filter_by(id = planet_id).first()

    db.session.delete(delete_planet)
    db.session.commit()

    return jsonify({"message": f"planeta {planet_name.name} fue eliminado con exito"}), 200

@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_favorites(user_id):
    
    favorites_character = FavoritesCharacters.query.filter_by(user_id = user_id).all()
    favorites_planet = FavoritesPlanets.query.filter_by(user_id = user_id).all()

    favorites = {
        "characters": list(map(lambda character: character.serialize(),favorites_character)),
        "planets": list(map(lambda planet: planet.serialize(),favorites_planet))
    }

    return jsonify(favorites), 200


@app.route('/users/<int:user_id>/favorites/characters/<int:character_id>', methods=['POST'])
def add_favorite_character(user_id,character_id):
    user = User.query.filter_by(id = user_id).first()
    character_name = Characters.query.filter_by(id = character_id).first()
    
    favorite = FavoritesCharacters(user_id = user_id, character_id = character_id)

    db.session.add(favorite)
    db.session.commit()

    return jsonify({"message": f"character {character_name.name} added to favorites with success in the username {user.username}"}), 201

@app.route('/users/<int:user_id>/favorites/characters/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(user_id,character_id):
    user = User.query.filter_by(id = user_id).first()
    character_name = Characters.query.filter_by(id = character_id).first()
    
    favorite =  FavoritesCharacters.query.filter_by(user_id = user_id,character_id = character_id).first()

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"message": f" character {character_name.name} successfully removed from favorites in the user {user.username} "}), 200

@app.route('/users/<int:user_id>/favorites/planets/<int:planet_id>', methods=['POST'])
def add_favorite_planet(user_id,planet_id):
    user = User.query.filter_by(id = user_id).first()
    planet_name = Planets.query.filter_by(id = planet_id).first()
    
    favorite = FavoritesPlanets(user_id = user_id, planet_id = planet_id)

    db.session.add(favorite)
    db.session.commit()

    return jsonify({"message": f"planet {planet_name.name} added to favorites with success in the username {user.username}"}), 201

@app.route('/users/<int:user_id>/favorites/planets/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id,planet_id):
    user = User.query.filter_by(id = user_id).first()
    planet_name = Planets.query.filter_by(id = planet_id).first()
    
    favorite =  FavoritesPlanets.query.filter_by(user_id = user_id,planet_id = planet_id).first()

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"message": f" planet {planet_name.name} successfully deleted from favorites in the user {user.username} "}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
