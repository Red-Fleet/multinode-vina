from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app_config import AppConfig
import logging

app = Flask(__name__)
app.config.from_object(AppConfig)

db:SQLAlchemy = SQLAlchemy(app)
migrate = Migrate(app, db)

# # Set the log file path
log_file = 'logfile.log'

# Configure Flask logger to write to file
file_handler = logging.FileHandler(log_file)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

from app.basic_authentication import auth
from app.routes import user_route, client_route, notification_route, docking_route
from app.models import client, notification, compute, docking, ligands


