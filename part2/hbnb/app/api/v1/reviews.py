from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model_create = api.model('ReviewCreate', {
    'comment': fields.String(required=True, description='Comment of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'author_id': fields.String(required=True, description='ID of the author'),
    'place_id': fields.String(required=True, description='ID of the place')
})

review_model_update = api.model('ReviewUpdate', {
    'comment': fields.String(required=False, description='Comment of the review'),
    'rating': fields.Integer(required=False, description='Rating of the place (1-5)'),
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model_create)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Place or User not found')
    def post(self):
        """Register a new review"""
        review_data = api.payload
        try:
            new_review = facade.create_review(review_data)
        except ValueError as e:
            if str(e) == "User not found.":
                return {'error': str(e)}, 404
            return {'error': str(e)}, 400
        if new_review is None:
            return {'error': 'Place not found'}, 404
        return new_review.get_details(), 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return reviews, 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review, 200
        
    @api.expect(review_model_update)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        payload = api.payload
        try:
            review = facade.update_review(review_id, payload)
        except ValueError as e:
            return {'error': str(e)}, 400

        if not review:
            return {'error': 'Review not found'}, 404

        review_details = facade.get_review(review_id)
        return review_details, 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        review = facade.delete_review(review_id)
        if review is None:
            return {'error': 'Review not found'}, 404
        return {'message': 'Review deleted successfully.'}, 200