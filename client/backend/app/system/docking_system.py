from app import app
from threading import Thread
from app.http_services.server_http_docking_service import ServerHttpDockingService
from vina import Vina
import os
import pathlib

class DockingSystem:
    def __init__(self, docking_id) -> None:
        self.docking_id = docking_id
        self.target: str = None
        self.target_path: str = None
        self.params: dict = None
        self.master_id: str = None
        self.vina: Vina = None
        self.dockingSystemThread = Thread(target=self.startDockingSystemThread)
        self.dockingSystemThread.start()
    
    def startDockingSystemThread(self):
        with app.app_context():
            # get docking details from server
            docking_details = self.getDockingDetails()
            self.params = docking_details["params"]
            self.target = docking_details["target"]
            self.master_id = docking_details["master_id"]
            
            # initializing vina
            self.vina = self.getVina()

            # save receptor in temp file
            self.saveReceptorInTempFolder(self.target)

            # set target/receptor in vina
            self.vina.set_receptor(self.target_path)

            # compute vina maps
            self.setVinaMap(self.vina, self.params)

            # start docking
            app.logger.info("Docking Started: docking_id({self.docking_id})")
            self.dock(self.vina, self.params)

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

    def dock(self, vina: Vina, params:dict):

        if "exhaustiveness" not in params: params["exhaustiveness"] = 8
        if "n_poses" not in params: params["n_poses"] = 20
        if "min_rmsd" not in params: params["min_rmsd"] = 1.0
        if "max_evals" not in params: params["max_evals"] = 0

        exhaustiveness = params["exhaustiveness"]
        n_poses = params["n_poses"]
        min_rmsd = params["min_rmsd"]
        max_evals= params["max_evals"]
        
        # get targets
        while True:
            computes = self.getComputes()
            results = [] # stores dict contaning 
            app.logger.info("sdfdsf")
            if len(computes) >= 1:
                # update compute result
                for compute in computes:
                    ligand = compute['ligand']
                    self.vina.set_ligand_from_string(ligand)
                    
                    self.vina.dock(exhaustiveness=exhaustiveness, 
                                            n_poses=n_poses,
                                            min_rmsd=min_rmsd,
                                            max_evals=max_evals)
                    
                    result1

                    

            else:
                app.logger.info("Docking Finished: docking_id({self.docking_id})")
                break

    def getComputes(self, docking_id:str, compute_count:int = 1):
        computes = ServerHttpDockingService.getComputes(docking_id=docking_id, count=compute_count)
        return computes
    
    def setVinaMap(self, vina:Vina, params:dict):

        if "grid_spacing" not in params: params["grid_spacing"] = 0.375

        center = [params["center_x"], params["center_y"], params["center_z"]]
        box = [params["box_size_x"], params["box_size_y"], params["box_size_z"]]

        vina.compute_vina_maps(center=center, box_size=box, spacing=params["grid_spacing"])



    def getVina(self, params:dict):
        # set default parameters if they are not set
        if "scoring_function" not in params: params["scoring_function"] = "vina"
        if "cpu_num" not in params: params["cpu_num"] = 0
        if "random_seed" not in params: params["random_seed"] = 0


        return Vina(sf_name=params["scoring_function"], 
                    cpu=params["cpu_num"],
                    seed=params["random_seed"])

    def getTarget(self)-> str:
        return ServerHttpDockingService.getDockingTarget(self.docking_id)
    
    def getDockingDetails(self, docking_id:str)-> str:
        return ServerHttpDockingService.getDockingTarget(docking_id)
        