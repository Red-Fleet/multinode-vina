import uuid
import datetime
from app import db, app
from app.models.client import Client, ClientState, ClientStateException
from app.models.user import User
from app.models.request import Request, RequestState

class ClientService:

    @staticmethod
    def updateState(client_id, state):
        """Update State of client using client_id

        Args:
            client_id (_type_): client_id (primary key of client table)
            state (_type_): new state of client

        Raises:
            Exception: raise exception on error
        """

        try:
            Client.query.filter_by(client_id=client_id).update(dict(state=ClientState.fromStr(state)))
            db.session.commit()
        except ClientStateException as e:
            raise e
        except Exception as e:
            app.logger.error(e)
            raise Exception("Database Error")
        

    @staticmethod
    def rejectComputeRequest(master_id, worker_id):
        """Reject Compute request from master

        Args:
            master_id (_type_): client_id of master
            worker_id (_type_): client_id of worker

        Raises:
            Exception: raise exception on error
        """
        try:
            Request.query.filter_by(
                master_id=master_id, 
                worker_id=worker_id).update(
                    dict(state=ClientState.fromStr(
                        state_update_time = datetime.datetime.now(),
                        state = RequestState.REJECTED
                    )))
            db.session.commit()
        except Exception as e:
            app.logger.error(e)
            raise Exception("Database Error")