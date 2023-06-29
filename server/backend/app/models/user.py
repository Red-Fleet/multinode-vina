import uuid
from app import db
import sqlalchemy as sqaly

class User(db.Model):
    """The user table stores information about registered users in the system. 
    Each entry represents a user with details such as the username, associated 
    client ID, name, and password hash.
    """
    # The unique identifier for the user.
    username = sqaly.Column(sqaly.String(256), primary_key=True)
    # The identifier of the associated client. Visible to other users. 
    # And is unique to a user (System generated).
    client_id = sqaly.Column(sqaly.String(36))
    # The name of the user. Visible to other users.
    name = sqaly.Column(sqaly.String(256), default="")
    # The hashed password for the user.
    password_hash = sqaly.Column(sqaly.String(128), default="")

    def __repr__(self):
        return '<User {}>'.format(self.username)