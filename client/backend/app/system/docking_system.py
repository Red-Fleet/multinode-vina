from app import app
from threading import Thread
from app.http_services.server_http_docking_service import ServerHttpDockingService

class DockingSystem:
    def __init__(self, docking_id) -> None:
        self.docking_id = docking_id
        self.target: str = None
        self.dockingSystemThread = Thread(target=self.startDockingSystemThread)
        self.dockingSystemThread.start()
    
    def startDockingSystemThread(self):
        with app.app_context():
            self.target = self.getTarget()
            print(self.target)

    def getTarget(self)-> str:
        return ServerHttpDockingService.getDockingTarget(self.docking_id)
        