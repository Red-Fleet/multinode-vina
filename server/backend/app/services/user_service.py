import uuid
import datetime
from app import db, app
from app.models.client import Client, ClientState, ClientStateException
from sqlalchemy.exc import IntegrityError

class UserService:
    @staticmethod
    def authenticateUser(client_id: str) -> str:
        """This method is used to check if user is present in database or not

        Args:
            client_id (str): username/client_id
        Raises:
            Exception: exception is raised if cannot query the database

        Returns:
            str: user(if user is authenticated), None(if user is not authenticated)
        """

        try:
            client = Client.query.filter_by(
                client_id=client_id).first()
        except Exception as e: 
            app.logger.error(e)
            raise Exception("database error")


        return client


    @staticmethod
    def connect(client_id: str) -> str:
        """This method is used to insert a new client in database.
        Args:
            client_id (str): username/client_id

        Raises:
            Exception: exception is raised if cannot insert entry in database

        Returns:
            str: client id
        """
        client = Client.query.filter_by(client_id=client_id).first()

        if client is None:
            client = Client(client_id=client_id,
                        last_connected=datetime.datetime.now(), state=ClientState.ONLINE)

            try:
                db.session.add(client) 
                db.session.commit() 
                
            except IntegrityError as e: 
                pass
            except Exception as e: 
                app.logger.error(e) 
                raise Exception("database error")

        return client.client_id

    