import enum
from app import db
import sqlalchemy as sqaly

class ClientState(enum.Enum):
        connected: str = "connected"
        idle: str = "idle"
        busy: str = "busy"
        computing: str = "computing"

class Client(db.Model):
    client_id = sqaly.Column(sqaly.String(36), primary_key=True)
    last_connected = sqaly.Column(sqaly.DateTime())
    state = sqaly.Column(sqaly.Enum(ClientState))

    def __repr__(self):
        return '<User {}>'.format(self.username)
