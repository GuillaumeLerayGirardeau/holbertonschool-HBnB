from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True,
                             description='Latitude of the place'),
    'longitude': fields.Float(required=True,
                              description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=False,
                             description="List of amenities ID's")
})


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Amenity not found')
    @jwt_required()
    def post(self):
        """Register a new place"""
        # Placeholder for the logic to register a new place
        try:
            current_user = get_jwt_identity()
            place_data = api.payload
            if not facade.get_user(place_data["owner_id"]):
                raise ValueError("User does not exist")
            if place_data["owner_id"] != current_user:
                return {'error': 'Unauthorized action'}, 403
            amenity_list = []
            if place_data["amenities"]:
                for name in place_data["amenities"]:
                    new_a = facade.get_amenity_by_name(name)
                    if not new_a:
                        return {'error': 'Amenity not found'}, 404
                    else:
                        amenity_list.append(new_a)
            place_data["amenities"] = amenity_list
            new_place = facade.create_place(place_data)
            new_place_amenities = []
            for i in new_place.amenities:
                new_place_amenities.append({
                    "id": i.id,
                    "name": i.name
                })
            return {
                'id': new_place.id,
                'title': new_place.title,
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'owner_id': new_place.owner_id,
                'amenities': new_place_amenities
            }, 201
        except Exception:
            return {"error": 'Invalid input data'}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        # Placeholder for logic to return a list of all places
        all_places = facade.get_all_places()
        place_list = []
        for i in all_places:
            place_list.append({
                "id": i.id,
                "title": i.title,
                "latitude": i.latitude,
                "longitude": i.longitude
            })
        return place_list, 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        # Placeholder for the logic to retrieve a place by ID
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        owner_data = facade.get_user(place.owner_id)
        amenities_list = []
        for i in place.amenities:
            amenities_list.append({
                "id": i.id,
                "name": i.name
            })
        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner": {
                "id": place.owner_id,
                "first_name": owner_data.first_name,
                "last_name": owner_data.last_name,
                "email": owner_data.email
            },
            "amenities": amenities_list
        }, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""
        # Placeholder for the logic to update a place by ID
        try:
            current_user = get_jwt_identity()
            place_data = api.payload
            if "title" in place_data:
                if not place_data["title"]:
                    return {"error": "Your place must have a title"}, 400
            if "description" in place_data:
                if not place_data["description"]:
                    return {"error": "Your place must have a description"}, 400
            if "price" in place_data:
                if place_data['price'] < 0:
                    return {"error": "Your place must cost at least 0€"}, 400
            if place_data["amenities"]:
                amenity_list = []
                for name in place_data["amenities"]:
                    new_a = facade.get_amenity_by_name(name)
                    if not new_a:
                        return {'error': 'Amenity not found'}, 404
                    else:
                        amenity_list.append(new_a)
                place_data["amenities"] = amenity_list
            place = facade.get_place(place_id)
            if not place:
                return {"error": "Place not found"}, 404
            if place.owner_id != current_user:
                return {'error': 'Unauthorized action'}, 403
            facade.update_place(place_id, place_data)
            return {"message": "Place updated successfully"}, 200
        except Exception:
            return {"error": "Invalid input data"}, 400


@api.route('/<place_id>/admin')
class AdminPlaceModify(Resource):
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""
        # Placeholder for the logic to update a place by ID
        try:
            admin = get_jwt()
            place_data = api.payload
            if not admin["is_admin"]:
                return {'error': 'Admin privileges required'}, 403
            if "title" in place_data:
                if not place_data["title"]:
                    return {"error": "Your place must have a title"}, 400
            if "description" in place_data:
                if not place_data["description"]:
                    return {"error": "Your place must have a description"}, 400
            if "price" in place_data:
                if place_data['price'] < 0:
                    return {"error": "Your place must cost at least 0€"}, 400
            if place_data["amenities"]:
                amenity_list = []
                for name in place_data["amenities"]:
                    new_a = facade.get_amenity_by_name(name)
                    if not new_a:
                        return {'error': 'Amenity not found'}, 404
                    else:
                        amenity_list.append(new_a)
                place_data["amenities"] = amenity_list
            place = facade.get_place(place_id)
            if not place:
                return {"error": "Place not found"}, 404
            facade.update_place(place_id, place_data)
            return {"message": "Place updated successfully"}, 200
        except Exception:
            return {"error": "Invalid input data"}, 400

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def delete(self, place_id):
        """delete a place's information"""
        # Placeholder for the logic to delete a place by ID
        try:
            admin = get_jwt()
            if not admin["is_admin"]:
                return {'error': 'Admin privileges required'}, 403
            place = facade.get_place(place_id)
            if not place:
                return {"error": "Place not found"}, 404
            facade.delete_place(place_id)
            return {"message": "Place deleted successfully"}, 200
        except Exception:
            return {"error": "Invalid input data"}, 400
