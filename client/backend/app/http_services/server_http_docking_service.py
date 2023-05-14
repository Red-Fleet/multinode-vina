from app import app, server, user
import requests
from app.http_services.http_error import HttpError


class ServerHttpDockingService:

    @staticmethod
    def createDocking(docking_details: dict)->str:
        """Create new docking task

        Raises:
            Exception: _description_

        Returns:
            str: docking_id
        """

        response = requests.post(server.address+"/docking/create", json=docking_details,auth=(user.username, user.password))
        if HttpError.isHttpError(response.status_code):
            raise Exception(str(response.status_code)+", "+str(response.text))
        

        return response.json()["docking_id"]
    
    @staticmethod
    def getComputes(docking_id: str, count: int):
        """return list of dict contaning compute_id and ligands

        Args:
            docking_id (str): _description_
            count (int): _description_

        Raises:
            Exception: _description_

        Returns:
            _type_: _description_
        """
        body = {
            "docking_id": docking_id,
            "count": count
        }

        response = requests.get(server.address+"/docking/computes", json=body,auth=(user.username, user.password))
        if HttpError.isHttpError(response.status_code):
            raise Exception(str(response.status_code)+", "+str(response.text))
        

        return response.json()
    
    @staticmethod
    def getDockingTarget(docking_id:str) -> str:
        """returns target pdbqt using docking_id

        Args:
            docking_id (str): _description_

        Raises:
            Exception: _description_

        Returns:
            str: target
        """
        body = {
            "docking_id": docking_id
        }

        response = requests.get(server.address+"/docking/target", json=body, auth=(user.username, user.password))

        if HttpError.isHttpError(response.status_code):
            raise Exception(str(response.status_code)+", "+str(response.text))
        
        return response.json()['target']
    

    @staticmethod
    def getDockingDetails(docking_id:str) -> str:
        """returns target pdbqt using docking_id

        Args:
            docking_id (str): _description_

        Raises:
            Exception: _description_

        Returns:
            str: target
        """
        body = {
            "docking_id": docking_id
        }

        response = requests.get(server.address+"/docking/details", json=body, auth=(user.username, user.password))

        if HttpError.isHttpError(response.status_code):
            raise Exception(str(response.status_code)+", "+str(response.text))
        
        return response.json()

