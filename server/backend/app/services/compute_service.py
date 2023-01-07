import uuid
import datetime
from app import db, app
from app.models.compute import Compute, ComputeState
from app.services.notification_service import WorkerNotification, MasterNotification

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
            WorkerNotification(compute_id=compute_id, worker_id=worker_id)
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
