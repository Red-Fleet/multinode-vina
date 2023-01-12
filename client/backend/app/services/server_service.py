from app import server
import requests

class ServerService:

    @staticmethod
    def loginToServer(username:str, password: str):
        """Methods connects client to server and gets user details 

        Args:
            username (str): username of client
            password (str): password of client

        Returns:
            dict: username, name, client_id
        """
        response = requests.get(server.address+"/user/login", auth=(username, password))
        
        if response.status_code <200 or response.status_code>299:
            raise Exception(response.text)

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
        response = requests.post(server.address+"/user/register", json=data)
        
        if response.status_code==500:
            raise Exception(str(response.text))
        
        return response.json()['client_id']

