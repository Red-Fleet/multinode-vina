from app import app, connection
from flask import Response, json
from flask import request
from app.http_services.server_http_service import ServerHttpService
from app.models.connect import Connect

@app.route('/user/details', methods=['GET'])
def isConnected():
    """Return client_id if logined, else 404

    Returns:
        _type_: _description_
    """
    
    if connection.connected is True:
        return Response(json.dumps({'client_id': connection.username}), status=200)

    
    return Response("Unauthorized", status=404)


@app.route('/user/connect', methods=['POST'])
def connect():
    """Api is used to connecct user into server, server address and client_id should be in post request

    Args: json input
        address (str): server address
        client_id (str): client_id

    Returns:
        _type_: returns user details
    """
    content = request.get_json()
    
    if 'address' not in content: return Response("'address' not present in request", status=500)
    address = content['address']

    if 'client_id' not in content: return Response("'client_id' not present", status=500)
    clientId = content['client_id']

    try:
        clientId = ServerHttpService.connectWithServer(server_addr=address, clientId=clientId)
    except Exception as e:
        if str(e) == "Unauthorized Access": return Response(str(e), status=401)
        return Response(str(e), status=500)
    
    # saving user details in backend on sucessful login
    connection.address = address
    connection.username = clientId
    connection.connected = True

    return Response(json.dumps({"client_id": clientId}), status=200)
