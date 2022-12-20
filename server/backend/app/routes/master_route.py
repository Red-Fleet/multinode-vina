from app import app, auth
from flask import request
from app.services.master_service import MasterService
from flask import Response, json

@app.route('/master/clients', methods = ['GET'])
@auth.login_required
def getAllClients() -> Response:
    """Get all registered clients

    Returns:
        Response: return list of client_id, name and state
    """
    try:
        result = MasterService.getAllClients()
        return Response(json.dumps(result), status=200, mimetype='application/json')
    except Exception as e:
        app.logger.error(e)
        return Response(str(e), status=500, mimetype='application/json')