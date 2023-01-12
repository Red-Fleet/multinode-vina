from app import app
from flask import Response

@app.route('/ping', methods = ['GET'])
def ping():
    return Response(status=200)