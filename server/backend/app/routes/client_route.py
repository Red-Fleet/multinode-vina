from app import app, auth
from flask import request
from app.services.client_service import ClientService
from flask import Response, json, g

@app.route('/client/all', methods = ['GET'])
@auth.login_required
def getAllClients() -> Response:
    """Get all registered clients

    Returns:
        Response: return list of client_id, name and state
    """
    try:
        result = ClientService.getAllClients()
        return Response(json.dumps(result), status=200, mimetype='application/json')
    except Exception as e:
        app.logger.error(e)
        return Response(str(e), status=500, mimetype='application/json')



@app.route('/client/state/<state>', methods = ['PUT'])
@auth.login_required
def updateState(state) -> Response:
    """Client can update its state

        Args:
            client_id (_type_): client_id (primary key of client table)
            state (_type_): new state of client

        Raises:
            Exception: raise exception on error
    """
    try:
        ClientService.updateState(client_id=g.user.client_id, state=state)
        return Response(status=200, mimetype='application/json')
    except Exception as e:
        app.logger.error(e)
        return Response(str(e), status=500, mimetype='application/json')

@app.route('/client/details', methods = ['GET'])
@auth.login_required
def getClientDetails():
    """return client details
    Args(json):
        client_id: client_id of client

    Returns:
        json: details of client - client_id, name, state
    """
    content = request.get_json()
    if 'client_id' not in content: return Response("'client_id' not found", status=500)
    client_id = content['client_id']
    try:
        result = ClientService.getClientDetails(client_id=client_id)
    except Exception as e:
        return Response(str(e), status=500)
    
    return Response(json.dumps(result), status=200)
