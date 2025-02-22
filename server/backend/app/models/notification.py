from app import db
import sqlalchemy as sqaly


class WorkerNotification(db.Model):
    """The worker_notification table stores notifications intended for workers in the 
    system. These notifications are created by the master when a new docking request 
    arrives.  Each notification contains the docking ID and client ID, which informs 
    the worker that it has to handle the docking request associated with that docking ID. 
    Once a worker receives its notification, the corresponding entry is deleted from the 
    table to maintain its size.
    """
    # The unique identifier of the docking request associated with the notification.
    docking_id = sqaly.Column(sqaly.String(36), primary_key=True) 
    # The unique identifier of the worker (client_id) associated with the notification. 
    # Indexed for faster retrieval of docking IDs.
    worker_id = sqaly.Column(sqaly.String(36), nullable=False, index=True)
    # The datetime when the notification was created. This column is used to delete 
    # entries that are considered very old, helping to clean the database.
    create_time = sqaly.Column(sqaly.DateTime())
