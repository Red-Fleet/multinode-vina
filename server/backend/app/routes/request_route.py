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


@app.route('/request/master', methods = ['GET'])
@auth.login_required
def getMasterRequests():
        """Returns all request created by master

        Raises:
            Exception: Database Error
        """

        try:
            result = RequestService.getMasterRequests(master_id=g.user.client_id)
            return Response(json.dumps(result), status=200, mimetype='application/json')
        except Exception as e:
            app.logger.error(e)
            return Response(str(e), status=500, mimetype='application/json')


@app.route('/request/worker', methods = ['GET'])
@auth.login_required
def getWorkerRequests():
        """Returns all request received by a worker

        Raises:
            Exception: Database Error
        """

        try:
            result = RequestService.getWorkerRequests(worker_id=g.user.client_id)
            return Response(json.dumps(result), status=200, mimetype='application/json')
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


@app.route('/request/accept/<master_id>', methods=['PUT'])
@auth.login_required
def acceptComputeRequest(master_id):
    """Client can use api to accept compute request

    Args:
        master_id (_type_): client_id of master

    Raises:
        Exception: raise exception on error
    """
    try:
        RequestService.acceptComputeRequest(master_id=master_id, worker_id=g.user.client_id)
        return Response(status=200, mimetype='application/json')
    except Exception as e:
        app.logger.error(e)
        return Response(str(e), status=500, mimetype='application/json')