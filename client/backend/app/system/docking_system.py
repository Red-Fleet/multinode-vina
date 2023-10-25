from collections.abc import Callable, Iterable, Mapping
from threading import Thread, Lock
import time
from typing import Any
from app.http_services.server_http_notification_service import ServerHttpNotificationService
from app import app, user
from app.system.docking_task import DockingTask
import random

class DockingSystem(Thread):
    def __init__(self, total_cores: int = 1,  group: None = None, target: Callable[..., object] | None = None, name: str | None = None, args: Iterable[Any] = ..., kwargs: Mapping[str, Any] | None = None, *, daemon: bool | None = None) -> None:
        super().__init__(group, target, name, args, kwargs, daemon=daemon)

        self.info("DockingSystem(__init__): method started")
        self.total_cores = total_cores
        self.docking_tasks: dict[str, DockingTask] = dict()
        self.docking_tasks_lock = Lock()
        self.info("DockingSystem(__init__): method finished")

    def run(self):
        self.info("DockingSystem(run): method started")
        self.notification_thread = Thread(target=self.checkNotificationAndStartDockingThread, daemon=True)
        self.notification_thread.start()

        self.remove_ended_task_thread = Thread(target=self.coreAssignmentThread, daemon=True)
        self.remove_ended_task_thread.start()

        while self.remove_ended_task_thread.is_alive() == True and self.notification_thread.is_alive() == True:
            time.sleep(10)

        self.info("DockingSystem(run): method finished")
    
    def startDocking(self, docking_id: str):
        try:
            self.docking_tasks_lock.acquire()
            if docking_id in self.docking_tasks: return

            task = DockingTask(docking_id=docking_id, avaliable_cores=0)
            task.daemon = True
            task.start()
            self.docking_tasks[docking_id] = task
            self.info("DockingSystem(startDocking): Created DockingTask for docking_id: "+ str(docking_id))
        except Exception as e:
            self.error("DockingSystem(startDocking): " + str(e))
        finally:
            self.docking_tasks_lock.release()

    def coresAssignment(self):
        """it distributes cores among different docking_tasks
        """
        total_tasks = len(self.docking_tasks)
        if total_tasks == 0: return
        cores = [self.total_cores//total_tasks]*total_tasks
        left_cores = self.total_cores - (self.total_cores//total_tasks)*total_tasks

        i = 0
        while left_cores > 0:
            cores[i] += 1
            left_cores -= 1
            i = (i+1)%total_tasks
        
        i = 0
        for task in self.docking_tasks.values():
            try:
                if cores[i] != task.avaliable_cores:
                    task.updateAvaliableCores(cores[i])
                    
            except Exception as e:
                print("Closing every thing: ", e)
                
            i += 1
        
        self.info("DockingSystem(coresAssignment): Distribution of cores among DockingTask finished")

        
    def coreAssignmentThread(self):
        """Thread will assign cores and remove the docking tasks which are finished
        """
        self.info("DockingSystem(removeEndedTasksThread): thread started")
        while True:
            try:
                time.sleep(30)
                self.docking_tasks_lock.acquire()

                remove = []
                
                for docking_id, task in self.docking_tasks.items():
                    if task.is_alive() == False:
                        remove.append(docking_id)

                for docking_id in remove:
                    self.info("DockingSystem(removeEndedTasksThread): DockingThread with docking_id(" + str(docking_id) + ") removed")
                    del self.docking_tasks[docking_id]
                
                self.coresAssignment()

                for process in self.docking_tasks.values():
                    self.info("#####################:docking_id(" + str(process.docking_id) + ") , cores:" + str(process.avaliable_cores) + ", alive:" + str(process.is_alive()))


            except Exception as e:
                self.error("DockingSystem(removeEndedTasksThread): " + str(e))
            finally:
                self.docking_tasks_lock.release()



            
    
    def checkNotificationAndStartDockingThread(self):
        self.info("DockingSystem(checkNotificationAndStartDockingThread): thread started")
        
        while True:
            try:
                time.sleep(5)
                if user.isAuthenticated == False:
                    continue
                # check notification
                print("Checking Notification")
                
                with app.app_context():
                    result = ServerHttpNotificationService.getWorkerNotifications()
                if isinstance(result, list) and len(result) > 0:
                    docking_ids = [x['docking_id'] for x in result]
                    if len(docking_ids) >= 1:
                        for docking_id in docking_ids:
                            self.info("DockingSystem(checkNotificationAndStartDockingThread): received notification of docking_id: "+ str(docking_id))
                            th = Thread(target=self.startDocking, args=(docking_id,))
                            th.start()
            except Exception as e:
                self.error("DockingSystem(checkNotificationAndStartDockingThread) Error:" + str(e))

    def info(self, message):
        # print(message)
        # def infoThread(message):
        with app.app_context():
            app.logger.info(message)
        
        # thread = Thread(target=infoThread, args=(message,))
        # thread.start()

    def error(self, message):
        # print(message)
        # def errorThread(message):
        with app.app_context():
            app.logger.error(message)
        
        # thread = Thread(target=errorThread, args=(message,))
        # thread.start()