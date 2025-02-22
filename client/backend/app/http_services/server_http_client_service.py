from app import app, connection
import requests
from app.http_services.http_error import HttpError

class ServerHttpClientService:
    @staticmethod
    def getClientDetails(client_id: str):
        """return dict containing details of client

        Args:
            client_id (str): client_id of client

        Raises:
            Exception: _description_

        Returns:
            dict: client_id, state, name
        """
        body = {'client_id': client_id}
        response = requests.get(connection.address+"/client/details", json=body, auth=(connection.username, ""))
        if HttpError.isHttpError(response.status_code):
            raise Exception(str(response.status_code)+", "+str(response.text))
        
        return response.json()

    @staticmethod
    def getAllClients()-> list[dict]:
        """return all clients details

        Raises:
            Exception: _description_

        Returns:
            list[dict]: client_id, status, name
        """
        try:
            response = requests.get(connection.address+"/client/all", auth=(connection.username, ""))
            if HttpError.isHttpError(response.status_code):
                raise Exception(str(response.status_code)+", "+str(response.text))
        except Exception as e:
            app.logger.error(e)
            raise e

        return response.json()