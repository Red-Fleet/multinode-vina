from app import app, server
from flask import Response, json
from flask import request
from app.services.worker_connection_request_service import WorkerConnectionRequestService

@app.route('/worker/connectionrequest', methods=['GET'])
def getConnectionRequests():
    """return all the requests of worker

    Returns:
        jsin: list of master_ids and state of connection request
    """
    try:
        result = WorkerConnectionRequestService.getWorkerConenctionRequests()
    except Exception as e:
        return Response(str(e), status=500)
    
    return Response(json.dumps(result), status=200)