from app.services.login_service import LoginService
from flask_httpauth import HTTPBasicAuth
from flask import g

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    user = LoginService.loginUser(username=username, password_hash=password)
    if user != None:
        g.user = user
    return user