from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(
        required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(404, 'Owner not found')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new review"""
        try:
            print("token")
            current_user = get_jwt_identity()
            data = api.payload
            print("user found")
            if not facade.get_user(data["user_id"]):
                return {"error": "User not found"}, 404
            print("place found")
            if not facade.get_place(data["place_id"]):
                return {"error": "Place not found"}, 404
            print("token is not the user")
            if data["user_id"] != current_user:
                return {'error': 'Unauthorized action.'}, 403
            print("user is owner")
            current_place = facade.get_place(data["place_id"])
            print("have the place id")
            print(current_place)
            print(current_place.owner_id)
            if current_place.owner_id == current_user:
                return {
                    'error': 'You cannot review your own place.'
                }, 403
            print("by place")
            all_reviews = facade.get_reviews_by_place(current_place.id)
            for review in all_reviews:
                if review.user_id == current_user:
                    return {
                        'error': 'You have already reviewed this place.'
                    }, 403
            print("All ok")
            review = facade.create_review(data)
            return {
                "id": review.id,
                "text": review.text,
                "rating": review.rating,
                "user_id": review.user_id,
                "place_id": review.place_id
            }, 201
        except Exception as e:
            return {"error": e}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [
            {
                "id": r.id,
                "text": r.text,
                "rating": r.rating,
            }
            for r in reviews
        ], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review_obj = facade.get_review(review_id)
        if not review_obj:
            return {"error": "Review not found"}, 404

        return {
            "id": review_obj.id,
            "text": review_obj.text,
            "rating": review_obj.rating,
            "user_id": review_obj.user_id,
            "place_id": review_obj.place_id
        }, 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        try:
            current_user = get_jwt_identity()
            data = api.payload
            if "rating" in data:
                if data["rating"] < 1 or data["rating"] > 5:
                    return {"error": "Rating must be between 1 and 5 !"}, 400
            review_obj = facade.get_review(review_id)
            if not review_obj:
                return {"error": "Review not found"}, 404
            if review_obj.user_id != current_user:
                return {"error": "Unauthorized action."}, 403
            facade.update_review(review_id, data)
            return {"message": "Review updated successfully"}, 200
        except Exception:
            return {"error": "Invalid input data"}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        current_user = get_jwt_identity()
        review_obj = facade.get_review(review_id)
        if not review_obj:
            return {"error": "Review not found"}, 404
        if review_obj.user_id != current_user:
            return {"error": "Unauthorized action."}, 403
        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200


@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            reviews = facade.get_reviews_by_place(place_id)
        except Exception:
            return {"error": "Place not found"}, 404

        return [
            {
                "id": r.id,
                "text": r.text,
                "rating": r.rating
            }
            for r in reviews
        ], 200


@api.route('/<review_id>/admin')
class AdminReviewModify(Resource):
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        try:
            admin = get_jwt()
            data = api.payload
            if not admin["is_admin"]:
                return {'error': 'Admin privileges required'}, 403
            if "rating" in data:
                if data["rating"] < 1 or data["rating"] > 5:
                    return {"error": "Rating must be between 1 and 5 !"}, 400
            review_obj = facade.get_review(review_id)
            if not review_obj:
                return {"error": "Review not found"}, 404
            facade.update_review(review_id, data)
            return {"message": "Review updated successfully"}, 200
        except Exception:
            return {"error": "Invalid input data"}, 400

    @api.expect(review_model)
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        admin = get_jwt()
        if not admin["is_admin"]:
            return {'error': 'Admin privileges required'}, 403
        review_obj = facade.get_review(review_id)
        if not review_obj:
            return {"error": "Review not found"}, 404
        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200
