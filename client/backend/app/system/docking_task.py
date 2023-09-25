from app import app
from threading import Thread
from app.http_services.server_http_docking_service import ServerHttpDockingService
from vina import Vina
import os
import pathlib
import time
import math
import queue
import multiprocessing
from app.system.vina_process import VinaProcess

class DockingTask:

    class ProcessEntity:
        def __init__(self, vina_process, control_queue, compute_queue, result_queue,error_queue, 
                     num_core, compute_assigned_queue) -> None:
            self.vina_process: VinaProcess = vina_process
            self.control_queue: multiprocessing.Queue = control_queue
            self.compute_queue: multiprocessing.Queue = compute_queue
            self.result_queue: multiprocessing.Queue = result_queue
            self.error_queue: multiprocessing.Queue = error_queue
            self.alive = True
            self.num_core = num_core
            self.compute_assigned_queue: queue.Queue = compute_assigned_queue


    def __init__(self, docking_id) -> None:
        self.docking_id = docking_id
        self.avaliable_cores = 1
        self.target = None
        self.target_path: str = None
        self.params: dict = None
        self.master_id: str = None

        self.inital_batch_size = 10
        self.ideal_completion_time = 10 # in minutes

        self.process_cores = []
        self.processes:list[DockingTask.ProcessEntity] = [] # will store all process entity
        
        self.docking_details_inititalized = False # should come before starting of the docking details thread
        
        self.run_thread = Thread(target=self.run)
        self.run_thread.start()

    
    def run(self):
        try:
            self.getDockingDetails()
        except Exception as e:
            #######################handle this###################
            with app.app_context():
                app.logger.info("Error while fetching Docking detials: docking_id{self.docking_id}\n", e)
        

        self.createVinaProcesses()

        



    def getDockingDetails(self):
        """will receive docking details from server(for given docking_id). And save target in temp folder
        """
        with app.app_context():
            docking_details = ServerHttpDockingService.getDockingDetails(self.docking_id)
            self.params = self.initVinaParams(docking_details["params"])
            self.target = docking_details["target"]
            self.master_id = docking_details["master_id"]

            app.logger.info("Docking Details received from server: docking_id({self.docking_id})")

            # save receptor in temp file
            self.saveReceptorInTempFolder(self.target)

            self.docking_details_inititalized = True

    def saveReceptorInTempFolder(self, target):
        temp_dir_path: str = os.path.join(str(pathlib.Path(__file__).parent.resolve()), "temp_receptors")
        if os.path.exists(temp_dir_path) == False:
            # create dir for storing temp files
            os.mkdir(temp_dir_path)

        # save receptor
        self.target_path = os.path.join(temp_dir_path, self.docking_id+"_receptor.pdbqt")
        rece_file = open(self.target_path, "w")
        rece_file.write(target)
        rece_file.close()

    def deleteReceptorFile(self):
        os.remove(self.target_path)

    def initVinaParams(self, params):
        """add keys which are required for docking

        Args:
            params (dict): dict

        Returns:
            dict: updated params
        """
        if "exhaustiveness" not in params: params["exhaustiveness"] = None
        if "n_poses" not in params: params["n_poses"] = None
        if "min_rmsd" not in params: params["min_rmsd"] = None
        if "max_evals" not in params: params["max_evals"] = None
        if "grid_spacing" not in params: params["grid_spacing"] = None
        if "scoring_function" not in params: params["scoring_function"] = None
        if "cpu_num" not in params: params["cpu_num"] = None
        if "random_seed" not in params: params["random_seed"] = None

        return params

    def createVinaProcesses(self):
        """fill self.processes with process entity having vina, queues and cores
        """
        cores = self.avaliable_cores
        self.totalProcesses = math.ceil(cores/4)
        self.process_cores = [4 * (cores//4)]
        if self.avaliable_cores%4 != 0:
            self.process_cores.append(cores%4)
        
        self.processes = []
        for num_core in self.process_cores:
            control_queue = multiprocessing.Queue()
            compute_queue = multiprocessing.Queue()
            result_queue = multiprocessing.Queue()
            error_queue = multiprocessing.Queue()
            compute_assigned_queue = queue.Queue()

            vina_process = VinaProcess(control_queue=control_queue,
                                       compute_queue=compute_queue,
                                       result_queue=result_queue,
                                       error_queue=error_queue,
                                       compute_assigned_queue=compute_assigned_queue
                                       )
        
            self.processes.append(DockingTask.ProcessEntity(
                vina_process=vina_process,
                control_queue = control_queue,
                compute_queue=compute_queue,
                result_queue=result_queue,
                error_queue=error_queue,
                num_core=num_core,
                compute_assigned_queue=compute_assigned_queue
            ))

    def runAndInitVinaProcesses(self):
        """will pass params to vina processes and create instance of vina in vinaProcess
        """
        for process in self.processes:
            # run vina process
            process.vina_process.start()

            process.control_queue.put(VinaProcess.ParamsMessage(
                center=self.params["center"],
                box = self.params['box'],
                target_path=self.target_path,
                scoring_function=self.params['scoring_function'],
                cores_count=process.num_core,
                random_seed=self.params['random_seed'],
                exhaustiveness=self.params['exhaustiveness'],
                n_poses=self.params['n_poses'],
                min_rmsd=self.params['min_rmsd'],
                max_evals=self.params['max_evals']
            ))

            # initialize vina
            process.control_queue.put(VinaProcess.InitVinaMessage())

            while not process.control_queue.empty():
                time.sleep(5)
            
            # check of error
            if process.vina_process





    

    def getComputes(self, docking_id:str, compute_count:int = 1):
        computes = ServerHttpDockingService.getComputes(docking_id=docking_id, count=compute_count)
        return computes
    
   




    def getTarget(self)-> str:
        return ServerHttpDockingService.getDockingTarget(self.docking_id)
    
    
    def updateComputeResult(self, compute_results: list):
        """This method start a thread which updates compute result on server

        Args:
            compute_results (list): list of dict contaning compute_id and result
        """
        def threadedComputeResultUpdate(docking_id, compute_results):
            with app.app_context():
                ServerHttpDockingService.saveComputeResult(docking_id, compute_results)

        t = Thread(target=threadedComputeResultUpdate, args=(self.docking_id, compute_results), daemon=False)
        t.start()

    def getLigandBatchSize(self, old_batch_size, old_batch_time):
        if old_batch_size == -1: return self.inital_batch_size

        x = int(self.ideal_completion_time - old_batch_time)
        return max(old_batch_size + x * abs(x), self.inital_batch_size)



        
        