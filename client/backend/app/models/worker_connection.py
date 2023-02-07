class WorkerConnection:
    """Stores the client_id of master worker is connected to
    """
    def __init__(self) -> None:
        # for storing client_id of master
        self._connections:set = set()
    
    def addMaster(self, master_id: str):
        """for adding single master

        Args:
            master_id (str): client_id of master
        """
        self._connections.add(master_id)

    def addMasters(self, master_ids:list):
        """for adding multiple masters

        Args:
            master_ids (list): list containing client_id of master
        """
        for master_id in master_ids:
            self._connections.add(master_id)

    def deleteMaster(self, master_id: str):
        """for deleting master

        Args:
            master_id (str): client_id of master
        """
        self._connections.remove(master_id)

    def isMasterPresent(self, master_id: str)->bool:
        """for checking if master is connected to worker

        Args:
            master_id (str): client_id of master

        Returns:
            bool: true if master is connected else false
        """
        return master_id in self._connections
    
    def getMaster(self)-> list:
        """return list of master_id

        Returns:
            list: list of master_id
        """
        return list(self._connections)
        
    pass