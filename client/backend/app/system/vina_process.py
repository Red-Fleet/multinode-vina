from threading import Thread
from vina import Vina
import os
import pathlib
import time
import multiprocessing
import signal
import random

class VinaProcess(multiprocessing.Process):
    
    class ParamsMessage:
        def __init__(self, center, box, target_path: str, scoring_function: str = None, cores_count: int = None, random_seed: int = None,
                     exhaustiveness = None, n_poses=None, min_rmsd=None, max_evals=None):
            self.scoring_function = scoring_function
            self.cores_count = cores_count
            self.random_seed = random_seed
            self.exhaustiveness = exhaustiveness
            self.n_poses = n_poses
            self.min_rmsd = min_rmsd
            self.max_evals = max_evals
            self.box = box
            self.center = center
            self.target_path  = target_path

            if box is None or len(box)!=3: raise Exception("Box should contain [x, y, z]")
            if center is None or len(center)!=3: raise Exception("Center should contain [x, y, z]")

    
    class InitVinaMessage:
        # will create new instance of vina and also initialize grid map
        pass
    
    class EndProcessMessage:
        # this messege will stop run
        pass

    class ProcessEndedMessage:
        # this message is send once run stops, for letting parent to know that run is stopped
        pass

    class Error:
        def __init__(self, message) -> None:
            self.message = message

    class LigandError:
        def __init__(self, compute_id, message) -> None:
            self.compute_id = compute_id
            self.message = message

    
    class ComputeMessage:
        def __init__(self, compute_id, ligand) -> None:
            self.compute_id = compute_id
            self.ligand = ligand
    
    class ResultMessage:
        def __init__(self, compute_id, result) -> None:
            self.compute_id = compute_id
            self.result = result
    
    def __init__(self,
                 control_queue: multiprocessing.Queue,
                 compute_queue: multiprocessing.Queue,
                 result_queue: multiprocessing.Queue, 
                 error_queue: multiprocessing.Queue,
                 slow_compute_queue: multiprocessing.Queue,
                 logs_queue: multiprocessing.Queue,
                 process_ended_event: multiprocessing.Event) -> None:
        multiprocessing.Process.__init__(self)
        self.control_queue = control_queue
        self.compute_queue = compute_queue
        self.result_queue = result_queue
        self.error_queue = error_queue
        self.slow_compute_queue = slow_compute_queue
        self.logs_queue = logs_queue
        self.process_ended_event = process_ended_event
        
        self.target_path: str = None
        self.vina: Vina = None

        self.scoring_function = "vina"
        self.cores_count = 1
        self.random_seed = 0
        self.exhaustiveness = 8
        self.n_poses = 20
        self.min_rmsd = 1.0
        self.max_evals = 0
        self.grid_spacing = 0.375

        self.exitProcessFlag: bool = False # if true this process will stop and exit
        
        self.dockingThreadVariable = None
        self.logs("VinaProcess(__init__): Vina Process initialized")
        
        

    def run(self):
        self.logs("VinaProcess(run): Control thread running")
        while self.exitProcessFlag == False:
            time.sleep(10) # read control signal after every 10 sec
            try:
                while not self.control_queue.empty():
                    item = self.control_queue.get()
                    self.logs("VinaProcess(run):Item "+ str(type(item)))
                    if isinstance(item, VinaProcess.ParamsMessage):
                        if item.scoring_function is not None: 
                            self.scoring_function = item.scoring_function
                        if item.cores_count is not None:
                            self.cores_count = item.cores_count
                        if item.random_seed is not None : 
                            self.random_seed = item.random_seed
                        if item.exhaustiveness is not None:
                            self.exhaustiveness = item.exhaustiveness
                        if item.n_poses is not None:
                            self.n_poses = item.n_poses
                        if item.min_rmsd is not None:
                            self.min_rmsd = item.min_rmsd
                        if item.max_evals is not None:
                            self.max_evals = item.max_evals
                        self.center = item.center
                        self.box = item.box
                        self.target_path = item.target_path

                    elif isinstance(item, VinaProcess.EndProcessMessage):
                        self.exitProcessFlag = True
                        break
                    elif isinstance(item, VinaProcess.InitVinaMessage):
                        try:
                            self.vina = self.getVina()
                        except Exception as e:
                            self.error_queue.put(VinaProcess.Error(e))
                            self.exitProcessFlag = True
                            break
                        
                        # Load target
                        try:
                            self.vina.set_receptor(self.target_path)
                        except Exception as e:
                            self.error_queue.put(VinaProcess.Error(e))
                            self.exitProcessFlag = True
                            break

                        # Generate grid map
                        try:
                            self.setVinaMap()
                        except Exception as e:
                            self.error_queue.put(VinaProcess.Error(e))
                            self.exitProcessFlag = True
                            break
                    
                        self.dockingThreadVariable = Thread(target=self.dockingThread)
                        self.dockingThreadVariable.start()

            except Exception as e:
                self.logs("VinaProcess(run):Error "+ str(e))
                self.error_queue.put(VinaProcess.Error(e))
                self.exitProcessFlag = True

            
        # weight for docking thread to end
        while self.dockingThreadVariable is not None and self.dockingThreadVariable.is_alive() == True:
            time.sleep(10)
        
        
        self.logs("VinaProcess(run): Control thread ended")
        self.process_ended_event.set()
        # os.kill(os.getpid(), signal.SIGKILL)

    def dockingThread(self):
        
        while self.exitProcessFlag is False:
            while self.compute_queue.empty() == True:
                time.sleep(10) # sleep for 10 seconds is no ligand is present
                if self.exitProcessFlag == True: return
            

            try: 
                
                compute: VinaProcess.ComputeMessage = self.compute_queue.get()
                
                try: 
                    self.vina.set_ligand_from_string(compute.ligand)
                except Exception as e:
                    self.error_queue.put(VinaProcess.LigandError(compute.compute_id, e))
                    self.exitProcessFlag = True
                    break

                self.vina.dock(exhaustiveness=self.exhaustiveness, 
                                                n_poses=self.n_poses,
                                                min_rmsd=self.min_rmsd,
                                                max_evals=self.max_evals)
                
                result = VinaProcess.ResultMessage(compute.compute_id, self.vina.poses(n_poses=self.n_poses))
                self.slow_compute_queue.get() # remove compute from computing_queue
                self.result_queue.put(result)
            except Exception as e:
                self.error_queue.put(VinaProcess.LigandError(compute.compute_id, e))
                self.exitProcessFlag = True
                break

    
    def setVinaMap(self):
        self.vina.compute_vina_maps(center=self.center, box_size=self.box, spacing=self.grid_spacing)



    def getVina(self):

        return Vina(sf_name=self.scoring_function, 
                    cpu=self.cores_count,
                    seed=self.random_seed)

    def logs(self, message: str):
        self.logs_queue.put(message)

        
        