from app import db
import sqlalchemy as sqaly


class WorkerNotification(db.Model):
    """Stores notification of worker
    """
    compute_id = sqaly.Column(sqaly.String(36), primary_key=True)
    worker_id = sqaly.Column(sqaly.String(36), nullable=False, index=True)
    create_time = sqaly.Column(sqaly.DateTime())

class MasterNotification(db.Model):
    """Stores notification of master
    """
    compute_id = sqaly.Column(sqaly.String(36), primary_key=True)
    master_id = sqaly.Column(sqaly.String(36), nullable=False, index=True)
    create_time = sqaly.Column(sqaly.DateTime())
