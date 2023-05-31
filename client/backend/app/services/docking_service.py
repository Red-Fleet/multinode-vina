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




