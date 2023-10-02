from collections.abc import Callable, Iterable, Mapping
from threading import Thread, Lock
import time
from typing import Any
from app.http_services.server_http_notification_service import ServerHttpNotificationService
from app import app, user
from app.services.docking_service import DockingService
from app.system.docking_task import DockingTask

class DockingSystem(Thread):
    def __init__(self, total_cores: int = 1,  group: None = None, target: Callable[..., object] | None = None, name: str | None = None, args: Iterable[Any] = ..., kwargs: Mapping[str, Any] | None = None, *, daemon: bool | None = None) -> None:
        super().__init__(group, target, name, args, kwargs, daemon=daemon)

        self.total_cores = total_cores
        self.docking_tasks: set[DockingTask] = set()
        self.docking_tasks_lock = Lock()


    def run(self):
        self.notification_thread = Thread(target=self.checkNotificationAndStartDockingThread)
        self.notification_thread.start()

        self.remove_ended_task_thread = Thread(target=self.removeEndedTasksThread)
        self.remove_ended_task_thread.start()

        while self.remove_ended_task_thread.is_alive() == True and self.notification_thread.is_alive() == True:
            time.sleep(600)
    
    def startDocking(self, docking_id: str):
        task = DockingTask(docking_id=docking_id, avaliable_cores=0)
        task.start()
        self.docking_tasks.add(task)

    def coresAssignment(self):
        """it distributes cores among different docking_tasks
        """
        self.docking_tasks_lock.acquire()
        
        total_tasks = len(self.docking_tasks)

        cores = [self.total_cores//total_tasks]*total_tasks
        left_cores = self.total_cores - (self.total_cores//total_tasks)*total_tasks

        i = 0
        while left_cores > 0:
            cores[i] += 1
            left_cores -= 1
            i = (i+1)%total_tasks
        
        i = 0
        for task in self.docking_tasks:
            task.updateAvaliableCores(avaliable_cores=cores[i])
            i += 1

        self.docking_tasks_lock.release()
        
    def removeEndedTasksThread(self):
        """Thread will remove the docking tasks which are finished
        """
        while True:
            time.sleep(180)
            self.docking_tasks_lock.acquire()

            removed = False
            for process in self.docking_tasks:
                if process.is_alive() == False:
                    removed = True
                    self.docking_tasks.remove(process)
            
            if removed == True:
                self.coresAssignment()
            
            self.docking_tasks_lock.release()


            
    
    def checkNotificationAndStartDockingThread():
        with app.app_context():
            while True:
                time.sleep(180)
                if user.isAuthenticated == False:
                    continue
                # check notification
                try:
                    result = ServerHttpNotificationService.getWorkerNotifications()
                    docking_ids = [x['docking_id'] for x in result]
                    if len(docking_ids) >= 1:
                        for docking_id in docking_ids:
                            DockingService.startDocking(docking_id=docking_id)
                except Exception as e:
                    app.logger.error(e)