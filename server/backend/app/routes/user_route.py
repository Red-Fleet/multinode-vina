from app import app, auth
from flask import request
from app.services.user_service import UserService
from flask import Response, json, g

@app.route('/user/register', methods = ['POST'])
def register() -> Response:
    """Used to register new user

    Args: json input
        username (str): username
        password_hash (str): hash of password

    Returns:
        Response: return json contaning client_id and username
    """
    content = request.get_json()
    username = content['username']
    password_hash = content['password_hash']
    name = content['name']
    try:
        client_id = UserService.createUser(username, password_hash, name)
        return Response(json.dumps({"client_id":client_id, "username":username}), status=201, mimetype='application/json')
    except Exception as e:
        return Response(str(e), status=500, mimetype='application/json')


@app.route('/user/login', methods=['GET'])
def userLogin() -> Response:
    """Api will return user details

    Returns:
        Response: _description_
    """
    result = {}
    result['username'] = g.user.username
    result['name'] = g.user.name
    result['client_id'] = g.user.client_id

    return Response(json.dumps(result), status=200)
