from app import app, auth
from flask import request
from app.services.master_service import MasterService
from flask import Response, json, g

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


@app.route('/master/request/<request_to_client_id>', methods = ['POST'])
@auth.login_required
def createRequest(request_to_client_id: str):
        """Create new Request

        Args:
            request_to_client_id (str): client_if of client to which request will be shared

        Raises:
            Exception: Database Error
        """

        try:
            MasterService.createRequest(request_from=g.user.client_id, request_to=request_to_client_id)
            return Response(status=200, mimetype='application/json')
        except Exception as e:
            app.logger.error(e)
            return Response(str(e), status=500, mimetype='application/json')