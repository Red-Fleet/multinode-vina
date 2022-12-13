from app import app
from flask import request
from app.services.register_service import RegisterService
from flask import Response, json

@app.route('/register', methods = ['POST'])
def register() -> Response:
    username = request.form['username']
    password_hash = request.form['password_hash']
    try:
        client_id = RegisterService.registerUser(username, password_hash)
        return Response(json.dumps({"client_id":client_id, "username":username}), status=201, mimetype='application/json')
    except Exception as e:
        return Response(str(e), status=500, mimetype='application/json')