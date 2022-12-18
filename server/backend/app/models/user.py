import uuid
from app import db
import sqlalchemy as sqaly

class User(db.Model):
    client_id = sqaly.Column(sqaly.String(36), primary_key=True)
    username = sqaly.Column(sqaly.String(256), index=True, unique=True)
    name = sqaly.Column(sqaly.String(256), default="")
    password_hash = sqaly.Column(sqaly.String(128), default="")

    def __repr__(self):
        return '<User {}>'.format(self.username)