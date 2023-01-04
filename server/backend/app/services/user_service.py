import uuid
import datetime
from app import db, app
from app.models.client import Client, ClientState, ClientStateException
from app.models.user import User
from sqlalchemy.exc import IntegrityError

class UserService:
    @staticmethod
    def authenticateUser(username: str, password_hash: str) -> str:
        """This method is used to check if user is present in database or not

        Args:
            username (str): username
            password_hash (str): hash of password

        Raises:
            Exception: exception is raised if cannot query the database

        Returns:
            str: user(if user is authenticated), None(if user is not authenticated)
        """

        try:
            user = User.query.filter_by(
                username=username, password_hash=password_hash).first()
        except Exception as e: 
            app.logger.error(e)
            raise Exception("database error")


        return user


    @staticmethod
    def createUser(username: str, password_hash: str, name: str) -> str:
        """This method is used to insert a new user in database,
        user and client tables in database are updated.

        Args:
            username (str): username
            password_hash (str): hash of password
            name (str): name of user

        Raises:
            Exception: exception is raised if cannot insert entry in database

        Returns:
            str: client id
        """
        if username == "":
            raise Exception("username cannot be null")

        client_id = str(uuid.uuid4())
        user = User(client_id=client_id, username=username,
                    password_hash=password_hash, name=name)
        client = Client(client_id=user.client_id,
                        last_connected=datetime.datetime.now(), state=ClientState.OFFLINE)

        try:
            db.session.add(user) 
            db.session.add(client) 
            db.session.commit() 
        except IntegrityError as e: 
            app.logger.error(e) 
            raise Exception("username taken")
        except Exception as e: 
            app.logger.error(e) 
            raise Exception("database error")

        return user.client_id

    