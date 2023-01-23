from app import app, server, user
import requests
from app.http_services.http_error import HttpError

class ServerHttpConnectionRequestService:
    """This class is used by client for connecting with server

    Raises:
        Exception: _description_
        e: _description_
    """
    @staticmethod
    def createConnectionRequest(master_id:str, worker_id: str):
        """This method creates new connection request on server

        Args:
            master_id (str): _description_
            worker_id (str): _description_

        Raises:
            Exception: _description_
            e: _description_
        """
        data = {}
        data['master_id'] = master_id
        data['worker_id'] = worker_id

        try:
            response = requests.post(server.address+"/request/create", json=data, auth=(user.username, user.password))
            if HttpError.isHttpError(response.status_code):
                raise Exception(str(response.status_code)+", "+str(response.text))
        except Exception as e:
            app.logger.error(e)
            raise e
