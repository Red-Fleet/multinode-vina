from app import app, server
from flask import Response, json
from flask import request

@app.route('/server/isinit', methods=['GET'])
def isServerInitialized():
    """Return 1 if server address is initialized, else 0

    Returns:
        _type_: _description_
    """
    if server.address_initialized == True:
        return Response("1", status=200)

    
    return Response("0", status=200)

@app.route('/server/address', methods=['GET'])
def getServerAddress():
    """Return server address

    Returns:
        _type_: _description_
    """
    return Response(server.address, status=200)

@app.route('/server/address', methods=['POST', 'PUT'])
def setServerAddress():
    """Set server address, address should be present in raw json

    Returns:
        _type_: returns status 500 on error
    """
    content = request.get_json()
    if 'address' not in content: return Response("'address' not present in request", status=500)
    
    server.address = content['address']
    server.address_initialized = True
    return Response(status=200)