import enum
from app import db
import sqlalchemy as sqaly

class ClientStateException(Exception):
    pass

class ClientState(enum.Enum):
    OFFLINE: str = "OFFLINE"
    ONLINE: str = "ONLINE"
    IDLE: str = "IDLE"
    BUSY: str = "BUSY"

    @staticmethod
    def fromStr(state_str):
        if state_str == "OFFLINE": return ClientState.OFFLINE
        elif state_str == "ONLINE": return ClientState.ONLINE
        elif state_str == "IDLE": return ClientState.IDLE
        elif state_str == "BUSY": return ClientState.BUSY
        else:
            raise ClientStateException("State not avaliable. Avaliable states :" +str([e.value for e in ClientState]))

class Client(db.Model):
    client_id = sqaly.Column(sqaly.String(36), primary_key=True)
    last_connected = sqaly.Column(sqaly.DateTime())
    state = sqaly.Column(sqaly.Enum(ClientState))

    def __repr__(self):
        return '<client_id {}>'.format(self.client_id)
