from app import app, server, user
import requests
from app.http_services.http_error import HttpError


class ServerHttpDockingService:

    @staticmethod
    def createDocking(target: str, target_name:str, ligands: list[str], ligands_name: str, worker_ids:list[str])->str:
        """Create new docking task

        Raises:
            Exception: _description_

        Returns:
            str: docking_id
        """
        body = {
            'target': target,
            'target_name': target_name,
            'ligands': ligands,
            'ligands_name': ligands_name,
            'worker_ids': worker_ids
        }
        response = requests.post(server.address+"/docking/create", json=body,auth=(user.username, user.password))
        if HttpError.isHttpError(response.status_code):
            raise Exception(str(response.status_code)+", "+str(response.text))
        

        return response.json()["docking_id"]