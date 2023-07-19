from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from app.models.server import Server
from app.models.user import User
from app.models.worker_connection import WorkerConnection
from flask_cors import CORS, cross_origin
import logging

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db:SQLAlchemy = SQLAlchemy(app)
migrate = Migrate(app, db)

# Set the log file path
log_file = '../logfile.log'

# Configure Flask logger to write to file
file_handler = logging.FileHandler(log_file)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

# stores address of server
server = Server()
# stores details of logined user
user = User()
# stores of current worker is connected to how many master
worker_connection = WorkerConnection()


from app.routes import home_route, server_route, user_route, master_connection_request_route
from app.routes import client_route, worker_connection_request_route, master_docking_route
from app.routes import chembl_route



from app.db_models import master_compute, master_compute_ligand, master_compute_target
# @app.shell_context_processor
# def make_shell_context():
#     return {'db': db, 'user': user, 'client': client, 'request': request}


# @app.before_first_request
# def startAutomatedServices():
#     from app.automates_services.automated_master_request_service import AutomatedMasterRequestService
#     AutomatedMasterRequestService.start()
#     print("this is running")