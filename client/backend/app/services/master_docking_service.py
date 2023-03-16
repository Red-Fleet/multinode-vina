import datetime
from app import db, app, user
from app.http_services.server_http_docking_service import ServerHttpDockingService


class MasterDockingService:
    """MasterDockingService class is used by master to create, view, update, delete dockings
    """
    @staticmethod
    def createDock(target: str, target_name:str, ligands: str, ligands_name: str, worker_ids:list[str]):
        try:
            dockin_id = ServerHttpDockingService.createDocking(target=target, ligands=[ligands], target_name=target_name, ligands_name=ligands_name, worker_ids=worker_ids)
        except Exception as e:
            app.logger.error(e)
            raise e
        
        return dockin_id