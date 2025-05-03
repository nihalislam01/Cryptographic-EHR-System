from functools import wraps
from flask import request, jsonify
from app.utils.jwt_helper import verify_token

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
