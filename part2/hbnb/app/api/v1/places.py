from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity'),
    'description': fields.String(description='Details of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'comment': fields.String(description='Comment of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'author_id': fields.String(description='ID of the author')
})

# Define the place model for input validation and documentation
place_model_create = api.model('PlaceCreate', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(required=True, description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=False, description='List of amenity IDs')
})

place_model_details = api.model('PlaceDetails', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews'),
    'created_at': fields.String(description='Creation datetime (ISO8601)'),
    'updated_at': fields.String(description='Last update datetime (ISO8601)'),
})

place_model_update = api.model('PlaceUpdate', {
    'title': fields.String(required=False, description='Title of the place'),
    'description': fields.String(required=False, description='Description of the place'),
    'price': fields.Float(required=False, description='Price per night'),
    'latitude': fields.Float(required=False, description='Latitude of the place'),
    'longitude': fields.Float(required=False, description='Longitude of the place'),
})

place_model_summary = api.model('PlaceSummary', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(description='Title of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place'),
})


@api.route('/')
class PlaceList(Resource):

    @api.expect(place_model_create, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        place_data = api.payload
        try:
            new_place = facade.create_place(place_data)
            place_details = facade.get_place(new_place.id)
        except ValueError as e:
            return {'error': str(e)}, 400

        return place_details, 201

    @api.marshal_list_with(place_model_summary)
    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return places, 200

@api.route('/<place_id>')
class PlaceResource(Resource):

    @api.marshal_with(place_model_details)
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place, 200


    @api.expect(place_model_update, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        payload = api.payload
        try:
            place = facade.update_place(place_id, payload)
        except ValueError as e:
            return {'error': str(e)}, 400

        if not place:
            return {'error': 'Place not found'}, 404

        place_details = facade.get_place(place_id)
        return place_details, 200
    
@api.route('/<place_id>/amenities/<amenity_id>')
class PlaceAmenityResource(Resource):

    @api.response(200, 'Amenity added successfully')
    @api.response(404, 'Place or Amenity not found')
    @api.response(400, 'Invalid operation')
    def post(self, place_id, amenity_id):
        """Add an amenity to a place"""
        try:
            place = facade.add_amenity_to_place(place_id, amenity_id)
        except ValueError as e:
            if str(e) == "Amenity not found.":
                return {'error': str(e)}, 404
            return {'error': str(e)}, 400

        if not place:
            return {'error': 'Place not found'}, 404

        place_details = facade.get_place(place_id)
        return place_details, 200


    @api.response(200, 'Amenity removed successfully')
    @api.response(404, 'Place or Amenity not found')
    @api.response(400, 'Invalid operation')
    def delete(self, place_id, amenity_id):
        """Remove an amenity from a place"""
        try:
            place = facade.remove_amenity_from_place(place_id, amenity_id)
        except ValueError as e:
            if str(e) == "Amenity not found.":
                return {'error': str(e)}, 404
            return {'error': str(e)}, 400

        if not place:
            return {'error': 'Place not found'}, 404

        place_details = facade.get_place(place_id)
        return place_details, 200

@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        reviews = facade.get_reviews_by_place(place_id)
        if reviews is None:
            return {'error': 'Place not found'}, 404
        return reviews, 200