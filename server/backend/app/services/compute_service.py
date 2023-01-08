import uuid
import datetime
from app import db, app
from app.models.compute import Compute, ComputeState
from app.services.notification_service import Notification

class ComputeService:
    
    def createComputeTask(master_id:str, worker_id:str, target, ligands)-> str:
        """Create new compute task, function will also create notification of worker, and return compute_id

        Args:
            master_id (str): _description_
            worker_id (str): _description_
            target (_type_): _description_
            ligands (_type_): _description_

        Raises:
            Exception: _description_
        """
        compute_id = str(uuid.uuid4())
        task = Compute(compute_id=compute_id, master_id=master_id, worker_id=worker_id, 
            target=target, ligands=ligands, state=ComputeState.CREATED, last_updated=datetime.datetime.now())
        
        try: 
            db.session.add(task)
            Notification.createWorkerNotification(compute_id=compute_id, worker_id=worker_id)
            db.session.commit()
        except Exception as e:
            app.logger.error(e)
            raise Exception("Database Error")
        
        return compute_id
    

        
    def getComputeTaskUsingComputeId(compute_id:str):
        """return compute task using compute id

        Args:
            compute_id (str): _description_

        Raises:
            Exception: _description_

        Returns:
            _type_: _description_
        """
        try:
            task = Compute.query.filter_by(compute_id = compute_id).first()
        except Exception as e:
            app.logger.error(e)
            raise Exception("Database Error")

        return task

    def updateResult(compute_id: str, result: str):
        """Update result of compute request and notify master

        Args:
            compute_id (str): _description_
            result (str): _description_

        Raises:
            Exception: _description_
        """
        try:
            Compute.query.filter_by(compute_id=compute_id).update({'result':result, 'state': ComputeState.FINISHED})
            
            # getting master_id for sending notification
            master_id = Compute.query.with_entities(Compute.master_id).filter_by(compute_id=compute_id).first()[0]

            Notification.createMasterNotification(compute_id=compute_id, master_id=master_id)
        except Exception as e:
            app.logger.error(e)
            raise Exception("Database Error")
        

    def updateError(compute_id: str, error: str):
        """Update error of compute request and notify master

        Args:
            compute_id (str): _description_
            error (str): _description_

        Raises:
            Exception: _description_
        """
        try:
            Compute.query.filter_by(compute_id=compute_id).update({'error':error, 'state': ComputeState.ERROR})
            
            # getting master_id for sending notification
            master_id = Compute.query.with_entities(Compute.master_id).filter_by(compute_id=compute_id).first()[0]

            Notification.createMasterNotification(compute_id=compute_id, master_id=master_id)
        except Exception as e:
            app.logger.error(e)
            raise Exception("Database Error")