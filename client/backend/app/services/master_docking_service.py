import datetime
from app import db, app, user
from app.http_services.server_http_docking_service import ServerHttpDockingService
from app.utils.pqbqt_utils import PdbqtUtils

class MasterDockingService:
    """MasterDockingService class is used by master to create, view, update, delete dockings
    """
    @staticmethod
    def createDock(docking_details: dict):
        try:
            # splitting pdbqt
            splitted_ligands = []
            for ligands in docking_details['ligands']:
                splitted_ligands += PdbqtUtils.splitIntoLigands(ligands)

            docking_details['ligands'] = splitted_ligands
            docking_id = ServerHttpDockingService.createDocking(docking_details)
        except Exception as e:
            app.logger.error(e)
            raise e
        
        return docking_id
    
    @staticmethod
    def getMasterDockingIds()->list[dict[str, str]]:
        """function returns all docking_id of dockings started by master

        Raises:
            Exception: _description_

        Returns:
            list[dict[str, str]]: list of dict contaning docking_id and state of docking
        """
        return ServerHttpDockingService.getMasterDockingIds()

    @staticmethod
    def getAllComputeIds(docking_id: str)-> list[str]:
        """returns all compute_ids of a docking

        Args:
            docking_id (str): docking id

        Raises:
            Exception: _description_

        Returns:
            list[str]: list contaning compute ids
        """

        return ServerHttpDockingService.getAllComputeIds(docking_id=docking_id)

