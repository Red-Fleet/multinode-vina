from threading import Thread, Lock
from app.models.compute import Compute, ComputeState
from app import app, db
from app.models.docking import Docking, DockingState
from app.models.compute import Compute, ComputeState
from app.services.notification_service import NotificationService
from sqlalchemy import case

class DockingSystem:
    def __init__(self, docking_id: str):
        self.docking_id = docking_id
        self.computed_ids = [] # result is already generarwd for these computes
        self.un_computed_ids = [] # result is yet to be generated
        self.computing_ids = set() # result is being generated
        self.error_ids = [] # compute ids which ended with error
        self.lock = Lock() # lock is used for updating computed, uncomputed and computing lists

        self.worker_ids = [] # for storing ids of workers
        self.master_id: str = None # for storing id of master
        self.params = dict() # for storing different parameters used while docking like scoring function, grid size etc.

        self.readDockingDetailsFromDBThread = Thread(target=self.readDockingDetailsFromDB)
        self.readDockingDetailsFromDBThread.start()

    # def set_computing_ligand_ids(self, computing_ligand_ids):
    #     self.computed_ligand_ids = computing_ligand_ids

    def readDockingDetailsFromDB(self):
        """Method will first get all compute_ids from docking table using docking_id, and then
        get compute status to initialize computed, uncomputed ids.
        Method will notify all workers of the docking
        Note: all computing ids will be considered as uncomputed.
        """
        with app.app_context():
            try:
                result = Docking.query.with_entities(
                    Docking.master_id, Docking.compute_ids, Docking.worker_ids).filter_by(docking_id=self.docking_id).first()

                self.worker_ids = result[2]
                self.master_id = result[0]
                compute_ids = result[1]

                # read status of all docking
                result = Compute.query.with_entities(
                    Compute.compute_id, Compute.state
                ).filter(
                    Compute.compute_id.in_(compute_ids)
                ).all()

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
            
        


        # garbage collector will automatically delete this object
        self.readDockingDetailsFromDBThread = None

    def getComputes(self, num: int):
        try:
            self.lock.acquire()
            compute_ids = []

            for i in range(min(num, len(self.un_computed_ids))):
                compute_ids.append(self.un_computed_ids[-1])
                self.computing_ids.add(self.un_computed_ids[-1])
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

        if len(computes) == 0: # docking finished
            Docking.query.filter_by(docking_id=self.docking_id).update({'state': DockingState.FINISHED})
            db.session.commit()
        return computes

    def saveResults(self, computes):
        """save compute result in database

        Args:
            computes (_type_): _description_
        """
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
                self.computing_ids.remove(id)
                self.computed_ids.append(id)

        except Exception as e:
            app.logger.error(e)
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
    
    def getComputeResult(self, compute_id: str)->dict[str, str]:
        """return result and state of compute 

        Args:
            compute_id (str): str

        Returns:
            dict[str, str]: dict contaning compute_id, state and result
        """
        data = Compute.query.with_entities(Compute.state, Compute.result).filter_by(compute_id= compute_id).first()
        result = {
            "compute_id": compute_id,
            "state": data[0],
            "result": data[1]
        }

        return result
