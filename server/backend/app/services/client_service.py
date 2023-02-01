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
    def getAllClients() -> list[dict]:
        """ return all clients id, state and name

        Raises:
            Exception: database error

        Returns:
            list[dict]: list of dictonary containing client_id, state, name
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
    def getClientDetails(client_id: str) -> dict:
        """return client details like name, state

        Args:
            client_id (str): client_id of client/user

        Raises:
            Exception: _description_

        Returns:
            dict: dictonary contaning name, client_id, state
        """
        try:
            state:str = Client.query.with_entities(
                Client.state
            ).filter_by(client_id=client_id).first()[0].name
            
            name: str = User.query.with_entities(
                User.name
            ).filter_by(client_id=client_id).first()[0]
            result = {
                'client_id': client_id,
                'state': state,
                'name': name
            }

        except Exception as e:
            app.logger.error(e)
            raise Exception("Database Error")

        return result