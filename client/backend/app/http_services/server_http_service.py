from app import app, server, user
import requests
from app.http_services.http_error import HttpError
class ServerHttpService:

    @staticmethod
    def loginToServer(server_addr: str, username:str, password: str):
        """Methods connects client to server and gets user details 

        Args:
            username (str): username of client
            password (str): password of client

        Returns:
            dict: username, name, client_id
        """
        try:
            response = requests.get(server_addr+"/user/login", auth=(username, password))
            if HttpError.isHttpError(response.status_code):
                raise Exception(str(response.status_code)+", "+str(response.text))
        except Exception as e:
            app.logger.error(e)
            raise e

        return response.json()

    @staticmethod
    def registerToServer(server_addr: str, username:str, password:str, name: str)-> str:
        """Method will return client_id

        Args:
            username (str): _description_
            password (str): _description_
            name (str): _description_

        Raises:
            Exception: _description_

        Returns:
            str: client_id
        """
        data = {}
        data['username'] = username
        data['password_hash'] = password
        data['name'] = name

        try:
            response = requests.post(server_addr+"/user/register", json=data)
            if HttpError.isHttpError(response.status_code):
                raise Exception(str(response.status_code)+", "+str(response.text))
        except Exception as e:
            app.logger.error(e)
            raise e
        
        return response.json()['client_id']


    def getAllClients()-> dict:
        """return all clients details

        Raises:
            Exception: _description_

        Returns:
            dict: client_id, status, name
        """
        try:
            response = requests.get(server.address+"/client/all", auth=(user.username, user.password))
            if HttpError.isHttpError(response.status_code):
                raise Exception(str(response.status_code)+", "+str(response.text))
        except Exception as e:
            app.logger.error(e)
            raise e

        return response.json()
