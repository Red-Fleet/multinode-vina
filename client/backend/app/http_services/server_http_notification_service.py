from app import app
import requests
from app.http_services.http_error import HttpError
from app import connection

class ServerHttpNotificationService:
    @staticmethod
    def getWorkerNotifications():
        """return all notifications of worker

        Raises:
            Exception: _description_

        Returns:
            list: list contaning dict of docking_id
        """
        response = requests.get(connection.address+"/notification/worker", auth=(connection.username, ""))
        if HttpError.isHttpError(response.status_code):
            raise Exception(str(response.status_code)+", "+str(response.text))
        

        return response.json()