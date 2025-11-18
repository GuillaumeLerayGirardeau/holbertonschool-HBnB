#!/usr/bin/python3
from app.models.base_class import basemodel
from app import db
from app.models.association_tables import place_amenity


class Place(basemodel):
    __tablename__ = 'places'

    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(128), nullable=False)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, default=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    owner_data = db.relationship('User', backref='places', lazy=True)
    reviews = db.relationship(
        'Review', backref='place', lazy=True, cascade='all, delete')
    amenities = db.relationship(
        'Amenity', secondary=place_amenity,
        lazy='subquery', backref=db.backref('place', lazy=True))


    def __init__(self, title, description, price,
                 latitude, longitude, owner_id, amenities):
        super().__init__()
        if not title or not description or not owner_id:
            raise ValueError("Some fields are empty !")
        self.title = title
        self.description = description
        if price < 0:
            raise ValueError("Your place must cost at least 0€")
        self.price = price
        if latitude < -90 or latitude > 90:
            raise ValueError(
                "The latitude or your place must be between -90 and 90"
            )
        self.latitude = latitude
        if longitude < -180 or longitude > 180:
            raise ValueError(
                "The longitude of your place must be between -180 and 180"
            )
        self.longitude = longitude
        self.owner_id = owner_id
        self.amenities = amenities
        self.reviews = []  # List to store related reviews

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)
