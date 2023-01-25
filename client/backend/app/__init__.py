from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from app.models.server import Server
from app.models.user import User
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db:SQLAlchemy = SQLAlchemy(app)
migrate = Migrate(app, db)

server = Server()
user = User()
db:SQLAlchemy = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.routes import home_route, server_route, user_route, master_connection_request_route
# @app.shell_context_processor
# def make_shell_context():
#     return {'db': db, 'user': user, 'client': client, 'request': request}


# @app.before_first_request
# def startAutomatedServices():
#     from app.automates_services.automated_master_request_service import AutomatedMasterRequestService
#     AutomatedMasterRequestService.start()
#     print("this is running")