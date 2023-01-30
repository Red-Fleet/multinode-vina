from app import app, auth
from flask import request
from app.services.request_service import RequestService
from flask import Response, json, g



@app.route('/request/create', methods = ['POST'])
@auth.login_required
def createRequest():
        """Create new Request

        Args(json):
            worker_id (str): client_id of worker to which request will be shared

        Raises:
            Exception: Database Error
        """
        content = request.get_json()

        if 'worker_id' not in content: return Response('worker_id not present', status=500)
        worker_id = content['worker_id']
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

@app.route('request/delete', method=['PUT'])
def deleteRequest():
    content = request.get_json()
    if 'worker_id' not in content: return Response('worker_id not present', status=500)
    worker_id = content['worker_id']
    try:
        RequestService.deleteMasterRequest(master_id=g.user.client_id, worker_id=worker_id)
    except Exception as e:
        return Response(str(e), status=500)

@app.route('/request/reject', methods=['PUT'])
@auth.login_required
def rejectComputeRequest():
    """Client can use api to reject compute request

    Args(json):
        master_id (str): client_id of master

    Raises:
        Exception: raise exception on error
    """
    content = request.get_json()

    if 'master_id' not in content: return Response('master_id not present', status=500)
    master_id = content['master_id']

    try:
        RequestService.rejectComputeRequest(master_id=master_id, worker_id=g.user.client_id)
        return Response(status=200, mimetype='application/json')
    except Exception as e:
        app.logger.error(e)
        return Response(str(e), status=500, mimetype='application/json')


@app.route('/request/accept', methods=['PUT'])
@auth.login_required
def acceptComputeRequest():
    """Client can use api to accept compute request

    Args(json):
        master_id (str): client_id of master

    Raises:
        Exception: raise exception on error
    """
    content = request.get_json()

    if 'master_id' not in content: return Response('master_id not present', status=500)
    master_id = content['master_id']

    try:
        RequestService.acceptComputeRequest(master_id=master_id, worker_id=g.user.client_id)
        return Response(status=200, mimetype='application/json')
    except Exception as e:
        app.logger.error(e)
        return Response(str(e), status=500, mimetype='application/json')