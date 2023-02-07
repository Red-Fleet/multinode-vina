from app.http_services.server_http_connection_request_service import ServerHttpConnectionRequestService
from app import app, worker_connection
class WorkerConnectionRequestService:
    """class used by worker for getting connection requests, accepting and rejeccted them
    """
    
    @staticmethod
    def getWorkerConenctionRequests():
        """get all connection requests of worker from server

        Raises:
            e: _description_

        Returns:
            list: list contaning dict of master_id and status
        """
        try:
            result = ServerHttpConnectionRequestService.getWorkerConnectionRequests()

            # adding master id of 'ACCEPTED' connection requests
            for con in result:
                if con['state'] == 'ACCEPTED':
                    worker_connection.addMaster(con['master_id'])
        except Exception as e:
            app.logger.error(e)
            raise e

        return result
