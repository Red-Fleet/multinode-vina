import datetime
from app import app
from app.http_services.server_http_client_service import ServerHttpClientService
class ClientService:
    @staticmethod
    def getClientDetails(client_id: str)-> dict:
        """return details of a client

        Args:
            client_id (str): client_id of client

        Raises:
            e: _description_

        Returns:
            dict: keys = client_id, state, name
        """
        try:
            result = ServerHttpClientService.getClientDetails(client_id=client_id)
        except Exception as e:
            app.logger.error(e)
            raise e

        return result

    
    @staticmethod
    def getAllClients()-> list[dict]:
        """return all clients details

        Raises:
            Exception: _description_

        Returns:
            list[dict]: client_id, status, name
        """

        try:
            result = ServerHttpClientService.getAllClients()
        except Exception as e:
            app.logger.error(e)
            raise e

        return result