import uuid
import datetime
from app import db, app
from app.services.notification_service import NotificationService
from app.models.docking import Docking, DockingState
from app.models.compute import Compute, ComputeState
from flask import json
from threading import Lock

class DockingService:
    dockings = dict() # contains all docking result
    docking_lock = Lock()

    class DockingDetails:
        def __init__(self, docking_id, db_read_ligand_ids=True):
            self.docking_id = docking_id
            self.computed_ids = [] 
            self.un_computed_ids = []
            self.computing_ids = set()
            self.lock = Lock()

            if db_read_ligand_ids == True:
                self.init_computed_and_un_computed_ligands()
        
        # def set_computing_ligand_ids(self, computing_ligand_ids):
        #     self.computed_ligand_ids = computing_ligand_ids
        
        def init_computed_and_un_computed_ligands(self):
            pass


        def getComputes(self, num: int):
            self.lock.acquire()
            compute_ids = []

            for i in range(min(num, len(self.un_computed_ids))):
                compute_ids.append(self.un_computed_ids[-1])
                self.computing_ids.add(self.un_computed_ids[-1])
                self.un_computed_ids.pop()

            self.lock.release()

            # get details from database
            computes = []

            try:
                results = Compute.query.filter(Compute.compute_id.in_(compute_ids)).with_entities(Compute.compute_id, Compute.ligand).all()
                computes = [{"compute_id": row[0], "ligand": row[1]} for row in results]
            except Exception as e:
                app.logger.error(e)
                raise Exception("Database Error")
            
            return computes
        

        def saveResults(self, computes):
            compute_ids = [compute["compute_id"] for compute in computes]
            # save in database
            Compute.query.filter(Compute.compute_id.in_(compute_ids)).update(
                    {Compute.result: db.case(computes, value=Compute.result)}
                )
            

            self.lock.acquire()
            for id in compute_ids:
                self.computing_ids.remove(id)
                self.computed_ids.append(id)
            
            self.lock.release()



            

    @staticmethod
    def createDock(target: str, target_name:str, ligands: list[str], ligands_name: str, master_id: str, worker_ids:list[str]):
        # updating docking details in database
        docking_id = str(uuid.uuid4())
        computes: list[Compute] = []
        compute_ids:list[str] = []
        #print(type(target), type(target_name), type(ligands), type(ligands_name), type(master_id), type(worker_ids))
        for ligand in ligands:
            compute_id = str(uuid.uuid4())
            compute_ids.append(compute_id)
            
            computes.append(Compute(compute_id=compute_id, ligand=ligand, state=ComputeState.NOT_COMPUTED))

        dock = Docking(docking_id=docking_id, master_id=master_id, worker_ids= worker_ids, 
            target=target, compute_ids=compute_ids, target_name=target_name, ligands_name=ligands_name,
            state=DockingState.CREATED, last_updated=datetime.datetime.now())
        
        docking_details = DockingService.DockingDetails(docking_id, db_read_ligand_ids=False)
        docking_details.un_computed_ids = compute_ids

        DockingService.docking_lock.acquire()
        DockingService.dockings[docking_id] = docking_details
        DockingService.docking_lock.release()
        
        try: 
            db.session.add(dock)
            #for ligand in ligand_models:
            db.session.add_all(computes)
            for worker in worker_ids:
                NotificationService.createWorkerNotification(docking_id=docking_id, worker_id=worker, commit=False)
            db.session.commit()
        except Exception as e:
            app.logger.error(e)
            raise Exception("DockingService: Database Error")
        
        return docking_id
    
    @staticmethod
    def getComputes(docking_id: str, num: int)-> dict:
        return DockingService.dockings[docking_id].getComputes(num)