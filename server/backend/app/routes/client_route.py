from app import app, auth
from flask import request
from app.services.client_service import ClientService
from flask import Response, json, g

@app.route('/client/state/<state>', methods = ['PUT'])
@auth.login_required
def updateState(state) -> Response:
    """Update State of client

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


@app.route('/client/request/reject/<master_id>', methods=['PUT'])
@auth.login_required
def rejectComputeRequest(master_id):
    """Client can use api to reject compute request

    Args:
        master_id (_type_): client_id of master

    Raises:
        Exception: raise exception on error
    """
    try:
        ClientService.rejectComputeRequest(master_id=master_id, worker_id=g.user.client_id)
        return Response(status=200, mimetype='application/json')
    except Exception as e:
        app.logger.error(e)
        return Response(str(e), status=500, mimetype='application/json')
