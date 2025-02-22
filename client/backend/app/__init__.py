from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from app_config import AppConfig
from flask_cors import CORS, cross_origin
import logging
from config import UserConfig
from app.models.connect import Connect

app = Flask(__name__)
app.config.from_object(AppConfig)
CORS(app)
# db:SQLAlchemy = SQLAlchemy(app)
# migrate = Migrate(app, db)


if UserConfig.LOGGING == True:
    # Configure Flask logger to write to file
    file_handler = logging.FileHandler(UserConfig.LOG_PATH)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    # app.logger.setLevel(logging.ERROR)


connection = Connect() # stores connection information and stores it



from app.routes import server_route, user_route
from app.routes import client_route, master_docking_route
from app.routes import chembl_route

from app.routes import home_route # should be imported last from routes

# @app.shell_context_processor
# def make_shell_context():
#     return {'db': db, 'user': user, 'client': client, 'request': request}


# @app.before_first_request
# def startAutomatedServices():
#     from app.automates_services.automated_master_request_service import AutomatedMasterRequestService
#     AutomatedMasterRequestService.start()
#     print("this is running")


    