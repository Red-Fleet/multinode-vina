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
    """Master uses this table to connect with new workers. 
    A new entry is created when the master sends a new connection request to the 
    client, and then the client can reject or accept master’s connection request.
    """
    # The unique identifier of the master who initiated the request. 
    # Indexed for faster retrieval.(After adding persistent storage in the client, 
    # the index on master_id will be removed)
    master_id = sqaly.Column(sqaly.String(36), index=True, primary_key=True)
    # The unique identifier of the worker associated with the request. 
    # Indexed for faster retrieval.
    worker_id = sqaly.Column(sqaly.String(36), index=True, primary_key=True)
    #  The timestamp indicating when the state of the request was last updated.
    state_update_time = sqaly.Column(sqaly.DateTime(), nullable=False)
    # The current state of the request. 
    state = sqaly.Column(sqaly.Enum(RequestState))

    def __repr__(self):
        return '<Request master:{}, worker:{}, state:{}, update_time:{}>'.format(self.master_id, 
                                                                    self.worker_id, 
                                                                    self.state, 
                                                                    self.state_update_time)
