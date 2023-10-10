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
from typing import Any
from collections.abc import Callable, Iterable, Mapping
import random

class DockingTask(Thread):

    class ProcessEntity:
        def __init__(self, id: int, num_core: int) -> None:
            self.id = id
            self.control_queue: multiprocessing.Queue = multiprocessing.Queue()
            self.compute_queue: multiprocessing.Queue = multiprocessing.Queue()
            self.result_queue: multiprocessing.Queue = multiprocessing.Queue()
            self.error_queue: multiprocessing.Queue = multiprocessing.Queue()
            self.computing_queue: multiprocessing.Queue = multiprocessing.Queue()
            self.logs_queue: multiprocessing.Queue = multiprocessing.Queue()
            self.process_ended_event: multiprocessing.Event = multiprocessing.Event()
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
                                       computing_queue=self.computing_queue,
                                       logs_queue=self.logs_queue,
                                       process_ended_event = self.process_ended_event
                                    )

        def replaceVinaProcess(self):
            if self.control_queue is None or self.compute_queue is None or self.result_queue is None or self.error_queue is None or self.computing_queue is None:
                raise Exception("control_queue, compute_queue, result_queue, error_queue, computing_queue cannot be empty")
            
            # empty control and computing_queue
            while self.control_queue.empty() == False: self.control_queue.get()
            while self.computing_queue.empty() == False: self.computing_queue.get()

            self.process_ended_event = multiprocessing.Event() # new event

            self.createVinaProcess()


    def __init__(self, docking_id, avaliable_cores, group: None = None, target: Callable[..., object] | None = None, name: str | None = None, args: Iterable[Any] = ..., kwargs: Mapping[str, Any] | None = None, *, daemon: bool | None = None) -> None:
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        
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

        self.processes_lock = Lock() # for locking processes list

        ### used for getting batch size of ligands ###
        self.batch_size = -1
        self.batch_time = -1
        ########################################
        

        ###### flag for exiting task ##
        self.exitTask = False  # if true run will stop

        self.info("DockingTask(__init__)[docking_id("+ str(self.docking_id) +"]: DockingTask created")

    
    def run(self):
        
        self.info("DockingTask(run)[docking_id("+ str(self.docking_id) +"]: started")
        self.processes_lock.acquire()
        try:
            self.getDockingDetails()
        except Exception as e:
            #######################handle this###################
            self.exitTask = True
            self.error("DockingTask(run)[docking_id("+ str(self.docking_id) +"]: Error while fetching docking details\n" + str(e))
            return # stop this task
        
        try:
            self.createVinaProcesses()
            self.info("DockingTask(run)[docking_id("+ str(self.docking_id) +"]: ProcessEntity Created")
        except Exception as e:
            #######################handle this###################
            self.exitTask = True
            self.error("DockingTask(run)[docking_id("+ str(self.docking_id) +"]: Error while creating Vina Processes\n" + str(e))
            return # stop this task

        try:
            self.info("DockingTask(run)[docking_id("+ str(self.docking_id) +"]: Initializing vina processes")
            for process in self.processes:
                self.runAndInitVinaProcess(process)
        except Exception as e:
            #######################handle this, send error to server###################
            self.exitTask = True
            self.error("DockingTask(run)[docking_id("+ str(self.docking_id) +"]: Error while Initializing vina processes and Creating Grid Map\n" + str(e))
            return # stop this task

        self.processes_lock.release()
        
        self.docking_details_inititalized = True

        try:
            self.info("DockingTask(run)[docking_id("+ str(self.docking_id) +"]: Starting Threads")
            self.compute_assignment_thread = Thread(target = self.computeAssignmentThread)
            self.compute_assignment_thread.start()

            self.result_update_thread = Thread(target=self.resultUpdateThread)
            self.result_update_thread.start()

            # self.error_handler_thread = Thread(target=self.errorHandlerThread)
            # self.error_handler_thread.start()

            self.restart_closed_process_thread = Thread(target=self.restartClosedProcessesThread)
            self.restart_closed_process_thread.start()

            self.logs_thread = Thread(target=self.printVinaProcessLogsThread)
            self.logs_thread.start()
        
        except Exception as e:
            self.error("DockingTask(run)[docking_id("+ str(self.docking_id) +"]: Error while Thread creation")
            
        # while True:
        #     time.sleep(10)
        #     if  self.exitTask == True:
        #         return

        while   (self.compute_assignment_thread is not None) and \
                (self.compute_assignment_thread.is_alive() is True) and \
                (self.result_update_thread is not None) and \
                (self.result_update_thread.is_alive() is True) and \
                (self.restart_closed_process_thread is not None) and \
                (self.restart_closed_process_thread.is_alive() is True):
            time.sleep(10)
            if  self.exitTask == True:
                return
                 
    def getDockingDetails(self):
        """will receive docking details from server(for given docking_id). And save target in temp folder
        """
        with app.app_context():
            docking_details = ServerHttpDockingService.getDockingDetails(self.docking_id)
        self.params = self.initVinaParams(docking_details["params"])
        self.target = docking_details["target"]
        self.master_id = docking_details["master_id"]

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
        """delete receptor file after docking finishes
        """
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
        params['center'] = [float(params['center_x']), float(params['center_y']), float(params['center_z'])]
        params['box'] = [float(params['box_size_x']), float(params['box_size_y']), float(params['box_size_z'])]
        return params

    def createVinaProcesses(self):
        """fill self.processes with process entity having vina, queues and cores
        """
        cores = self.avaliable_cores
        process_cores = [4] * (cores//4)
        if cores%4 != 0:
            process_cores.append(cores%4)
        
        self.processes = []
        for i in range(len(process_cores)):
            self.processes.append(DockingTask.ProcessEntity(
                id = i,
                num_core= process_cores[i],
            ))
        
        self.info("DockingTask(createVinaProcesses)[docking_id("+ str(self.docking_id) +"]: Total process created = " + str(len(self.processes)))
            

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
        
        while process.control_queue.empty() == False and process.vina_process.is_alive() == True:
            time.sleep(5)
        
        
        # check for error
        if process.vina_process.is_alive() == False or process.error_queue.empty() == False:
            ################ Handle error #####################
            ################# Update Server about error ################
            error_str = ""
            if process.error_queue.empty() == False:
                error_str = str(process.error_queue.get().message)
            
            raise Exception(f"Error: docking_id({self.docking_id})" , error_str) 
        
        self.info("DockingTask(runAndInitVinaProcess)[docking_id("+ str(self.docking_id) +"][Process id:"+str(process.id)+"]: VinaProcess running (" + str(process)+")")              

    def assignComputesToProcesses(self, computes: list[VinaProcess.ComputeMessage]):
        totalComputes = len(computes)
        for process in self.processes:
            totalComputes += process.compute_queue.qsize()
        
        average_computes = math.ceil(totalComputes/len(self.processes))
        print("assignining computes to process queues")
        for process in self.processes:
            put = average_computes - process.compute_queue.qsize()
            while put>0 and len(computes)>0:
                put -= 1
                compute = computes.pop()
                process.compute_queue.put(compute)

    def computeAssignmentThread(self):
        """This thread will assign new computes to the process.
        It keeps looking for ideal processes, once ideal process is found 
        it will ask for new batch of ligands.
        """
        self.info("DockingTask(computeAssignmentThread)[docking_id("+ str(self.docking_id) +"]: Running")
        while True and self.exitTask==False:
            try:
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
                    computes = [VinaProcess.ComputeMessage(compute['compute_id'], compute['ligand']) for compute in computes]
                    self.assignComputesToProcesses(computes=computes)
                    self.info("DockingTask(computeAssignmentThread)[docking_id("+ str(self.docking_id) +"]: "+ str(len(computes)) + " computes fetched")
                    
            except Exception as e:
                self.error("DockingTask(computeAssignmentThread): " + str(e))
            finally:
                self.processes_lock.release()

    def updateKilledProcessError(self, process: ProcessEntity):
        if process.vina_process.is_alive() == True:
            self.error("DockingTask(updateKilledProcessError)[docking_id("+ str(self.docking_id) +"]: Cannot update error of running process")
            return
        
        error_compute = process.computing_queue.get()
        
        compute_id = error_compute.compute_id
        ####################### handle this ###############################
        self.info("DockingTask(updateKilledThreadError)[docking_id("+ str(self.docking_id) +"][Process id:"+str(process.id)+"]: Vina killed, Error in ligand pdbqt, compute_id(" + str(compute_id)+ ")")
        

    def replaceKilledVinaProcesses(self):
        """handle error of processes which were killed due to error in vina while docking ligand
         - dead processes with non-empty computing_queue
        """
        for process in self.processes:
            if process.vina_process.is_alive() ==False:
                if process.computing_queue.empty() == False:
                    # process is dead and it is killed due to error in ligand
                    # update error
                    self.updateKilledProcessError(process)

                    process.replaceVinaProcess()
                    self.runAndInitVinaProcess(process)

                    self.info("DockingTask(updateKilledThreadError)[docking_id("+ str(self.docking_id) +"][Process id:"+str(process.id)+"]: Killed Process Restarted")
                else:
                    self.exitTask = True
                    self.info("DockingTask(updateKilledThreadError)[docking_id("+ str(self.docking_id) +"]: Vina killed, Error in target pdbqt or grid map generation")
              
    def restartClosedProcessesThread(self):
        """thread for restaring processes that were killed due to error in vina
        """
        self.info("DockingTask(restartClosedProcessesThread): Running")
        while True and self.exitTask==False:
            time.sleep(10) # sleep for 180 seconds
            self.processes_lock.acquire()

            try:
                self.replaceKilledVinaProcesses()
            except Exception as e:
                self.error("DockingTask(restartClosedProcessesThread)[docking_id("+ str(self.docking_id) +"]: Error\n", str(e))
            finally:
                self.processes_lock.release()

    def resultUpdate(self, results):
        """updates result to the server
        """
        if len(results) > 0:
            self.info("DockingTask(resultUpdate)[docking_id("+ str(self.docking_id) +"]: result updating")
            ServerHttpDockingService.saveComputeResult(self.docking_id, results)
    
    def getResultsFromQueues(self):
        results = []

        for process in self.processes:
            while process.result_queue.empty() == False:
                try:
                    self.info("DockingTask(getResultsFromQueues)[docking_id("+ str(self.docking_id) +"]: que size:" + str(process.result_queue.qsize()))
                    result = process.result_queue.get(timeout=1)
                    results.append({"compute_id": result.compute_id, "result": result.result})
                except:
                    break

        return results

    def resultUpdateThread(self):
        """thread will update result to server
        """
        self.info("DockingTask(resultUpdateThread)[docking_id("+ str(self.docking_id) +"]: Running")
        while True and self.exitTask==False:
            time.sleep(10)
            try:
                try:
                    self.processes_lock.acquire()
                    results = self.getResultsFromQueues()
                finally:
                    self.processes_lock.release()

                self.resultUpdate(results)
            except Exception as e:
                self.error("DockingTask(resultUpdateThread)[docking_id("+ str(self.docking_id) +"]: Error\n", str(e))

    # def errorHandler(self): # not using this
    #     """handle error present in error queue of processes
    #     """
        
    #     for process in self.processes:
    #         if process.error_queue.empty() == False:
    #             error = process.error_queue.get()
                
    #             if isinstance(error, VinaProcess.Error):
                    
    #                 app.logger.error(f"Update ligand error: {error.compute_id}")


            
    # def errorHandlerThread(self): # not using this
    #     """thread used to handle error present in error_queue of processes
    #     """
    #     self.info("DockingTask(errorHandlerThread): Running")
    #     while True:
    #         time.sleep(10)
    #         try:
    #             self.errorHandler()
    #         except Exception as e:
    #             self.error("DockingTask(errorHandlerThread)[docking_id("+ str(self.docking_id) +"]: Error\n", str(e))


    def printVinaProcessLogs(self):
        for process in self.processes:
            while process.logs_queue.empty() == False:
                self.info("Vina Logs[docking_id("+ str(self.docking_id) +"]: " + str(process.logs_queue.get()))
    
    def printVinaProcessLogsThread(self):
        while True:
            try:
                time.sleep(10)
                self.printVinaProcessLogs()
            except: 

                pass
            
    def updateAvaliableCores(self, avaliable_cores):
        """Used to change alloted cores to a Docking task.
        - Stops all currently running processes and start new ones acc. to required cores 

        Args:
            avaliable_cores (_type_): _description_
        """
        while self.docking_details_inititalized == False:
            time.sleep(10) # wait for docking details to get initialized

        try:
            self.processes_lock.acquire()
            self.info("DockingTask(updateAvaliableCores)[docking_id("+ str(self.docking_id) +"]: Updating Cores")
            self.avaliable_cores = avaliable_cores
            # if self.is_alive() == False:
            #     return
            
            for process in self.processes:
                process.control_queue.put(VinaProcess.EndProcessMessage())
            
            # weight for all processes to end
            # process_running = True
            # while process_running:
            #     process_running = False
            #     for process in self.processes:
            #         self.info("DockingTask(updateAvaliableCores)[docking_id("+ str(self.docking_id) +"]:process id:" + str(process.id) + ", status:" + str(process.vina_process.is_alive()))
            #         process_running =  process.vina_process.is_alive() or process_running
            #     self.info("DockingTask(updateAvaliableCores)[docking_id("+ str(self.docking_id) +"]:Vina Processes still running")
            #     time.sleep(10)
            
            for process in self.processes:
                process.process_ended_event.wait()
            
            self.info("DockingTask(updateAvaliableCores)[docking_id("+ str(self.docking_id) +"]:result updating")
            #updating result
            results = self.getResultsFromQueues()
            self.info("DockingTask(updateAvaliableCores)[docking_id("+ str(self.docking_id) +"]:got results")
           
            self.resultUpdate(results=results)
            

            for process in self.processes:
                process.vina_process.terminate()
                process.vina_process.join()
            
            self.info("DockingTask(updateAvaliableCores)[docking_id("+ str(self.docking_id) +"]:all processes closed")
            # adding all computes in computes list
            computes = []
            for process in self.processes:
                while process.compute_queue.empty() == False:
                    computes.append(process.compute_queue.get())
            

            
            
            # handle error of if present in error_queue
            # self.errorHandler()
            self.info("DockingTask(updateAvaliableCores)[docking_id("+ str(self.docking_id) +"]:updating ligand error")
            # handle error of processes which were killed due to vina error (they will have non empty computing queue)
            for process in self.processes:
                if process.vina_process.is_alive() ==False and process.computing_queue.empty()==False:
                    # process is dead and it is killed due to error in ligand
                    # update error
                    self.updateKilledProcessError(process)
            
            self.info("DockingTask(updateAvaliableCores)[docking_id("+ str(self.docking_id) +"]:creating process entitites")
            # removing all old processes entities and adding new one
            self.processes = []
            self.createVinaProcesses()
            self.info("DockingTask(updateAvaliableCores)[docking_id("+ str(self.docking_id) +"]:initializring")
            # initializing and running new processes
            for process in self.processes:
                self.runAndInitVinaProcess(process)
            self.info("DockingTask(updateAvaliableCores)[docking_id("+ str(self.docking_id) +"]:all processes closed")
            # reassign computes
            self.assignComputesToProcesses(computes=computes)

            self.info("DockingTask(updateAvaliableCores)[docking_id("+ str(self.docking_id) +"]: reassignig computes")
        
        except Exception as e:
            self.exitTask = True
            self.info("DockingTask(updateAvaliableCores)[docking_id("+ str(self.docking_id) +"]: Error\n" + str(e))
            ######################333 Update to server ################################33
        finally:
            self.processes_lock.release()


    def getComputes(self, docking_id:str, compute_count:int = 1):
        """fetches computes/ligands from server

        Args:
            docking_id (str): docking_id 
            compute_count (int, optional): number of computes/ligands to get from server. Defaults to 1.

        Returns:
            _type_: _description_
        """
        computes = ServerHttpDockingService.getComputes(docking_id=docking_id, count=compute_count)
        return computes
    

    def getTarget(self)-> str:
        """fetches target from server

        Returns:
            str: _description_
        """
        return ServerHttpDockingService.getDockingTarget(self.docking_id)
     

    def getLigandBatchSize(self):
        """returns number of computes/ligands to fetch from server

        Returns:
            _type_: _description_
        """
        if self.batch_size == -1:
            self.batch_size = self.inital_batch_size
            self.batch_time = time.time()
            return self.batch_size
    
        x = int(self.ideal_completion_time - (time.time() - self.batch_time))
        self.batch_size = max(self.batch_size + x * abs(x), self.inital_batch_size)
        self.batch_time = time.time()
        return self.batch_size


    def info(self, message):
        with app.app_context():
            app.logger.info(message)

    def error(self, message):
        with app.app_context():
            app.logger.error(message)


        
        