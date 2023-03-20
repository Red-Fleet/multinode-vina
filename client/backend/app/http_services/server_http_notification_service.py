from app import app, server, user
import requests
from app.http_services.http_error import HttpError


class ServerHttpNotificationService:
    @staticmethod
    def getWorkerNotifications():
        """return all notifications of worker

        Raises:
            Exception: _description_

        Returns:
            list: list contaning dict of docking_id
        """
        response = requests.get(server.address+"/notification/worker", auth=(user.username, user.password))
        if HttpError.isHttpError(response.status_code):
            raise Exception(str(response.status_code)+", "+str(response.text))
        

        return response.json()