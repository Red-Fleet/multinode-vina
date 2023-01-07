import enum
from app import db
import sqlalchemy as sqaly

class ComputeState(enum.Enum):
    CREATED: str = "CREATED"
    STARTED: str = "STARTED"
    FINISHED: str = "FINISHED"
    ERROR: str = "ERROR"

class Compute(db.Model):
    compute_id = sqaly.Column(sqaly.String(36), primary_key=True)
    worker_id = sqaly.Column(sqaly.String(36), nullable=False)
    master_id = sqaly.Column(sqaly.String(36), nullable=False)
    target = sqaly.Column(sqaly.BLOB())
    ligands = sqaly.Column(sqaly.BLOB())
    result = sqaly.Column(sqaly.BLOB())
    last_updated = sqaly.Column(sqaly.DateTime())
    state = sqaly.Column(sqaly.Enum(ComputeState))
    error = sqaly.Column(sqaly.String(1000))


    