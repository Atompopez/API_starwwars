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
from models import db, User, People, Planet, Favorite
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
def get_user():
    all_users = User.query.all()

    return jsonify(list(map(lambda user : user.serialize(), all_users))), 200

@app.route('/<int:user>/favorites', methods=['GET'])
def get_favorites(user):
    all_favorites = Favorite.query.filter_by(user_id = user)

    return jsonify(list(map(lambda favorite : favorite.serialize(), all_favorites))), 200

@app.route('/favorite/planet/<int:id_planet>', methods=['POST'])
def post_favorite_planet(id_planet):
    id_user = 1 
    new_favorite = Favorite(name = 'prueba', user_id = id_user, planet_id = id_planet)
    db.session.add(new_favorite)
    db.session.commit()
    
    return 'created favorite', 200

@app.route('/favorite/people/<int:id_people>', methods=['POST'])
def post_favorite_people(id_people):
    id_user = 1 
    new_favorite = Favorite(name = 'prueba', user_id = id_user, people_id = id_people)
    db.session.add(new_favorite)
    db.session.commit()
    
    return 'created favorite', 200

@app.route('/people', methods=['GET'])
def get_people():
    all_people = People.query.all()

    return jsonify(list(map(lambda people : people.serialize(), all_people))), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_id (people_id):
    all_people = People.query.filter_by(id = people_id).first()
    
    return jsonify(all_people.serialize())

@app.route('/planet', methods=['GET'])
def get_planet():
    all_planet = Planet.query.all()

    return jsonify(list(map(lambda people : people.serialize(), all_planet))), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet_id (planet_id):
    all_planet = Planet.query.filter_by(id = planet_id).first()
    
    return jsonify(all_planet.serialize())

@app.route('/favorite/planet/<int:id>', methods=['DELETE'])
def delete_planet_id (id):
    all_planet = Favorite.query.filter_by(planet_id = id).first()
    print(all_planet)
    db.session.delete(all_planet)
    db.session.commit()
    
    return 'deleted favorite'

@app.route('/favorite/people/<int:id>', methods=['DELETE'])
def delete_people_id (id):
    all_people = Favorite.query.filter_by(people_id = id).first()
    print(all_people)
    db.session.delete(all_people)
    db.session.commit()
    
    return 'deleted favorite'

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
