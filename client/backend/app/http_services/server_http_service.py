from app import server, app
import requests

class ServerHttpService:
    @staticmethod
    def isHttpError(status_code: int)->bool:
        if status_code<200 or status_code>299:
            return True
        return False

    @staticmethod
    def loginToServer(username:str, password: str):
        """Methods connects client to server and gets user details 

        Args:
            username (str): username of client
            password (str): password of client

        Returns:
            dict: username, name, client_id
        """
        try:
            response = requests.get(server.address+"/user/login", auth=(username, password))
            if ServerHttpService.isHttpError(response.status_code):
                raise Exception(str(response.status_code)+", "+str(response.text))
        except Exception as e:
            app.logger.error(e)
            raise e

        return response.json()

    @staticmethod
    def registerToServer(username:str, password:str, name: str)-> str:
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
            response = requests.post(server.address+"/user/register", json=data)
            if ServerHttpService.isHttpError(response.status_code):
                raise Exception(str(response.status_code)+", "+str(response.text))
        except Exception as e:
            app.logger.error("")

        
        return response.json()['client_id']

    #def createRequest():

