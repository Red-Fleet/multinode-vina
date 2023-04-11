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
        self.vina: Vina = None
        self.dockingSystemThread = Thread(target=self.startDockingSystemThread)
        self.dockingSystemThread.start()
    
    def startDockingSystemThread(self):
        with app.app_context():
            # inititalizing target
            self.target = self.getTarget()
            
            # initializing vina
            self.vina = self.getVina()

            # save receptor
            self.saveReceptorInFile()

            self.dock()

    def saveReceptorInFile(self):
        temp_dir_path: str = os.path.join(str(pathlib.Path(__file__).parent.resolve()), "temp_receptors")
        if os.path.exists(temp_dir_path) == False:
            # create dir for storing temp files
            os.mkdir(temp_dir_path)

        # save receptor
        self.target_path = os.path.join(temp_dir_path, self.docking_id+"_receptor.pdbqt")
        rece_file = open(self.target_path, "w")
        rece_file.write(self.target)
        rece_file.close()

    def deleteReceptorFile(self):
        os.remove(self.target_path)

    def dock(self):
        app.logger.info("Docking Started: docking_id({self.docking_id})")
        # set receptor
        self.vina.set_receptor(self.target_path)

        # setting bounding box
        box = {"center": [-19, -38, 23], "box_size": [20, 20, 20]}

        # computing vina maps
        self.vina.compute_vina_maps(center=box["center"], box_size=box["box_size"])
    
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
                    
                    energy = self.vina.dock(exhaustiveness=32, n_poses=20)

                    

            else:
                app.logger.info("Docking Finished: docking_id({self.docking_id})")
                break

    def getComputes(self):
        computes = ServerHttpDockingService.getComputes(docking_id=self.docking_id, count=2)
        return computes
    
    def getVina(self):
        return Vina(sf_name='vina', seed=10)

    def getTarget(self)-> str:
        return ServerHttpDockingService.getDockingTarget(self.docking_id)
        