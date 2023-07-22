import uuid
import datetime
from app import db, app
from app.models.notification import WorkerNotification, MasterNotification

class NotificationService:
    @staticmethod
    def createWorkerNotification(docking_id:str, worker_id:str, commit=True):
        """Used to create notification for worker

        Args:
            docking_id (str): _description_
            worker_id (str): client_id of worker
            commit (boolean): only commit transaction if commit is set to true

        Raises:
            Exception: _description_
        """
        try:
            notification = WorkerNotification.query.filter_by(docking_id=docking_id, worker_id=worker_id).first()

            #create new Notification
            if notification == None:
                notification = WorkerNotification(docking_id=docking_id, worker_id=worker_id, create_time=datetime.datetime.now())
                db.session.add(notification)
            # update previous notification
            else:
                notification.create_date = datetime.datetime.now()
            
            if commit == True:
                db.session.commit()
        except Exception as e:
            app.logger.error(e)
            raise Exception("Database Error")

    
    def createMasterNotification(docking_id:str, master_id:str):
        """Used to create notification for master

        Args:
            docking_id (str): _description_
            master_id (str): client_id of worker

        Raises:
            Exception: _description_
        """
        try:
            notification = MasterNotification.query.filter_by(docking_id=docking_id).first()

            #create new Notification
            if notification == None:
                notification = MasterNotification(docking_id=docking_id, master_id=master_id, create_time=datetime.datetime.now())
                db.session.add(notification)
            # update previous notification
            else:
                notification.create_date = datetime.datetime.now()
            
            db.session.commit()
        except Exception as e:
            app.logger.error(e)
            raise Exception("Database Error")
    
    def getMasterNotifications(master_id: str)-> list[MasterNotification]:
        """return notification of master and delete them from server

        Args:
            master_id (str): _description_

        Raises:
            Exception: _description_

        Returns:
            _type_: _description_
        """
        try:
            # fetching notifications
            results = MasterNotification.query.filter_by(master_id=master_id).all()
            # deleting notifications
            for result in results:
                db.session.delete(result)
            db.session.commit()
        except Exception as e:
            app.logger.error(e)
            raise Exception("Database Error")
        
        return results

    def getWorkerNotifications(worker_id: str)-> list[WorkerNotification]:
        """return notification of master and delete them from server

        Args:
            master_id (str): _description_

        Raises:
            Exception: _description_

        Returns:
            _type_: _description_
        """
        try:
            # fetching notifications
            results = WorkerNotification.query.filter_by(worker_id=worker_id).all()
            # deleting notifications
            for result in results:
                db.session.delete(result)
            db.session.commit()
        except Exception as e:
            app.logger.error(e)
            raise Exception("Database Error")
        
        return results