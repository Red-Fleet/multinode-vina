import enum
from app import db
import sqlalchemy as sqaly


class LigandState(enum.Enum):
    COMPUTED: str = "COMPUTED"
    NOT_COMPUTED: str = "NOT_COMPUTED"

class Ligands(db.Model):
    ligand_id = sqaly.Column(sqaly.String(36), primary_key=True)
    ligand = sqaly.Column(sqaly.TEXT())
    state = sqaly.Column(sqaly.Enum(LigandState))