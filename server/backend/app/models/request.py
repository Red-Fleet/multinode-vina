import enum
from app import db
import sqlalchemy as sqaly


class RequestState(enum.Enum):
    # new request is created by master
    CREATED: str = "CREATED"
    # request is accepted by worker
    ACCEPTED: str = "ACCEPTED"
    # request is rejected by worker
    REJECTED: str = "REJECTED"


class Request(db.Model):
    master_id = sqaly.Column(sqaly.String(36),  primary_key=True)
    worker_id = sqaly.Column(sqaly.String(36), index=True, primary_key=True)
    state_update_time = sqaly.Column(sqaly.DateTime(), nullable=False)
    state = sqaly.Column(sqaly.Enum(RequestState))

    def __repr__(self):
        return '<Request master:{}, worker:{}, state:{}, update_time:{}>'.format(self.master_id, 
                                                                    self.worker_id, 
                                                                    self.state, 
                                                                    self.state_update_time)
