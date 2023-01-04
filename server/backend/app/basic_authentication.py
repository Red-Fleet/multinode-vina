from app.services.user_service import UserService
from flask_httpauth import HTTPBasicAuth
from flask import g

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    user = UserService.authenticateUser(username=username, password_hash=password)
    if user != None:
        g.user = user
    return user