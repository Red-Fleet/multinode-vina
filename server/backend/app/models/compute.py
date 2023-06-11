import enum
from app import db
import sqlalchemy as sqaly

class ComputeState(enum.Enum):
    COMPUTED: str = "COMPUTED"
    NOT_COMPUTED: str = "NOT_COMPUTED"
    COMPUTING: str = "COMPUTING"
    ERROR: str = "ERROR"

class Compute(db.Model):
    compute_id = sqaly.Column(sqaly.String(36), primary_key=True)
    # worker_id = sqaly.Column(sqaly.String(36), nullable=True)
    # master_id = sqaly.Column(sqaly.String(36), nullable=True)
    docking_id = sqaly.Column(sqaly.String(36), index=True)
    result = sqaly.Column(sqaly.TEXT())
    last_updated = sqaly.Column(sqaly.DateTime())
    state = sqaly.Column(sqaly.Enum(ComputeState))
    error = sqaly.Column(sqaly.TEXT())
    ligand = sqaly.Column(sqaly.TEXT())
    ligand_name = sqaly.Column(sqaly.TEXT())



    