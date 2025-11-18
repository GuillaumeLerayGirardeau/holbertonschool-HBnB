#!/usr/bin/python3
from app.models.base_class import basemodel
from app import db
from app.models.association_tables import place_amenity


class Amenity(basemodel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)
    place_data = db.relationship(
        'Place', secondary=place_amenity,
        lazy='subquery', backref=db.backref('amenity', lazy=True))

    def __init__(self, name):
        super().__init__()
        if not name:
            raise ValueError("Name must not be empty !")
        self.name = name
        self.places = []

    def add_place(self, place):
        self.places.append(place)
