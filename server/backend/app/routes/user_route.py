from app import app, auth
from flask import request
from app.services.user_service import UserService
from flask import Response, json, g

@app.route('/user/register', methods = ['POST'])
def register() -> Response:
    """Used to register new user

    Args(json):{
        "username": "username",
        "password_hash": "hash of password"
    }

    Returns:
        Success Response (HTTP status code 201) with JSON body:
        {
            "client_id": "id",
            "username": "username"
        }
        Failure Response (HTTP status code 500)
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
@auth.login_required
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
