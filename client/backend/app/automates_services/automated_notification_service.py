import threading
import time
from app.http_services.server_http_notification_service import ServerHttpNotificationService
from app import app, user
import time
from app.services.docking_service import DockingService
import os

class AutomatedNotificationService:

    @staticmethod
    def start():
        print("AutomatedNotificationService: started")
        x = threading.Thread(target=AutomatedNotificationService.checkNotificationAndStartDocking)
        x.start()


    # @staticmethod
    # def printThread():
    #     with app.app_context():
    #         #MasterRequestService.createRequest(client_id="id1", worker_id="wd1")
    #         pass

    def checkNotificationAndStartDocking():
        with app.app_context():
            while True:
                if user.isAuthenticated == False:
                    time.sleep(30)
                    continue
                # check notification
                try:
                    start_time = time.process_time()
                    result = ServerHttpNotificationService.getWorkerNotifications()
                    end_time = time.process_time()
                    app.logger.info("Time taken for fetching notifications: " + str(end_time-start_time) + " seconds")
                    docking_ids = [x['docking_id'] for x in result]
                    if len(docking_ids) >= 1:
                        for docking_id in docking_ids:
                            DockingService.startDocking(docking_id=docking_id)
                    
                    else:
                        time.sleep(30)
                except Exception as e:
                    app.logger.error(e)
                    time.sleep(30)
