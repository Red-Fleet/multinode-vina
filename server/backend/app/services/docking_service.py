import uuid
import datetime
from app import db, app
from app.services.notification_service import NotificationService
from app.models.docking import Docking, DockingState
from app.models.compute import Compute, ComputeState
from flask import json
from threading import Lock
from app.system.docking_system import DockingSystem

class DockingService:
    dockings = dict() # contains all docking result
    docking_lock = Lock()

    @staticmethod
    def initDockingService():
        """Method will read pending docking tasks from database, create docking system for those dockings
        and notify all workers associated with those dockings
        Note: this method should run as soon as app starts.
        """
        app.logger.info("Initializing DockingService")

        docking_ids = []
        try:
        # read uncompleted Dockings from database
            result = Docking.query.with_entities(Docking.docking_id).filter_by(state=DockingState.STARTED)
            docking_ids = [row[0] for row in result]
        except Exception as e:
            app.logger.error(e)
        
        for docking_id in docking_ids:
            docking_system = DockingSystem(docking_id)
            DockingService.docking_lock.acquire()
            DockingService.dockings[docking_id] = docking_system
            DockingService.docking_lock.release()
        
        app.logger.info("DockingService initialized")


            

    @staticmethod
    def createDock(target: str, target_name:str, ligands: list[str], ligands_name: str, master_id: str, worker_ids:list[str], params):
        """Method will add a new entry in docking table and add new comptues in compute table for every ligand.
        Method will notify workers using WorkerNotification class.
        Method will create and store a new instance of DockingSystem.

        Args:
            target (str): _description_
            target_name (str): _description_
            ligands (list[str]): _description_
            ligands_name (str): _description_
            master_id (str): _description_
            worker_ids (list[str]): _description_
            params: json

        Raises:
            Exception: _description_

        Returns:
            str: docking_id
        """
        # updating docking details in database
        docking_id = str(uuid.uuid4())
        computes: list[Compute] = []
        compute_ids:list[str] = []
        #print(type(target), type(target_name), type(ligands), type(ligands_name), type(master_id), type(worker_ids))
        for ligand in ligands:
            compute_id = str(uuid.uuid4())
            compute_ids.append(compute_id)
            pass
            computes.append(Compute(compute_id=compute_id, ligand=ligand, state=ComputeState.NOT_COMPUTED))

        dock = Docking(docking_id=docking_id, master_id=master_id, worker_ids= worker_ids, 
            target=target, compute_ids=compute_ids, target_name=target_name, ligands_name=ligands_name,
            state=DockingState.STARTED, last_updated=datetime.datetime.now(), params=params)
        
        try: 
            db.session.add(dock)
            #for ligand in ligand_models:
            db.session.add_all(computes)
            
            #Notifying workers
            for worker in worker_ids:
                NotificationService.createWorkerNotification(docking_id=docking_id, worker_id=worker, commit=False)
            db.session.commit()
        except Exception as e:
            app.logger.error(e)
            raise Exception("DockingService: Database Error")
        
        docking_system = DockingSystem(docking_id)
        DockingService.docking_lock.acquire()
        DockingService.dockings[docking_id] = docking_system
        DockingService.docking_lock.release()

        return docking_id
    
    @staticmethod
    def getDockingDetails(docking_id: str)->dict:
        """returns target pdbqt, master_id, parameters of vina using docking_id

        Args:
            docking_id (str): _description_

        Raises:
            Exception: _description_

        Returns:
            dict: containing target, master_id, params
        """
        try:
            result = Docking.query.with_entities(Docking.master_id, Docking.target, Docking.params).filter_by(docking_id=docking_id).first()
        except Exception as e: 
            app.logger.error(e)
            raise Exception("database error")
        
        dock = {
            "master_id": result[0],
            "target": result[1],
            "params": result[2]
        }

        return dock
        

    def getDockingTarget(docking_id: str)->str:
        """returns target pdbqt using docking_id

        Args:
            docking_id (str): _description_

        Raises:
            Exception: _description_

        Returns:
            str: target
        """
        try:
            result = Docking.query.with_entities(Docking.target).filter_by(docking_id=docking_id).first()

        except Exception as e: 
            app.logger.error(e)
            raise Exception("database error")
        
        return result[0]
        
    @staticmethod
    def getComputes(docking_id: str, num: int)-> dict:
        return DockingService.dockings[docking_id].getComputes(num)