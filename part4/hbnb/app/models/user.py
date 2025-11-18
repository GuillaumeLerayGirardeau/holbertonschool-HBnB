#!/usr/bin/python3
from app import db, bcrypt
from app.models.base_class import basemodel
from email_validator import validate_email, EmailNotValidError


class User(basemodel):

    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    place_owned = db.relationship(
        'Place', backref='owner', lazy=True, cascade='all, delete')
    reviews = db.relationship(
        'Review', backref='user', lazy=True, cascade='all, delete')

    def __init__(self, first_name, last_name, email, password,
                 is_admin=False):
        super().__init__()
        if not first_name or not last_name or not email or not password:
            raise ValueError("Empty value !")
        if not validate_email(email):
            raise EmailNotValidError("Incorrect email !")
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.hash_password(password)
        self.is_admin = is_admin
        self.places = []
        self.reviews = []

    def add_places(self, place):
        self.places.append(place)

    def add_reviews(self, review):
        self.reviews.append(review)

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
