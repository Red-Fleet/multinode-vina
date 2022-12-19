import enum
from app import db
import sqlalchemy as sqaly

class RequestState(enum.Enum):
    CREATED: str = "CREATED"
    ACCEPTED: str = "ACCEPTED"
    DECLINED: str = "DECLINED"

class Request(db.Model):
    request_to = sqaly.Column(sqaly.String(36), primary_key=True)
    request_from = sqaly.Column(sqaly.String(36), primary_key=True)
    last_connected = sqaly.Column(sqaly.DateTime())
    state = sqaly.Column(sqaly.Enum(RequestState))
