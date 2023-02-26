import enum
from app import db
import sqlalchemy as sqaly


class MasterComputeLigand(db.Model):
    """This table will store details of computation started by master like ligand, 
    target_id to which current ligand is associated with.


    Args:
        db (_type_): _description_
    """

    # table name
    __tablename__ = "master_compute_ligand"
    # auto generated id
    ligand_id = sqaly.Column(sqaly.Integer, primary_key=True, autoincrement=True)
    # id of target to which current lignad is associated with
    target_id = sqaly.Column(sqaly.Integer, index=True)
    # target pdbqt
    ligand = sqaly.Column(sqaly.TEXT())
    # ligand file name
    ligand_name = sqaly.Column(sqaly.String(1000))