import threading
import time
from app.services.master_request_service import MasterRequestService
from app import app

class AutomatedMasterRequestService:
    @staticmethod
    def start():
        print("AutomatedMasterRequestService: started")
        x = threading.Thread(target=AutomatedMasterRequestService.printThread)
        x.start()


    @staticmethod
    def printThread():
        with app.app_context():
            #MasterRequestService.createRequest(client_id="id1", worker_id="wd1")
            pass