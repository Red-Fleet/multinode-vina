import enum
from app import db
import sqlalchemy as sqaly


class RequestState(enum.Enum):
    CREATED: str = "CREATED"
    ACCEPTED: str = "ACCEPTED"
    REJECTED: str = "REJECTED"


class Request(db.Model):
    request_to = sqaly.Column(sqaly.String(36), primary_key=True)
    request_from = sqaly.Column(sqaly.String(36), primary_key=True)
    state_update_time = sqaly.Column(sqaly.DateTime(), nullable=False)
    state = sqaly.Column(sqaly.Enum(RequestState))

    def __repr__(self):
        return '<Request to:{}, from:{}, state:{}, update_time:{}>'.format(self.request_to, 
                                                                    self.request_from, 
                                                                    self.state, 
                                                                    self.state_update_time)
