import enum
from app import db
import sqlalchemy as sqaly

class ComputeState(enum.Enum):
    # The docking computation has been successfully completed.
    COMPUTED: str = "COMPUTED"
    # The docking computation has not been performed yet.
    NOT_COMPUTED: str = "NOT_COMPUTED"
    # The docking computation is currently in progress.
    COMPUTING: str = "COMPUTING"
    # An error occurred during the docking computation.
    ERROR: str = "ERROR"

class Compute(db.Model):
    """Each entry in this table has a ligand which will be docked by a worker, 
    it will also store result of docking of that particular ligand as well error 
    is there is any.
    """
    # The unique identifier of the computation.
    compute_id = sqaly.Column(sqaly.String(36), primary_key=True)
    # docking id to which this entry is associated with.
    docking_id = sqaly.Column(sqaly.String(36), index=True)
    # The result of the docking process of this ligand.
    result = sqaly.Column(sqaly.TEXT())
    # The datetime when the computation was last updated. Used for database cleanup.
    last_updated = sqaly.Column(sqaly.DateTime())
    # Stores state of computation.
    state = sqaly.Column(sqaly.Enum(ComputeState))
    #  An error message associated with the computation, if any.
    error = sqaly.Column(sqaly.TEXT())
    # ligand pdbqt
    ligand = sqaly.Column(sqaly.TEXT())
    ligand_name = sqaly.Column(sqaly.TEXT())



    