import enum
from app import db
import sqlalchemy as sqaly

class ClientState(enum.Enum):
    CONNECTED: str = "CONNECTED"
    IDLE: str = "IDLE"
    BUSY: str = "BUSY"
    COMPUTING: str = "COMPUTING"

class Client(db.Model):
    client_id = sqaly.Column(sqaly.String(36), primary_key=True)
    last_connected = sqaly.Column(sqaly.DateTime())
    state = sqaly.Column(sqaly.Enum(ClientState))

    def __repr__(self):
        return '<client_id {}>'.format(self.client_id)
