import datetime
from app import db, app, user
from app.http_services.server_http_connection_request_service import ServerHttpConnectionRequestService


class MasterConnectionRequestService:
    """Class is used to create new 'connection request', will update server database

    """
    @staticmethod
    def createConnectionRequest(worker_id:str):
        """Create new connection request

        Args:
            client_id (str): this will be used as master_id
            worker_id (str): id of client for which request will be created

        Raises:
            e: _description_
        """
        try:
            ServerHttpConnectionRequestService.createConnectionRequest(master_id=user.client_id, worker_id=worker_id)
        except Exception as e:
            app.logger.error(e)
            raise e

    @staticmethod
    def getAllConnectionRequest()->list:
        """get all connection requests created by client from server

        Args:
            client_id (str): master_id(client who created connecton request)

        Raises:
            e: _description_

        Returns:
            list: list contaning dict of worker_id and status
        """
        try:
            result = ServerHttpConnectionRequestService.getAllConnectionRequests(master_id=user.client_id)
        except Exception as e:
            app.logger.error(e)
            raise e

        return result
    

    
