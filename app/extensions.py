from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

api = Api()
cors = CORS()
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
