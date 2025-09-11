import os
from flask import Flask
from dotenv import load_dotenv
from models import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///dev.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret')

    db.init_app(app)
    Migrate(app, db)
    JWTManager(app)
    CORS(app)

    from auth import auth_bp
    from api import api_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(api_bp, url_prefix='/api')
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=True)