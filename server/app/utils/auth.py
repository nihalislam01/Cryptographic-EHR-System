from functools import wraps
from flask import request, jsonify
from app.utils.jwtHelper import verify_token
from app.models.user import User

def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'message': 'Missing or invalid token'}), 401

        token = auth_header.split(" ")[1]
        user_id = verify_token(token)

        if not user_id:
            return jsonify({'message': 'Token is invalid or expired'}), 401

        return f(user_id=user_id, *args, **kwargs)
    return decorated_function

def authorized(allowed_roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({'message': 'Missing or invalid token'}), 401

            token = auth_header.split(" ")[1]
            user_id = verify_token(token)

            if not user_id:
                return jsonify({'message': 'Invalid or expired token'}), 401

            user = User.query.get(user_id)
            if not user or user.role not in allowed_roles:
                return jsonify({'message': 'Unauthorized'}), 403

            return f(user_id=user_id, *args, **kwargs)
        return wrapper
    return decorator
