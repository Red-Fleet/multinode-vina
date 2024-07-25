from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import logging

app = Flask(__name__)
app.config.from_object(Config)

db:SQLAlchemy = SQLAlchemy(app)
migrate = Migrate(app, db)

# # Set the log file path
log_file = 'logfile.log'

# Configure Flask logger to write to file
file_handler = logging.FileHandler(log_file)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

from app.basic_authentication import auth
from app.routes import request_route, user_route, client_route, compute_route, notification_route, docking_route
from app.models import user, client, request, notification, compute, docking, ligands

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'user': user, 'client': client, 'request': request}


# Initialize Services
from app.services.docking_service import DockingService

with app.app_context():
    DockingService.initDockingService()

