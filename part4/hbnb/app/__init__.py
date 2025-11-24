from flask import Flask, render_template, redirect, url_for, request
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
import requests

bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()


def create_app(config_class="config.DevelopmentConfig"):
    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.auth import api as auth_ns
    from app.api.v1.protected import api as protected_ns
    from app.models.place import Place

    app = Flask(__name__)
    app.config.from_object(config_class)
    api = Api(app, version='1.0',
              title='HBnB API',
              description='HBnB Application API',
              doc='/api/v1/',
              prefix='/api/v1')
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    # Register the users namespace
    api.add_namespace(users_ns, path='/users')

    # Register the amenities namespace
    api.add_namespace(amenities_ns, path='/amenities')

    # Register the places namespace
    api.add_namespace(places_ns, path='/places')

    # Register the reviews namespace
    api.add_namespace(reviews_ns, path='/reviews')

    # Register the auth namespace
    api.add_namespace(auth_ns, path='/auth')

    # Register the protected namespace
    api.add_namespace(protected_ns, path='/protected')

    @app.route("/")
    def home():
        return redirect(url_for('index'))


    @app.route("/index")
    def index():
        return render_template('index.html')
    
    @app.route("/login")
    def login():
        return render_template('login.html')
    
    @app.route("/place")
    def place():
        place_id = request.args.get('id')
        # get the place data
        place_api = 'http://localhost:5000/api/v1/places/' + place_id
        place_data = requests.get(place_api)
        place_data = place_data.json()
        # get the reviews 
        place_reviews_api = 'http://localhost:5000/api/v1/reviews/places/' + place_id + '/reviews'
        place_reviews = requests.get(place_reviews_api)
        if place_reviews:
            place_reviews = place_reviews.json()
        else:
            place_reviews = None
        return render_template('place.html', place_data = place_data, place_reviews = place_reviews)

    @app.route("/add_review")
    def add_review():
        place_id = request.args.get('id')
        place_data = {}
        if place_id:
            try:
                place_data = requests.get(f"http://localhost:5000/api/v1/places/{place_id}")
                place_data.raise_for_status()
                place_data = place_data.json()
            except requests.RequestException:
                 place_data = {}

        return render_template('add_review.html', place_data = place_data)

    return app
