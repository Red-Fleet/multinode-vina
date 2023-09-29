from app import app
from threading import Thread, Lock
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
        def __init__(self, num_core) -> None:
            
            self.control_queue: multiprocessing.Queue = multiprocessing.Queue()
            self.compute_queue: multiprocessing.Queue = multiprocessing.Queue()
            self.result_queue: multiprocessing.Queue = multiprocessing.Queue()
            self.error_queue: multiprocessing.Queue = multiprocessing.Queue()
            self.computing_queue: multiprocessing.Queue = multiprocessing.Queue()

            self.createVinaProcess()
            
            self.num_core = num_core

        
        def createVinaProcess(self):
            if self.control_queue is None or self.compute_queue is None or self.result_queue is None or self.error_queue is None or self.computing_queue is None:
                raise Exception("control_queue, compute_queue, result_queue, error_queue, computing_queue cannot be empty")
            self.vina_process: VinaProcess = VinaProcess(
                                        control_queue=self.control_queue,
                                       compute_queue=self.compute_queue,
                                       result_queue=self.result_queue,
                                       error_queue=self.error_queue,
                                       computing_queue=self.computing_queue
                                    )

        def replaceVinaProcess(self):
            if self.control_queue is None or self.compute_queue is None or self.result_queue is None or self.error_queue is None or self.computing_queue is None:
                raise Exception("control_queue, compute_queue, result_queue, error_queue, computing_queue cannot be empty")
            
            # empty control and computing_queue
            while self.control_queue.empty() == False: self.control_queue.get()
            while self.computing_queue.empty() == False: self.computing_queue.get()

            self.createVinaProcess()


    def __init__(self, docking_id, avaliable_cores) -> None:

        self.docking_id = docking_id
        self.avaliable_cores = avaliable_cores
        self.target = None
        self.target_path: str = None
        self.params: dict = None
        self.master_id: str = None

        self.inital_batch_size = 10
        self.ideal_completion_time = 10 # in minutes

        self.processes:list[DockingTask.ProcessEntity] = [] # will store all process entity
        
        self.docking_details_inititalized = False # should come before starting of the docking details thread
        
        self.run_thread = Thread(target=self.run)
        self.run_thread.start()

        self.processes_lock = Lock() # for locking processes list

        ### used for getting batch size of ligands ###
        self.batch_size = -1
        self.batch_time = -1
        ########################################

    
    def run(self):
        try:
            self.getDockingDetails()
        except Exception as e:
            #######################handle this###################
            with app.app_context():
                app.logger.info("Error while fetching Docking detials: docking_id{self.docking_id}\n", e)
            
            return
        
        try:
            self.createVinaProcesses()
        except Exception as e:
            #######################handle this###################
            with app.app_context():
                app.logger.info("Error while fetching Docking detials: docking_id{self.docking_id}\n", e)
            
            return


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
        totalProcesses = math.ceil(cores/4)
        process_cores = [4] * (cores//4)
        if cores%4 != 0:
            process_cores.append(cores%4)
        
        self.processes = []
        for num_core in process_cores:
            self.processes.append(DockingTask.ProcessEntity(
                num_core=num_core,
            ))

    def runAndInitVinaProcess(self, process: ProcessEntity):
        """This will fill control_queue with target and vina params, and then start process thread 

        Args:
            process (ProcessEntity): _description_

        Raises:
            Exception: _description_
        """
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

        # run vina process
        process.vina_process.start()

        # initialize vina
        process.control_queue.put(VinaProcess.InitVinaMessage())

        while not process.control_queue.empty():
            time.sleep(5)
        
        # check for error
        if process.vina_process.is_alive() == False or process.error_queue.empty() == False:
            ################ Handle error #####################
            ################# Update Server about error ################
            error_str = ""
            if process.error_queue.empty() == False:
                error_str = str(process.error_queue.get().message)
            raise Exception("Error: docking_id({self.docking_id})" , error_str)                 
            
    def computeAssignmentThread(self):
        """This thread will assign new computes to the process.
        It keeps looking for ideal processes, once ideal process is found 
        it will ask for new batch of ligands.
        """

        while True:
            time.sleep(10) # sleep for 10 sec

            # acquire processes lock
            self.processes_lock.acquire()

            # check if all processes have computes or not
            hasComputes = True
            for process in self.processes:
                if process.compute_queue.qsize() == 0:
                    hasComputes = False
                    break
            
            if hasComputes == False:
                # get new batch of ligands
                computes = self.getComputes(docking_id=self.docking_id, compute_count=self.getLigandBatchSize())

                totalComputes = len(computes)
                for process in self.processes:
                    totalComputes += process.compute_queue.qsize()
                
                average_computes = math.ceil(totalComputes/len(self.processes))
                
                for process in self.processes:
                    put = average_computes - process.compute_queue.qsize()
                    while put>0 and len(computes)>0:
                        put -= 1
                        compute = computes.pop()
                        process.compute_queue.put(VinaProcess.ComputeMessage(
                            compute['compute_id'], compute['ligand'])
                            )
            self.processes_lock.release()

    def updateKilledThreadError(self):
        """handle error of processes which were killed due to error in vina,
        dead processes with non-empty computing_queue
        """
        for process in self.processes:
            if process.vina_process.is_alive():
                # update error
                error_compute = process.computing_queue.get()
                with app.app_context():
                    compute_id = error_compute['compute_id']
                    app.logger.error("########### Update ligand error on server: {compute_id}")
                
                process.replaceVinaProcess()
                self.runAndInitVinaProcess(process)

                
    def restartClosedProcessesThread(self):
        while(1):
            time.sleep(180) # sleep for 180 seconds
            self.processes_lock.acquire()

            self.updateKilledThreadError()
            
            self.processes_lock.release()

    def resultUpdate(self):
        results = []
            
        for process in self.processes:
            while process.result_queue.empty() == False:
                result = process.result_queue.get()
                results.append(result)
        
        ServerHttpDockingService.saveComputeResult(self.docking_id, results)

    def resultUpdateThread(self):
        while(1):
            time.sleep(600)
            self.resultUpdate()

    def errorHandler(self):
        for process in self.processes:
            error = process.error_queue.get()
            
            if isinstance(error, VinaProcess.LigandLoadError):
                with app.app_context():
                    app.logger.error("Update ligand error: {error.compute_id}")

            
    def errorHandlerThread(self):
        while(1):
            time.sleep(180)
            self.errorHandler()

            
            
    def updateAvaliableCores(self, avaliable_cores):
        self.avaliable_cores = avaliable_cores

        self.processes_lock.acquire()

        for process in self.processes:
            process.control_queue.put(VinaProcess.EndProcessMessage())
        
        # weight for all processes to end
        process_running = True
        while process_running:
            process_running = False
            for process in self.processes:
                process_running =  process.vina_process.is_alive() or process_running
            
            time.sleep(10)
        
        # adding all computes in computes list
        computes = []
        for process in self.processes:
            while process.compute_queue.empty() == False:
                computes.append(process.compute_queue.get())
        
        # updating result
        self.resultUpdate()

        # handle error of if present in error_queue
        self.errorHandler()

        # handle error of processes which were killed due to vina error (they will have non empty computing queue)
        self.updateKilledThreadError()

        # removing all old processes entities and adding new one
        self.processes = []
        self.createVinaProcesses()

        # initializing and running new processes
        for process in self.processes:
            self.runAndInitVinaProcess(process)

        self.processes_lock.release()


    def getComputes(self, docking_id:str, compute_count:int = 1):
        computes = ServerHttpDockingService.getComputes(docking_id=docking_id, count=compute_count)
        return computes
    
   




    def getTarget(self)-> str:
        return ServerHttpDockingService.getDockingTarget(self.docking_id)
    
    
    # def updateComputeResult(self, compute_results: list):
    #     """This method start a thread which updates compute result on server

    #     Args:
    #         compute_results (list): list of dict contaning compute_id and result
    #     """
    #     def threadedComputeResultUpdate(docking_id, compute_results):
    #         with app.app_context():
    #             ServerHttpDockingService.saveComputeResult(docking_id, compute_results)

    #     t = Thread(target=threadedComputeResultUpdate, args=(self.docking_id, compute_results), daemon=False)
    #     t.start()

    def getLigandBatchSize(self):
        if self.batch_size == -1:
            self.batch_size = self.inital_batch_size
            self.batch_time = time.time()
            return self.batch_size
    
        x = int(self.ideal_completion_time - (time.time() - self.batch_time))
        self.batch_size = max(self.batch_size + x * abs(x), self.inital_batch_size)
        self.batch_time = time.time()
        return self.batch_size



        
        