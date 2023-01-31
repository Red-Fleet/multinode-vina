from app import app, server
from flask import Response, json
from flask import request
from app.services.master_connection_request_service import MasterConnectionRequestService

@app.route('/master/connectionrequest', methods=['GET'])
def getConnectionRequests():
    """return all the requests created by master

    Returns:
        _type_: _description_
    """
    try:
        result = MasterConnectionRequestService.getAllConnectionRequest()
    except Exception as e:
        return Response(str(e), status=500)
    
    return Response(json.dumps(result), status=200)

@app.route('/master/connectionrequest/create', methods=['POST'])
def createConnectionRequest():
    """create new connection request

    Returns:
        _type_: _description_
    """
    content = request.get_json()
    
    if 'worker_id' not in content : return Response("'worker_id' is missing", status=500)
    try:
        MasterConnectionRequestService.createConnectionRequest(worker_id=content['worker_id'])
    except Exception as e:
        return Response(str(e), status=500)
    
    return Response(status=201)

@app.route('master/connectionrequest', method=['DELETE'])
def deleteConnectionRequest():
    """Delete Connection request

    Returns:
        _type_: _description_
    """
    content = request.get_json()
    if 'worker_id' not in content : return Response("'worker_id' is missing", status=500)
    worker_id = content['worker_id']
    try:
        MasterConnectionRequestService.deleteConnectionRequest(worker_id=worker_id)
    except Exception as e:
        return Response(str(e), status= 500)

    return Response(status=200)