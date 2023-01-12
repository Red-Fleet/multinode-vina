from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from app.models.server import Server
from app.models.user import User

app = Flask(__name__)
app.config.from_object(Config)
server = Server()
user = User()

#db:SQLAlchemy = SQLAlchemy(app)
#migrate = Migrate(app, db)

from app.routes import home_route, server_route, user_route

# @app.shell_context_processor
# def make_shell_context():
#     return {'db': db, 'user': user, 'client': client, 'request': request}



