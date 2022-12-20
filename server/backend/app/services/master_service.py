import uuid
import datetime
from app import db, app
from app.models.client import Client
from app.models.user import User
from app.models.request import Request, RequestState


class MasterService:

    @staticmethod
    def getAllClients() -> list[dict]:
        """ return all clients id and state

        Raises:
            Exception: database error

        Returns:
            list[dict]: list of dictonary containing client_id and state
        """
        try:
            result = Client.query.with_entities(
                Client.client_id, Client.state).all()
            result = [{'client_id': row[0],
                       'state': row[1].name,
                       'name': User.query.with_entities(User.name).filter_by(client_id=row[0]).first()[0]}
                      for row in result]
        except Exception as e:
            app.logger.error(e)
            raise Exception("Database Error")
        return result

    @staticmethod
    def createRequest(request_from: str, request_to: str):
        """Add or update new entry in request db

        Args:
            request_from (str): client_id of client from which request is comming
            request_to (str): client_if of client to which request will be shared

        Raises:
            Exception: Database Error
        """
        try:
            request = Request.query.filter_by(request_from=request_from, request_to=request_to).first()
            
            # create new request
            if request == None:
                request = Request(request_from=request_from, request_to=request_to,
                                state=RequestState.CREATED, state_update_time=datetime.datetime.now())
                db.session.add(request)
            # update previous request
            else:
                x = Request.query.filter_by(request_from=request_from, 
                                    request_to=request_to).update(dict(state_update_time = datetime.datetime.now(), 
                                                                        state = RequestState.CREATED))
    
            db.session.commit()

        except Exception as e:
            app.logger.error(e)
            raise Exception("Database Error")

