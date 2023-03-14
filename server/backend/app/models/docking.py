import enum
from app import db
import sqlalchemy as sqaly

class DockingState(enum.Enum):
    CREATED: str = "CREATED"
    STARTED: str = "STARTED"
    FINISHED: str = "FINISHED"
    ERROR: str = "ERROR"

class Docking(db.Model):
    docking_id = sqaly.Column(sqaly.String(36), primary_key=True)
    master_id = sqaly.Column(sqaly.String(36), nullable=False, index=True)
    worker_ids = sqaly.Column(sqaly.JSON()) # array of worker_ids
    target = sqaly.Column(sqaly.TEXT())
    target_name = sqaly.Column(sqaly.String(1000))
    ligand_ids = sqaly.Column(sqaly.JSON()) # array of ligand_ids
    ligands_name = sqaly.Column(sqaly.String(1000))
    last_updated = sqaly.Column(sqaly.DateTime())
    state = sqaly.Column(sqaly.Enum(DockingState))