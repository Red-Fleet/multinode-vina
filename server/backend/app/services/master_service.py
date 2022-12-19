import uuid
import datetime
from app import db, app
from app.models.client import Client
from app.models.user import User


class MasterService:

    @staticmethod
    def getAllClients()-> list[dict]:
        """ return all clients id and state

        Raises:
            Exception: database error

        Returns:
            list[dict]: list of dictonary containing client_id and state
        """
        try:
            result = Client.query.with_entities(Client.client_id, Client.state).all()
            result = [{'client_id': row[0], 
                'state': row[1].name, 
                'name': User.query.with_entities(User.name).filter_by(client_id=row[0]).first()[0]} 
                for row in result]
        except Exception as e:
            app.logger.error(e)
            raise Exception("Database Error")
        return result
