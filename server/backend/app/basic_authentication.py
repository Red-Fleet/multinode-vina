from app.services.user_service import UserService
from flask_httpauth import HTTPBasicAuth
from flask import g

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    client = UserService.authenticateUser(client_id=username)
    if client != None:
        g.client = client
    return client