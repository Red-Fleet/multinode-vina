from app.models.master_request import MasterRequest, MasterRequestState, MasterRequestDto
import datetime
from app import db, app
from app.http_services.server_http_request_service import ServerHttpRequestService
class MasterRequestService:

    @staticmethod
    def createRequest(client_id:str, worker_id:str):
        """Create new request 

        Args:
            client_id (str): _description_
            worker_id (str): _description_

        Raises:
            e: _description_
        """
        try:
            request = MasterRequest(client_id=client_id, worker_id=worker_id, create_time=datetime.datetime.now(), request_state=MasterRequestState.CREATED)
            ServerHttpRequestService.createRequest(master_id=client_id, worker_id=worker_id)
            db.session.add(request)
            db.session.commit()
        except Exception as e:
            app.logger.error(e)
            raise e
    
    def getAllRequestUsingClient(client_id:str)->list[MasterRequestDto]:
        """get all requests created by client

        Args:
            client_id (str): _description_

        Raises:
            e: _description_

        Returns:
            list[MasterRequestDto]: _description_
        """
        try:
            result = MasterRequest.query.filter_by(client_id=client_id).all()
            dtos = [MasterRequestDto.getDtoFromModel(e) for e in result]
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
            MasterRequest.query.filter_by(id=id).delete()
        except Exception as e:
            app.logger.error(e)
            raise e

    
