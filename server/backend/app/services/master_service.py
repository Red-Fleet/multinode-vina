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
    def createRequest(master_id: str, worker_id: str):
        """Add or update new entry in request db

        Args:
            master_id (str): client_id of master from which request is comming
            worker_id (str): client_if of worker to which request will be shared

        Raises:
            Exception: Database Error
        """
        try:
            request = Request.query.filter_by(worker_id=worker_id, master_id=master_id).first()
            
            # create new request
            if request == None:
                request = Request(worker_id=worker_id, master_id=master_id,
                                state=RequestState.CREATED, state_update_time=datetime.datetime.now())
                db.session.add(request)
            # update previous request
            else:
                x = Request.query.filter_by(worker_id=worker_id, 
                                    master_id=master_id).update(dict(state_update_time = datetime.datetime.now(), 
                                                                        state = RequestState.CREATED))
    
            db.session.commit()

        except Exception as e:
            app.logger.error(e)
            raise Exception("Database Error")

