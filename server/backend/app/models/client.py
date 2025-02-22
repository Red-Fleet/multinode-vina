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
    """The client table stores information about clients registered in the system. 
    Each entry represents a client with details such as the client ID, last connected 
    timestamp, and state. There is one to one relationship between user and client. 
    Details of this table can be viewed by all users.
    """
    # The unique identifier for the client.
    client_id = sqaly.Column(sqaly.String(36), primary_key=True)
    
    # The datetime when the client was last connected. For determining state of client.
    last_connected = sqaly.Column(sqaly.DateTime())
    # The current state of the client.
    state = sqaly.Column(sqaly.Enum(ClientState))

    
    def __repr__(self):
        return '<client_id {}>'.format(self.client_id)
