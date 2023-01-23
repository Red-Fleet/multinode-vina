from app.models.master_connection_request import MasterConnectionRequest, MasterConnectionRequestState, MasterConnectionRequestDto
import datetime
from app import db, app
from app.http_services.server_http_connection_request_service import ServerHttpConnectionRequestService


class MasterConnectionRequestService:
    """Class is used to create new 'connection request', will update client and server database

    """
    @staticmethod
    def createConnectionRequest(client_id:str, worker_id:str):
        """Create new connection request

        Args:
            client_id (str): this will be used as master_id
            worker_id (str): id of client for which request will be created

        Raises:
            e: _description_
        """
        try:
            request = MasterConnectionRequest(client_id=client_id, worker_id=worker_id, create_time=datetime.datetime.now(), request_state=MasterConnectionRequestState.CREATED)
            ServerHttpConnectionRequestService.createConnectionRequest(master_id=client_id, worker_id=worker_id)
            db.session.add(request)
            db.session.commit()
        except Exception as e:
            app.logger.error(e)
            raise e
    
    def getAllConnectionRequestUsingClient(client_id:str)->list[MasterConnectionRequestDto]:
        """get all requests created by client

        Args:
            client_id (str): _description_

        Raises:
            e: _description_

        Returns:
            list[MasterRequestDto]: _description_
        """
        try:
            result = MasterConnectionRequest.query.filter_by(client_id=client_id).all()
            dtos = [MasterConnectionRequestDto.getDtoFromModel(e) for e in result]
        except Exception as e:
            app.logger.error(e)
            raise e

        return dtos
    
    def deleteRequestUsingId(id:int):
        """delete entry using id

        Args:
            id (int): _description_

        Raises:
            e: _description_
        """
        try:
            MasterConnectionRequest.query.filter_by(id=id).delete()
        except Exception as e:
            app.logger.error(e)
            raise e

    
