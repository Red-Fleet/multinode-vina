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