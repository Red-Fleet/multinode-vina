import threading
from app import app
from app.http_services.server_http_docking_service import ServerHttpDockingService
import time
from threading import Thread, Lock
from app.system.docking_system import DockingSystem

class DockingService:
    dockings: dict = dict()
    docking_lock:Lock = Lock()

    @staticmethod
    def startDocking(docking_id: str):
        system = DockingSystem(docking_id=docking_id)
        DockingService.docking_lock.acquire()
        DockingService.dockings[docking_id] = system
        DockingService.docking_lock.release()

    # def __init__(self, docking_id):
    #     self.docking_id = docking_id
    #     with app.app_context():
    #         thr = threading.Thread(target=self.startDockingThread)
    #         thr.start()
    
    def startDockingThread(self):
        while True:
            computes = self.getComputes()
            print("\n\n\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ getting ligands @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            if len(computes) >= 1:
                # update compute result
                for compute in computes:
                    print("#######################################")
                    print("Computing  compute_id:", compute['compute_id'])
                    #print("Ligand:", compute['ligand'])
                time.sleep(5)

            else:
                print("Docking Finished")
                break
    
    def getComputes(self):
        computes = ServerHttpDockingService.getComputes(docking_id=self.docking_id, count=2)
        return computes


