from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db:SQLAlchemy = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.basic_authentication import auth
from app.routes import register_route, master_route, client_route
from app.models import user, client, request

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'user': user, 'client': client, 'request': request}



