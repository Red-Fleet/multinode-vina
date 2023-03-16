import uuid
import datetime
from app import db, app
from app.services.notification_service import NotificationService
from app.models.docking import Docking, DockingState
from app.models.ligands import Ligands, LigandState
from flask import json

class DockingService:

    def createDock(target: str, target_name:str, ligands: list[str], ligands_name: str, master_id: str, worker_ids:list[str]):
        # updating docking details in database
        docking_id = str(uuid.uuid4())
        ligand_models: list[Ligands] = []
        ligand_ids:list[str] = []
        #print(type(target), type(target_name), type(ligands), type(ligands_name), type(master_id), type(worker_ids))
        for ligand in ligands:
            ligand_id = str(uuid.uuid4)
            ligand_ids.append(ligand_id)

            ligand_models.append(Ligands(ligand_id=ligand_id, ligand=ligand, state=LigandState.NOT_COMPUTED))

        dock = Docking(docking_id=docking_id, master_id=master_id, worker_ids= worker_ids, 
            target=target, ligand_ids=ligand_ids, target_name=target_name, ligands_name=ligands_name,
            state=DockingState.CREATED, last_updated=datetime.datetime.now())

        try: 
            db.session.add(dock)
            #for ligand in ligand_models:
            db.session.add_all(ligand_models)
            for worker in worker_ids:
                NotificationService.createWorkerNotification(docking_id=docking_id, worker_id=worker, commit=False)
            db.session.commit()
        except Exception as e:
            app.logger.error(e)
            raise Exception("DockingService: Database Error")
        
        return docking_id