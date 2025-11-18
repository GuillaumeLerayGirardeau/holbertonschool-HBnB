from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        # Placeholder for the logic to register a new amenity
        try:
            amenity_data = api.payload
            existing_amenity = facade.get_all_amenities()
            for i in existing_amenity:
                if i.name == amenity_data['name']:
                    return {'error': 'Amenity already exist'}, 400
            new_amenity = facade.create_amenity(amenity_data)
            return {'id': new_amenity.id, 'name': new_amenity.name}, 201
        except Exception:
            return {"error": "Invalid input data"}, 400

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        # Placeholder for logic to return a list of all amenities
        all_amenity = facade.get_all_amenities()
        amenity_list = []
        for amenity in all_amenity:
            amenity_list.append({
                'id': amenity.id,
                'name': amenity.name
            })
        return amenity_list, 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        # Placeholder for the logic to retrieve an amenity by ID
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {'id': amenity.id, 'name': amenity.name}, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        # Placeholder for the logic to update an amenity by ID
        try:
            amenity_data = api.payload
            if not amenity_data["name"]:
                raise ValueError("Name must not be empty !")
            amenity = facade.get_amenity(amenity_id)
            if not amenity:
                return {'error': 'Amenity not found'}, 404
            facade.update_amenity(amenity_id, amenity_data)
            return {"message": "Amenity updated successfully"}, 200
        except Exception:
            return {"error": "Invalid input data"}, 400


@api.route('/admin')
class AdminUserResource(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        """Register a new amenity"""
        # Placeholder for the logic to register a new amenity
        try:
            admin = get_jwt()
            amenity_data = api.payload
            if not admin["is_admin"]:
                return {'error': 'Admin privileges required'}, 403
            existing_amenity = facade.get_all_amenities()
            for i in existing_amenity:
                if i.name == amenity_data['name']:
                    return {'error': 'Amenity already exist'}, 400
            new_amenity = facade.create_amenity(amenity_data)
            return {'id': new_amenity.id, 'name': new_amenity.name}, 201
        except Exception:
            return {"error": "Invalid input data"}, 400


@api.route('/<amenity_id>/admin')
class AdminAmenityModify(Resource):
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity's information"""
        # Placeholder for the logic to update an amenity by ID
        try:
            admin = get_jwt()
            if not admin["is_admin"]:
                return {'error': 'Admin privileges required'}, 403
            amenity_data = api.payload
            if not amenity_data["name"]:
                raise ValueError("Name must not be empty !")
            amenity = facade.get_amenity(amenity_id)
            if not amenity:
                return {'error': 'Amenity not found'}, 404
            facade.update_amenity(amenity_id, amenity_data)
            return {"message": "Amenity updated successfully"}, 200
        except Exception:
            return {"error": "Invalid input data"}, 400


    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def delete(self, amenity_id):
        """delete an amenity's information"""
        # Placeholder for the logic to delete an amenity by ID
        try:
            admin = get_jwt()
            if not admin["is_admin"]:
                return {'error': 'Admin privileges required'}, 403
            amenity = facade.get_amenity(amenity_id)
            if not amenity:
                return {'error': 'Amenity not found'}, 404
            facade.delete_amenity(amenity_id)
            return {"message": "Amenity deleted successfully"}, 200
        except Exception:
            return {"error": "Invalid input data"}, 400
