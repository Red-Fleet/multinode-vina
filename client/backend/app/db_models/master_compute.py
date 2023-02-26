import enum
from app import db
import sqlalchemy as sqaly

class MasterComputeState(enum.Enum):
    CREATED: str = "CREATED"
    STARTED: str = "STARTED"
    FINISHED: str = "FINISHED"
    ERROR: str = "ERROR"

class MasterCompute(db.Model):
    # id of target to which current computation is associated with
    target_id = sqaly.Column(sqaly.Integer, index=True)
    # id of lignad to which current computation is associated with
    ligand_id = sqaly.Column(sqaly.Integer)

    compute_id = sqaly.Column(sqaly.String(36), primary_key=True)
    worker_id = sqaly.Column(sqaly.String(36), nullable=False)
    master_id = sqaly.Column(sqaly.String(36), nullable=False)
    target = sqaly.Column(sqaly.TEXT())
    target_name = sqaly.Column(sqaly.String(1000))
    ligands = sqaly.Column(sqaly.TEXT())
    ligands_name = sqaly.Column(sqaly.String(1000))
    result = sqaly.Column(sqaly.TEXT())
    last_updated = sqaly.Column(sqaly.DateTime())
    state = sqaly.Column(sqaly.Enum(MasterComputeState))
    error = sqaly.Column(sqaly.TEXT())


    