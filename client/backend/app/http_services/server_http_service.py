from app import app
import requests
from app.http_services.http_error import HttpError
class ServerHttpService:


    @staticmethod
    def connectWithServer(server_addr: str, clientId: str)-> str:
        """Method will return client_id

        Args:
            username (str): client_id/username

        Raises:
            Exception: _description_

        Returns:
            str: client_id
        """
        data = {}
        data['client_id'] = clientId

        try:
            response = requests.post(server_addr+"/user/connect", json=data)
            if HttpError.isHttpError(response.status_code):
                raise Exception(str(response.status_code)+", "+str(response.text))
        except Exception as e:
            app.logger.error(e)
            raise e
        
        return response.json()['client_id']


