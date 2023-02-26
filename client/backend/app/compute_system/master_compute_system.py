import threading

class MasterComputeSystem:
    def __init__(self) -> None:
        self.master_id: str = None # client_id of user who is logged in
        self.authentication = False # for keeping track if client is logged in or not
        self.computeInstances: dict[str, MasterComputeInstance] = dict() # dictonary of storing all compute instances , key = target_id, value=computeInstance 
    
    def loggined(self, master_id: str):
        """this method should be used after sucessful user authentication, this will start automatic computation and
        is first method that should run after __init__, this is basically the entry point of master compute system

        Args:
            master_id (str):  client_id of user who is logged in
        """
        self.master_id = master_id
        self.authentication = True
        #threading.Thread(target=AutomatedMasterConnectionRequestService.printThread)
    
    def startComputeInstance(self, target_id: str):
        if target_id in self.computeInstances:
            # delete if a compute Instance is already running on target_id
            self.computeInstances[target_id].deleteInstance()
        
        # start new ComputeInstance
        self.computeInstances[target_id] = MasterComputeInstance(target_id=target_id)
    
    def stopComputeInstance(self, target_id: str):
        if target_id in self.computeInstances:
            # delete if a compute Instance is already running on target_id
            self.computeInstances[target_id].deleteInstance()
    

        


class MasterComputeInstance:
    def __init__(self, target_id: str):

        self.target_id = target_id # target id of target on which computation should happen
    
    def deleteInstance(self):
        # implement this - stop all threads and delete object
        pass