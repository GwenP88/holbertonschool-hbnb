from flask_restx import Namespace, Resource, fields
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
    def post(self):
        amenity_data = api.payload
        try:
            new_amenity = facade.create_amenity(amenity_data)
        except ValueError as e: 
            return {'error': str(e)}, 400
        return {'id': new_amenity.id, 'name': new_amenity.name, 'description': new_amenity.description}, 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
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
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {'id': amenity.id, 'name': amenity.name, 'description': amenity.description}, 200

    @api.expect(amenity_model_update, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        payload = api.payload
        try :
            amenity = facade.update_amenity(amenity_id, payload)
        except ValueError as e:
            return {'error': str(e)}, 400
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {'id': amenity.id, 'name': amenity.name, 'description': amenity.description}, 200