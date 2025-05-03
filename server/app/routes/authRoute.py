from flask import Blueprint
from app.controllers.authController import register, login, check_status

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

auth_bp.route('/register', methods=['POST'])(register)
auth_bp.route('/login', methods=['POST'])(login)
auth_bp.route('/status', methods=['GET'])(check_status)
