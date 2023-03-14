import uuid
import datetime
from app import db, app
from app.services.notification_service import NotificationService
from app.models.docking import Docking, DockingState
from flask import json

class DockingService:

    def createDock(target: str, target_name:str, lignads: list[str], ligands_name: str, master_id: str, worker_ids:list[str]):
        # updating docking details in database
        docking_id = str(uuid.uuid4())
        dock = Docking(docking_id=docking_id, master_id=master_id, worker_ids= worker_ids, 
            target=target, ligands=lignads, target_name=target_name, ligands_name=ligands_name,
            state=DockingState.CREATED, last_updated=datetime.datetime.now())
        
        try: 
            db.session.add(dock)
            for worker in worker_ids:
                NotificationService.createWorkerNotification(docking_id=docking_id, worker_id=worker)
            db.session.commit()
        except Exception as e:
            app.logger.error(e)
            raise Exception("DockingService: Database Error")
        
        return docking_id