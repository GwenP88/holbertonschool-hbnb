from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model_create = api.model('ReviewCreate', {
    'comment': fields.String(required=True, description='Comment of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})

review_model_update = api.model('ReviewUpdate', {
    'comment': fields.String(required=False, description='Comment of the review'),
    'rating': fields.Integer(required=False, description='Rating of the place (1-5)'),
})


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model_create, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Place or User not found')
    @api.doc(security='Bearer')
    @jwt_required()
    def post(self):
        """Register a new review"""
        review_data = api.payload
        current_user = get_jwt_identity()
        review_data['author_id'] = current_user
        try:
            new_review = facade.create_review(review_data)
        except ValueError as e:
            if str(e) == "User not found." or str(e) == "Place not found.":
                return {'error': str(e)}, 404
            return {'error': str(e)}, 400
        return new_review.get_details(), 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        result = []
        for r in reviews:
            result.append(r.get_details())
        return result, 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review.get_details(), 200 

    @api.expect(review_model_update, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @api.doc(security='Bearer')
    @jwt_required()
    def put(self, review_id):
        payload = api.payload
        current_user = get_jwt_identity()
        claims = get_jwt()
        review = facade.review_repo.get(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        if review.author_id != current_user and not claims.get("is_admin"):
            return {'error': 'Unauthorized action'}, 403
        try:
            facade.update_review(review_id, payload)
        except ValueError as e:
            return {'error': str(e)}, 400
        review_details = facade.get_review(review_id)
        return review_details, 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    @api.doc(security='Bearer')
    @jwt_required()
    def delete(self, review_id):
        current_user = get_jwt_identity()
        claims = get_jwt()
        review = facade.review_repo.get(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        if review.author_id != current_user and not claims.get("is_admin"):
            return {'error': 'Unauthorized action'}, 403
        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully.'}, 200
