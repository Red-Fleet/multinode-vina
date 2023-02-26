import enum
from app import db
import sqlalchemy as sqaly

class MasterComputeState(enum.Enum):
    COMPUTING: str = "COMPUTING"
    PAUSED: str = "PAUSED" # system will not resume paused computation automatically
    FINISHED: str = "FINISHED"
    ERROR: str = "ERROR" # system will not resume error computation automatically

class MasterComputeTarget(db.Model):
    """This table will store details of computation started by master like target, 
    workers on which computation will happen


    Args:
        db (_type_): _description_
    """

    # table name
    __tablename__ = "master_compute_target"
    # auto generated id
    target_id = sqaly.Column(sqaly.Integer, primary_key=True, autoincrement=True)
    # client_id of master (index is not necessary)
    master_id = sqaly.Column(sqaly.String(36))
    # target pdbqt
    target = sqaly.Column(sqaly.TEXT())
    # target file name
    target_name = sqaly.Column(sqaly.String(1000))
    # client_id of workers on which computation will happen
    workers = sqaly.Column(sqaly.JSON)
    
    state = sqaly.Column(sqaly.Enum(MasterComputeState), index=True)