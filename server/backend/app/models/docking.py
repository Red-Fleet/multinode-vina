import enum
from app import db
import sqlalchemy as sqaly
from flask import json

class ListType(sqaly.TypeDecorator):
    # Custom data type that serializes and deserializes lists as strings
    impl = sqaly.TEXT

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value
    
    def cache_key(self, **kw):
        return self.impl.cache_key(**kw)

    # Set cache_ok to True to silence the warning
    cache_ok = True

class DockingState(enum.Enum):
    STARTED: str = "STARTED"
    FINISHED: str = "FINISHED"
    ERROR: str = "ERROR"

class Docking(db.Model):
    """The docking table stores docking information in the system. 
    Each entry represents a docking request initiated by the master. 
    It stores target pdbqt, worker’s ids and stores other information 
    which are important for docking like grid box, spacing etc.  

    """
    #  The unique identifier of the docking request.
    docking_id = sqaly.Column(sqaly.String(36), primary_key=True)
    # The unique identifier of the master who initiated the docking request. 
    # (Note: The master_id column is currently indexed for faster retrieval. 
    # However, after adding persistent storage in the client, the index on 
    # master_id will be removed.)
    master_id = sqaly.Column(sqaly.String(36), nullable=False, index=True)
    # An array of worker IDs that are going to perform docking.
    worker_ids = sqaly.Column(ListType)
    # The target information, in PDBQT format, for the docking process.
    target = sqaly.Column(sqaly.TEXT())
    # The name or description of the target for the docking process.
    target_name = sqaly.Column(sqaly.String(1000))
    #compute_ids = sqaly.Column(ListType) # array of ligand_ids # have to remove this
    # The datetime when the docking request was last updated. Used for database cleanup.
    last_updated = sqaly.Column(sqaly.DateTime())
    # The state of the docking request ("STARTED", "FINISHED", "ERROR").
    state = sqaly.Column(sqaly.Enum(DockingState))
    # Additional parameters related to the docking request stored as 
    # JSON data like grid box, spacing etc.
    params = sqaly.Column(sqaly.JSON) # for storing parameters
    # for saving error, will store key as worker_id and error as value
    error = sqaly.Column(sqaly.JSON)