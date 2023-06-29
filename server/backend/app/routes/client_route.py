from app import app, auth
from flask import request
from app.services.client_service import ClientService
from flask import Response, json, g

@app.route('/client/all', methods = ['GET'])
@auth.login_required
def getAllClients() -> Response:
    """Api returns all registered clients details (client_id, state, name)

    Returns:
        json: [{"client_id": "id", "state":"OFFLINE/ONLINE", "name":"client-name"}, ...]
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
    """Api used by client to update its state

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
    """Api returns client details (client_id, name, state)
    Args:
        json: {"client_id": "id"}

    Returns:
        json: {"client_id": "id", "state":"OFFLINE/ONLINE", "name":"client-name"}
    """
    content = request.get_json()
    if 'client_id' not in content: return Response("'client_id' not found", status=500)
    client_id = content['client_id']
    try:
        result = ClientService.getClientDetails(client_id=client_id)
    except Exception as e:
        return Response(str(e), status=500)
    
    return Response(json.dumps(result), status=200)
