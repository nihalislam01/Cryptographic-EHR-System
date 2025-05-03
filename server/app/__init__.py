from flask import Flask
from app.routes.authRoute import auth_bp
from app.models.user import db;
from app.controllers.authController import bcrypt
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config')

    CORS(app)
    db.init_app(app)
    bcrypt.init_app(app)
    
    with app.app_context():
        db.create_all()

    app.register_blueprint(auth_bp)

    return app
