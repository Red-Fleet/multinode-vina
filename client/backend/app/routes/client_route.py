from app import app, user, server
from flask import Response, json
from flask import request
from app.services.client_service import ClientService

@app.route('/client/all', methods = ['GET'])
def getAllClients():
    """return all clients details

    Returns:
        json: [{client_id_1, status, name}, {client_id_2, status, name}, ....]
    """
    try:
        result = ClientService.getAllClients()
    except Exception as e:
        return Response(str(e), status = 500)
    
    return Response(json.dumps(result), status=200, mimetype='application/json')

@app.route('/client/details', methods=['GET'])
def getClientDetails():
    """return details of a client
    Args(json):
        client_id: client_id of client 
    Returns:
        json: client_id, state, name
    """
    content = request.args
    if 'client_id' not in content: return Response("'client_id' not found")
    client_id = content['client_id']

    try:
        result = ClientService.getClientDetails(client_id=client_id)
    except Exception as e:
        return Response(str(e), status=500)
    
    return Response(json.dumps(result), status=200)