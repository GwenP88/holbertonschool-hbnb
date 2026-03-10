from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('users', description='User operations')

user_model = api.model('UserCreate', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(required=False, description='First name of the user'),
    'last_name': fields.String(required=False, description='Last name of the user')
})

user_update_model_email = api.model('UserUpdateEmail', {
    'email': fields.String(required=True, description='Email of the user'),
})

user_update_model_password = api.model('UserUpdatePassword', {
    'password': fields.String(required=True, description='Password of the user'),
})


@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        user_data = api.payload
        try:
            new_user = facade.create_user(user_data)
        except ValueError as e:
            return {'error': str(e)}, 400
        return {'id': new_user.id, 'first_name': new_user.first_name, 'last_name': new_user.last_name, 'email': new_user.email}, 201

    @api.response(200, 'Users retrieved successfully')
    def get(self):
        users = facade.get_users()
        list_users = []
        for user in users:
            list_users.append({'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email})
        return list_users, 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User details updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @api.doc(security='Bearer')
    @jwt_required()
    def put(self, user_id):
        payload = api.payload
        current_user = get_jwt_identity()
        if user_id != current_user:
            return {'error': 'Unauthorized action'}, 403
        if "email" in payload or "password" in payload:
            return {'error': 'You cannot modify email or password.'}, 400
        try:
            user = facade.update_user(user_id, payload)
        except ValueError as e:
            return {'error': str(e)}, 400
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name}, 200

@api.route('/<user_id>/email')
class UserEmailResource(Resource):
    @api.expect(user_update_model_email, validate=True)
    @api.response(200, 'User email updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @api.doc(security='Bearer')
    @jwt_required()
    def put(self, user_id):
        payload = api.payload
        current_user = get_jwt_identity()
        if user_id != current_user:
            return {'error': 'Unauthorized action'}, 403
        try:
            user = facade.update_user_email(user_id, payload)
        except ValueError as e:
            return {'error': str(e)}, 400
        if not user:
            return {'error': 'User not found'}, 404
        return {'message': 'Email updated successfully', 'email': user.email}, 200

@api.route('/<user_id>/password')
class UserPasswordResource(Resource):
    @api.expect(user_update_model_password, validate=True)
    @api.response(200, 'User password updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @api.doc(security='Bearer')
    @jwt_required()
    def put(self, user_id):
        payload = api.payload
        current_user = get_jwt_identity()
        if user_id != current_user:
            return {'error': 'Unauthorized action'}, 403
        try:
            user = facade.update_user_password(user_id, payload)
        except ValueError as e:
            return {'error': str(e)}, 400
        if not user:
            return {'error': 'User not found'}, 404
        return {'message': 'Password updated successfully'}, 200