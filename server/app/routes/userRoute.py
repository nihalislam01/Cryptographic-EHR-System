from flask import Blueprint
from app.controllers.userController import get_all_patients

user_bp = Blueprint('user', __name__, url_prefix='/api/user')

user_bp.route('/get', methods=['GET'])(get_all_patients)
