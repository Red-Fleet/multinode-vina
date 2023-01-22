from app import app, user, server
from flask import Response, json
from flask import request
from app.http_services.server_http_service import ServerHttpService

@app.route('/user/isauth', methods=['GET'])
def isUserAuthenticated():
    """Return 1 if user is authenticated, else 0

    Returns:
        _type_: _description_
    """
    if user.isAuthenticated == True:
        return Response("1", status=200)

    
    return Response("0", status=200)

@app.route('/user/details', methods=['GET'])
def getUserDetails():
    """Return user details

    Returns:
        json: if user is authenticated (username, name, password, client_id) else response code 401
    """

    if user.isAuthenticated == False:
        return Response("Unauthorized Access", status=401)

    result = {}
    result['username'] = user.username
    result['name'] = user.name
    result['password'] = user.password
    result['client_id'] = user.client_id
    return Response(json.dumps(result), status=200)

@app.route('/user/login', methods=['POST'])
def login():
    """Api is used to login user into server, username and password should be in post request

    Args: json input
        address (str): server address
        username (str): username
        password (str): hash of password

    Returns:
        _type_: returns user details
    """
    content = request.get_json()
    
    if 'address' not in content: return Response("'address' not present in request", status=500)
    server.address = content['address']
    server.address_initialized = True

    if 'username' not in content: return Response("'username' not present", status=500)
    username = content['username']

    if 'password' not in content: return Response("'password' not present", status=500)
    password = content['password']
    try:
        result = ServerHttpService.loginToServer(server_addr=server.address, username=username, password=password)
    except Exception as e:
        if str(e) == "Unauthorized Access": return Response(str(e), status=401)
        return Response(str(e), status=500)
    
    # saving user details in backend on sucessful login
    user.username = result['username']
    user.isAuthenticated = True
    user.client_id = result['client_id']
    user.name = result['name']
    user.password = password

    return Response(json.dumps(result), status=200)

    

@app.route('/user/register', methods = ['POST'])
def register() -> Response:
    """Used to register new user to server

    Args: json input
        address (str): server address
        username (str): username
        password (str): hash of password
        name (str): name

    Returns:
        Response: return json contaning client_id and username
    """
    content = request.get_json()

    if 'address' not in content: return Response("'address' not present in request", status=500)
    server.address = content['address']
    server.address_initialized = True

    if 'username' not in content: Response("'username' is missing", status=500)
    username = content['username']
    
    if 'password' not in content: Response("'password' is missing", status=500)
    password = content['password']
    
    if 'name' not in content: Response("'name' is missing", status=500)
    name = content['name']

    try:
        client_id = ServerHttpService.registerToServer(server_addr=server.address, username=username, password=password, name=name)
        user.username = username
        user.client_id = client_id
        user.isAuthenticated = True
        user.password = password
        user.name = name
    except Exception as e:
        return Response(str(e), status= 500)
    
    return Response(json.dumps({"client_id":client_id, "username":username, "name":name}), status=201, mimetype='application/json')

@app.route('/client/all', methods = ['GET'])
def getAllClients():
    """return all clients details

    Returns:
        _type_: json contaning client_id, status, name
    """
    try:
        result = ServerHttpService.getAllClients()
    except Exception as e:
        return Response(str(e), status = 500)
    
    return Response(json.dumps(result), status=200, mimetype='application/json')