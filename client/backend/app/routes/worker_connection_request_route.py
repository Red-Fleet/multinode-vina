from app import app, server
from flask import Response, json
from flask import request
from app.services.worker_connection_request_service import WorkerConnectionRequestService

@app.route('/worker/connectionrequest', methods=['GET'])
def getWorkerConnectionRequests():
    """return all the requests of worker

    Returns:
        jsin: list of master_ids and state of connection request
    """
    try:
        result = WorkerConnectionRequestService.getWorkerConenctionRequests()
    except Exception as e:
        return Response(str(e), status=500)
    
    return Response(json.dumps(result), status=200)


@app.route('/worker/connectionrequest/accept', methods=['PUT'])
def acceptConnectionRequest():
    """used by worker to accept connection request of master 

    """
    content = request.get_json()
    if "master_id" not in content : return Response("'master_id' not found", status=500)
    master_id = content['master_id']
    try:
        WorkerConnectionRequestService.acceptConnectionRequest(master_id = master_id)
    except Exception as e:
        return Response(str(e), status=500)
    
    return Response(status=200)


@app.route('/worker/connectionrequest/reject', methods=['PUT'])
def rejectConnectionRequest():
    """used by worker to accept connection request of master 

    """
    content = request.get_json()
    if "master_id" not in content : return Response("'master_id' not found", status=500)
    master_id = content['master_id']
    try:
        WorkerConnectionRequestService.rejectConnectionRequest(master_id = master_id)
    except Exception as e:
        return Response(str(e), status=500)
    
    return Response(status=200)
