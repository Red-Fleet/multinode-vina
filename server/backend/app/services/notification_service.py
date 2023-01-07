import uuid
import datetime
from app import db, app
from app.models.notification import WorkerNotification, MasterNotification

class Notification:
    def createWorkerNotification(compute_id:str, worker_id:str):
        """Used to create notification for worker

        Args:
            compute_id (str): _description_
            worker_id (str): client_id of worker

        Raises:
            Exception: _description_
        """
        try:
            notification = WorkerNotification.query.filter_by(compute_id=compute_id).first()

            #create new Notification
            if notification == None:
                notification = WorkerNotification(compute_id=compute_id, worker_id=worker_id, create_time=datetime.datetime.now())
                db.session.add(notification)
            # update previous notification
            else:
                notification.create_date = datetime.datetime.now()
            
            db.session.commit()
        except Exception as e:
            app.logger.error(e)
            raise Exception("Database Error")

    
    def createMasterNotification(compute_id:str, master_id:str):
        """Used to create notification for master

        Args:
            compute_id (str): _description_
            master_id (str): client_id of worker

        Raises:
            Exception: _description_
        """
        try:
            notification = MasterNotification.query.filter_by(compute_id=compute_id).first()

            #create new Notification
            if notification == None:
                notification = MasterNotification(compute_id=compute_id, master_id=master_id, create_time=datetime.datetime.now())
                db.session.add(notification)
            # update previous notification
            else:
                notification.create_date = datetime.datetime.now()
            
            db.session.commit()
        except Exception as e:
            app.logger.error(e)
            raise Exception("Database Error")
    
