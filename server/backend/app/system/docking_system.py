from threading import Thread, Lock
from app.models.compute import Compute, ComputeState
from app import app, db
from app.models.docking import Docking, DockingState
from app.models.compute import Compute, ComputeState
from app.services.notification_service import NotificationService
from sqlalchemy import case
import time

class DockingSystem:
    def __init__(self, docking_id: str):
        self.docking_id = docking_id
        self.computed_ids = [] # result is already generated for these computes
        self.un_computed_ids = [] # result is yet to be generated
        self.computing_ids:dict = dict() # result is being generated, will store compute_id as key and time at which enrty is created as value
        self.error_ids = [] # compute ids which ended with error
        self.lock = Lock() # lock is used for updating computed, uncomputed and computing lists

        self.worker_ids = [] # for storing ids of workers
        self.master_id: str = None # for storing id of master
        self.params = dict() # for storing different parameters used while docking like scoring function, grid size etc.
        
        self.docking_details_initialized = False
        self.readDockingDetailsFromDBThread = Thread(target=self.readDockingDetailsFromDB)
        self.readDockingDetailsFromDBThread.start()

        self.docking_error_lock = Lock() # for storing docking error in database => lock makes this operation atomic
    # def set_computing_ligand_ids(self, computing_ligand_ids):
    #     self.computed_ligand_ids = computing_ligand_ids

    def readDockingDetailsFromDB(self):
        """Method will first get all compute_ids from compute table using docking_id, and then
        get compute status to initialize computed, uncomputed ids.
        Method will notify all workers of the docking
        Note: all computing ids will be considered as uncomputed.
        """
        with app.app_context():
            try:
                result = Docking.query.with_entities(
                    Docking.master_id, Docking.worker_ids).filter_by(docking_id=self.docking_id).first()

                self.worker_ids = result[1]
                self.master_id = result[0]

                result = Compute.query.with_entities(
                    Compute.compute_id, Compute.state
                ).filter_by(docking_id = self.docking_id).all()

                # compute_ids = [row[0] for row in result]
                
                # read status of all docking
                # result = Compute.query.with_entities(
                #     Compute.compute_id, Compute.state
                # ).filter(
                #     Compute.compute_id.in_(compute_ids)
                # ).all()

                try: 
                    self.lock.acquire()
                    for compute in result:
                        if compute[1] == ComputeState.COMPUTED: self.computed_ids.append(compute[0])
                        elif compute[1] == ComputeState.NOT_COMPUTED: self.un_computed_ids.append(compute[0])
                        elif compute[1] == ComputeState.COMPUTING: self.un_computed_ids.add(compute[0]) # computing_ids are considered as uncomputed
                        else: self.error_ids.append(compute[0])
                except Exception as e:
                    app.logger.error(e)
                finally:
                    self.lock.release() # always release this lock

                # Notifying workers
                for worker in self.worker_ids:
                    NotificationService.createWorkerNotification(docking_id=self.docking_id, worker_id=worker, commit=False)
                # commiting
                db.session.commit()
                
            except Exception as e:
                app.logger.error(e)
                # garbage collector will automatically delete this object
                self.readDockingDetailsFromDBThread = None
                raise Exception("Database Error")
            finally:
                self.docking_details_initialized = True
            
        


        # garbage collector will automatically delete this object
        self.readDockingDetailsFromDBThread = None

    def getComputes(self, num: int):
        try:
            self.lock.acquire()
            compute_ids = []

            for i in range(min(num, len(self.un_computed_ids))):
                compute_ids.append(self.un_computed_ids[-1])
                self.computing_ids[self.un_computed_ids[-1]] = time.time()
                self.un_computed_ids.pop()

        except Exception as e:
            app.logger.error(e)
        finally:
            self.lock.release()


        # get details from database
        computes = []

        try:
            results = Compute.query.filter(Compute.compute_id.in_(
                compute_ids)).with_entities(Compute.compute_id, Compute.ligand).all()
            computes = [{"compute_id": row[0], "ligand": row[1]}
                        for row in results]
        except Exception as e:
            app.logger.error(e)
            raise Exception("Database Error")

        if len(computes) == 0:
            if len(self.computing_ids) == 0: # docking is finished
                try:
                    Docking.query.filter_by(docking_id=self.docking_id).update({'state': DockingState.FINISHED})
                    db.session.commit()
                except Exception as e:
                    app.logger.error(e)
                    raise Exception("Database Error")
            else:
                try:
                    self.lock.acquire()
                    # if compute is spending too much time on worker(worker might be closed) then reassign it to other worker
                    rem_ids = []

                    # if more than 30 minutes has passed remove them from computing and insert in uncomputes_ids
                    for compute_id, start_time in self.computing_ids.items():
                        if time.time() - start_time > 30*60: 
                            rem_ids.append(compute_id)
                    
                    for compute_id in rem_ids:
                        self.computing_ids.pop(compute_id)
                        self.un_computed_ids.append(compute_id)
                except Exception as e:
                    app.logger.error(e)
                    raise Exception("Error while compute reassignment")
                finally:
                    self.lock.release()

        return computes

    def isDockingFinished(self):
        """Return true if all computes are computed else false

        Returns:
            _type_: boolean
        """
        if self.docking_details_initialized == False: return False

        try:
            self.lock.acquire()
            if len(self.un_computed_ids)==0 and len(self.computing_ids)==0:
                return True
            else:
                return False
        finally:
            self.lock.release()
        
    def saveResults(self, computes):
        """save compute result in database

        Args:
            computes (_type_): _description_
        """
        if len(computes) == 0: return 
        
        compute_ids = [compute["compute_id"] for compute in computes]
        
        # save in database
        Compute.query.filter(Compute.compute_id.in_(compute_ids)).update(
            {
                Compute.result: db.case({compute["compute_id"]: compute["result"] for compute in computes}, value=Compute.compute_id),
                Compute.state: case({compute["compute_id"]: "COMPUTED" for compute in computes}, value=Compute.compute_id)
            }
        )

        db.session.commit()
        try:
            self.lock.acquire()
            for id in compute_ids:
                self.computing_ids.pop(id)
                self.computed_ids.append(id)

        except Exception as e:
            app.logger.error(e)
            raise Exception("Error while saving compute result")
        finally:
            self.lock.release()

    def saveComputeError(self, computes):
        """save compute error in database

        Args:
            computes (_type_): list of compute error
        """
        if len(computes) == 0: return 
        
        compute_ids = [compute["compute_id"] for compute in computes]
        
        # save in database
        Compute.query.filter(Compute.compute_id.in_(compute_ids)).update(
            {
                Compute.result: db.case({compute["compute_id"]: compute["error"] for compute in computes}, value=Compute.compute_id),
                Compute.state: case({compute["compute_id"]: "ERROR" for compute in computes}, value=Compute.compute_id)
            }
        )

        db.session.commit()
        try:
            self.lock.acquire()
            for id in compute_ids:
                self.computing_ids.pop(id)
                self.error_ids.append(id)

        except Exception as e:
            app.logger.error(e)
            raise Exception("Error while saving compute error")
        finally:
            self.lock.release()

    def getDockingStatus(self)-> dict[str, int]:
        """returns dictonary contaning total of computing, computed, uncomputed and error computes

        Returns:
            dict[str, int]: _description_
        """
        result = {
            ComputeState.COMPUTING.name: len(self.computing_ids),
            ComputeState.COMPUTED.name: len(self.computed_ids),
            ComputeState.NOT_COMPUTED.name: len(self.un_computed_ids),
            ComputeState.ERROR.name: len(self.error_ids)
        }
        return result
    
    def saveDockingError(self, worker_id: str, error:str):
        """save error from worker raised while grid map generation or target loading

        Args:
            worker_id (str): id of worker
            error (str): error raised by worker
        """
        with app.app_context():
            try:
                self.docking_error_lock.acquire()
                result = Docking.query.with_entities(
                    Docking.error).filter_by(docking_id=self.docking_id).first()
                
                if result is None:
                    result = dict()

                result["worker_id"] = error

                Docking.query.with_entities(Docking.error).update(
                    {
                        Docking.error: result
                    }
                )

                db.session.commit()
            except Exception as e:
                app.logger.error(e)
                raise Exception("Error while saving docking error")
            finally:
                self.docking_error_lock.release()

                
                


        

    # def getComputeResult(self, compute_id: str)->dict[str, str]:
    #     """return result and state of compute 

    #     Args:
    #         compute_id (str): str

    #     Returns:
    #         dict[str, str]: dict contaning compute_id, state and result
    #     """
    #     data = Compute.query.with_entities(Compute.state, Compute.result).filter_by(compute_id= compute_id).first()
    #     result = {
    #         "compute_id": compute_id,
    #         "state": data[0],
    #         "result": data[1]
    #     }

    #     return result
