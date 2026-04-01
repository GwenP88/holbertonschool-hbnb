from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('AmenityCreate', {
    'name': fields.String(required=True, description='Name of the amenity'),
    'description': fields.String(required=False, description='Name of the amenity')
})

amenity_model_update = api.model('AmenityUpdate', {
    'name': fields.String(required=False, description='Name of the amenity'),
    'description': fields.String(required=False, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @api.doc(security='Bearer')
    @jwt_required()
    def post(self):
        """Create a new amenity"""
        claims = get_jwt()
        if not claims.get("is_admin"):
            return {'error': 'Admin privileges required'}, 403
        amenity_data = api.payload
        try:
            new_amenity = facade.create_amenity(amenity_data)
        except ValueError as e:
            return {'error': str(e)}, 400
        return {'id': new_amenity.id, 'name': new_amenity.name, 'description': new_amenity.description}, 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        list_amenities = []
        for amenity in amenities:
            list_amenities.append({'id': amenity.id, 'name': amenity.name, 'description': amenity.description})
        return list_amenities, 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {'id': amenity.id, 'name': amenity.name, 'description': amenity.description}, 200

    @api.expect(amenity_model_update, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @api.doc(security='Bearer')
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity's information"""
        claims = get_jwt()
        if not claims.get("is_admin"):
            return {'error': 'Admin privileges required'}, 403
        payload = api.payload
        try:
            amenity = facade.update_amenity(amenity_id, payload)
        except ValueError as e:
            return {'error': str(e)}, 400
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {'id': amenity.id, 'name': amenity.name, 'description': amenity.description}, 200
    
    @api.response(200, 'Amenity deleted successfully')
    @api.response(404, 'Amenity not found')
    @api.response(403, 'Admin privileges required')
    @api.doc(security='Bearer')
    @jwt_required()
    def delete(self, amenity_id):
        """Delete an amenity"""
        claims = get_jwt()
        amenity = facade.amenity_repo.get(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        if not claims.get("is_admin"):
            return {'error': 'Admin privileges required'}, 403
        facade.delete_amenity(amenity_id)
        return {'message': 'Amenity deleted successfully.'}, 200
