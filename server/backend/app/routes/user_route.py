from app import app, auth
from flask import request
from app.services.user_service import UserService
from flask import Response, json, g

@app.route('/user/connect', methods = ['POST'])
def connect() -> Response:
    """Used to register/login a user

    Args(json):{
        "client_id": "client_id/username"
    }

    Returns:
        Success Response (HTTP status code 201) with JSON body:
        {
            "client_id": "id"
        }
        Failure Response (HTTP status code 500)
    """
    content = request.get_json()
    client_id = content['client_id']
    try:
        client_id = UserService.connect(client_id)
        return Response(json.dumps({"client_id":client_id}), status=201, mimetype='application/json')
    except Exception as e:
        return Response(str(e), status=500, mimetype='application/json')


