import uuid
import datetime
from app import db, app
from app.services.notification_service import NotificationService
from app.models.docking import Docking, DockingState
from app.models.compute import Compute, ComputeState
from flask import json
from threading import Lock
from app.system.docking_system import DockingSystem
import time
from app.models.notification import WorkerNotification
from threading import Thread

class DockingService:
    dockings: dict[str, DockingSystem] = dict() # contains all docking result
    docking_lock: Lock = Lock()
    recreate_docking_notification = None

    @staticmethod
    def recreateDockingNotificationThread():
        with app.app_context():
            while(1):
                
                time.sleep(60*2) # after every 2 minutes recreates docking notification from worker
                
                try:
                    DockingService.docking_lock.acquire()
                    for docking in DockingService.dockings.values():
                        if docking.isDockingFinished() == True: continue

                        # only create notification if docking is not finished
                        for worker_id in docking.worker_ids:
                            NotificationService.createWorkerNotification(docking_id=docking.docking_id, worker_id=worker_id, commit=False)
                    
                    db.session.commit()
                except Exception as e:
                    app.logger.error(e)
                finally:
                    DockingService.docking_lock.release()
                


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
        
        # starting notification thread
        DockingService.recreate_docking_notification = Thread(target=DockingService.recreateDockingNotificationThread)
        DockingService.recreate_docking_notification.start()
        app.logger.info("DockingService initialized")


            

    @staticmethod
    def createDock(target: str, 
                   target_name:str, 
                   ligands: list[str], 
                   ligands_name: list[str], 
                   master_id: str, 
                   worker_ids:list[str],
                   params: dict
                   ):
        """Method will add a new entry in docking table and add new comptues in compute table for every ligand.
        Method will notify workers using WorkerNotification class.
        Method will create and store a new instance of DockingSystem.

        Args:
            target (str): _description_
            target_name (str): _description_
            ligands (list[str]): list contaning ligand pdbqt
            ligands_name (list[str]): list contaning ligand name
            master_id (str): _description_
            worker_ids (list[str]): _description_
            params: dict

        Raises:
            Exception: _description_

        Returns:
            str: docking_id
        """
        # updating docking details in database
        docking_id = str(uuid.uuid4())
        computes: list[Compute] = []
        compute_ids:list[str] = []
        
        for i in range(len(ligands)):
            ligand = ligands[i]
            try: 
                ligand_name = ligands_name[i]
            except Exception as e: # ligand name is not present
                ligand_name = ""

            compute_id = str(uuid.uuid4())
            compute_ids.append(compute_id)
            computes.append(Compute(compute_id=compute_id, docking_id=docking_id, ligand=ligand, ligand_name=ligand_name, state=ComputeState.NOT_COMPUTED))

        dock = Docking(docking_id=docking_id, master_id=master_id, worker_ids= worker_ids, 
            target=target, target_name=target_name,
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
        
        # creating docking system for this target
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
        if docking_id in DockingService.dockings:
            return DockingService.dockings[docking_id].getComputes(num)
        else : return []
    
    @staticmethod
    def saveComputeResult(docking_id: str, computes: list):
        DockingService.dockings[docking_id].saveResults(computes)
        
        
    @staticmethod
    def saveComputeError(docking_id: str, computes: list):
        
        DockingService.dockings[docking_id].saveComputeError(computes)
        
        
    
    @staticmethod
    def saveDockingError(docking_id: str, worker_id: str, error: str):
        
        DockingService.dockings[docking_id].saveDockingError(worker_id=worker_id, error=error)
        
        
    @staticmethod
    def getDockingStatus(docking_id: str)-> dict[str, int]:
        """returns dictonary contaning total of computing, computed, uncomputed and error computes

        Args:
            docking_id (str): _description_

        Returns:
            dict[str, int]: _description_
        """
        return DockingService.dockings[docking_id].getDockingStatus()
    
    @staticmethod
    def isDockingFinished(docking_id: str)->bool:
        finished = True
        if docking_id in DockingService.dockings:
            finished =  DockingService.dockings[docking_id].isDockingFinished()
        

        return finished


    

    @staticmethod
    def deleteDocking(docking_id: str):
       

        try:
            DockingService.docking_lock.acquire()
            if docking_id in DockingService.dockings:
                del DockingService.dockings[docking_id]
        except Exception as e:
            app.logger.error(e)
        finally:
            DockingService.docking_lock.release()

        # removing from database
        try:
            Docking.query.filter_by(docking_id=docking_id).delete()
            Compute.query.filter_by(docking_id=docking_id).delete()
            db.session.commit()
        except Exception as e:
            app.logger.error(e)
            raise Exception("database error")
    


    # @staticmethod
    # def getComputeResult(docking_id: str, compute_id: str)-> dict[str, str]:
    #     """return result and state of compute 

    #     Args:
    #         docking_id (str): _description_
    #         compute_id (str): _description_

    #     Returns:
    #         dict[str, str]: dict contaning compute_id, state and result
    #     """
    #     return DockingService.dockings[docking_id].getComputeResult(compute_id=compute_id)
    
    @staticmethod
    def getMasterDockingIds(master_id: str)->list[dict[str, str]]:
        """function returns all docking_id of dockings started by master

        Args:
            master_id (str): client_id of master

        Raises:
            Exception: _description_

        Returns:
            list[dict[str, str]]: list of dict contaning docking_id and state of docking
        """
        try:
            rows = Docking.query.with_entities(Docking.docking_id, Docking.state).filter_by(master_id=master_id)
            result: list[dict[str, str]] = [{"docking_id": row[0], "state": row[1].name} for row in rows]
        except Exception as e:
            app.logger.error(e)
            raise Exception("DockingService: Database Error")

        for docking in result:
            if docking['docking_id'] in DockingService.dockings:
                docking["computed"] = DockingService.getDockingStatus(docking['docking_id'])['COMPUTED']

            else:
                docking['computed'] = Compute.query.with_entities(Compute.compute_id).filter_by(docking_id = docking['docking_id']).count()


        return result
    

    @staticmethod
    def getAllComputeIds(docking_id: str)-> list[str]:
        """returns all compute_ids of a docking

        Args:
            docking_id (str): docking id

        Raises:
            Exception: _description_

        Returns:
            list[str]: list contaning compute ids
        """
        try:
            rows = Compute.query.with_entities(Compute.compute_id).filter_by(docking_id=docking_id)
            result: list[str] = [row[0] for row in rows]
        except Exception as e:
            app.logger.error(e)
            raise Exception("DockingService: Database Error")
        
        return result

    def getComputeResult(compute_id: str)-> dict[str, str]:
        """returns result pdbqt and ligand_name of given compute_id

        Args:
            compute_id (str): compute id of ligand

        Raises:
            Exception: _description_

        Returns:
            dict[str, str]: {
                "result": "pdbqt",
                "ligand_name": "name"
            }
        """
        try:
            row = Compute.query.with_entities(Compute.result, Compute.ligand_name).filter_by(compute_id=compute_id).first()
            result = {
                "result": row[0],
                "ligand_name": row[1]
            }
        except Exception as e:
            app.logger.error(e)
            raise Exception("DockingService: Database Error")
        
        return result

        