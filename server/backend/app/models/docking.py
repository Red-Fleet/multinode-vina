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
    CREATED: str = "CREATED"
    STARTED: str = "STARTED"
    FINISHED: str = "FINISHED"
    ERROR: str = "ERROR"

class Docking(db.Model):
    docking_id = sqaly.Column(sqaly.String(36), primary_key=True)
    master_id = sqaly.Column(sqaly.String(36), nullable=False, index=True)
    worker_ids = sqaly.Column(ListType) # array of worker_ids
    target = sqaly.Column(sqaly.TEXT())
    target_name = sqaly.Column(sqaly.String(1000))
    compute_ids = sqaly.Column(ListType) # array of ligand_ids
    ligands_name = sqaly.Column(sqaly.String(1000))
    last_updated = sqaly.Column(sqaly.DateTime())
    state = sqaly.Column(sqaly.Enum(DockingState))