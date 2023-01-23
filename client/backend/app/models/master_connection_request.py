import enum
from app import db
import sqlalchemy as sqaly

class MasterConnectionRequestStateException(Exception):
    pass

class MasterConnectionRequestState(enum.Enum):
    CREATED: str = "CREATED"
    ACCEPTED: str = "ACCEPTED"
    REJECTED: str = "REJECTED"

    @staticmethod
    def fromString(str_state):
        if str_state == "CREATED": return MasterConnectionRequestState.CREATED
        elif str_state == "ACCEPTED": return MasterConnectionRequestState.ACCEPTED
        elif str_state == "REJECTED": return MasterConnectionRequestState.REJECTED
        else: raise MasterConnectionRequestStateException("MasterRequestState: State not avaliable")

class MasterConnectionRequest(db.Model):
    """this table will store the nodes to with current(logined) client is or will be connected

    Columns:
        client_id = current(logined) client
        worker_id = client to which connection request is send
        create_time = request creation time
        request_state = state of request
    """
    __tablename__ = "master_connection_request"
    id = sqaly.Column(sqaly.Integer, primary_key=True, autoincrement=True)
    client_id = sqaly.Column(sqaly.String(36), index=True)
    worker_id = sqaly.Column(sqaly.String(36))
    create_time = sqaly.Column(sqaly.DateTime(), nullable=False)
    request_state = sqaly.Column(sqaly.Enum(MasterConnectionRequestState))



class MasterConnectionRequestDto:
    def __init__(self, id=None, client_id=None, worker_id=None, create_time=None, request_state=None) -> None:
        self.id = id
        self.client_id = client_id
        self.worker_id = worker_id
        self.create_time = create_time
        self.request_state = request_state

        pass

    @staticmethod
    def getDtoFromModel(model: MasterConnectionRequest):
        return MasterConnectionRequestDto(id=model.id, 
            client_id=model.client_id, 
            worker_id=model.worker_id,
            create_time=model.create_time,
            request_state=model.request_state
            )