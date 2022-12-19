from app import app
from flask import request
from app.services.login_service import LoginService
from flask import Response, json

#@app.route('/login', methods = ['GET'])
def login() -> Response:
    """Used to login new user

    Args: json input
        username (str): username
        password_hash (str): hash of password

    Returns:
        Response: return client_id and username on sucessful authentication, else authentication error
    """
    content = request.get_json()
    username = content['username']
    password_hash = content['password_hash']
    try:
        client_id = LoginService.loginUser(username, password_hash)
        if client_id == None:
            return Response(status=401)
        else :
            return Response(json.dumps({"client_id":client_id, "username":username}), status=200, mimetype='application/json')
    except Exception as e:
        return Response(str(e), status=500, mimetype='application/json')