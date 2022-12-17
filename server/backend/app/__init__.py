from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db:SQLAlchemy = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.routes import register_route, login_route
from app.models import user, client