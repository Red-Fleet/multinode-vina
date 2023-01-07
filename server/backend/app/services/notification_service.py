import uuid
import datetime
from app import db, app
from app.models.notification import WorkerNotification, MasterNotification

class Notification:
    def createWorkerNotification(compute_id:str, worker_id:str):
        try:
            notification = 