from app import app, auth
from flask import request
from app.services.request_service import RequestService
from flask import Response, json, g



@app.route('/request/create/<worker_id>', methods = ['POST'])
@auth.login_required
def createRequest(worker_id: str):
        """Create new Request

        Args:
            master_id (str): client_id of worker to which request will be shared

        Raises:
            Exception: Database Error
        """

        try:
            RequestService.newRequest(master_id=g.user.client_id, worker_id=worker_id)
            return Response(status=200, mimetype='application/json')
        except Exception as e:
            app.logger.error(e)
            return Response(str(e), status=500, mimetype='application/json')

@app.route('/request/reject/<master_id>', methods=['PUT'])
@auth.login_required
def rejectComputeRequest(master_id):
    """Client can use api to reject compute request

    Args:
        master_id (_type_): client_id of master

    Raises:
        Exception: raise exception on error
    """
    try:
        RequestService.rejectComputeRequest(master_id=master_id, worker_id=g.user.client_id)
        return Response(status=200, mimetype='application/json')
    except Exception as e:
        app.logger.error(e)
        return Response(str(e), status=500, mimetype='application/json')
