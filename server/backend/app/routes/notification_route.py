from app import app, auth
from flask import request
from app.services.notification_service import NotificationService
from flask import Response, json, g


@app.route('/notification/master', methods = ['GET'])
@auth.login_required
def getMasterNotifications():
    """Api will return all the notifications of master
    """

    master_id = g.user.client_id

    try:
        result = NotificationService.getMasterNotifications(master_id=master_id)
        result = [{'compute_id': noti.compute_id} for noti in result]
    except Exception as e:
        return Response(str(e), status=500, mimetype='application/json')
    
    return Response(json.dumps(result), status=200, mimetype='application/json')


@app.route('/notification/worker', methods = ['GET'])
@auth.login_required
def getWorkerNotifications():
    """Api will return all the notifications of worker
    """

    worker_id = g.user.client_id

    try:
        result = NotificationService.getWorkerNotifications(worker_id=worker_id)
        result = [{'compute_id': noti.compute_id} for noti in result]
    except Exception as e:
        return Response(str(e), status=500, mimetype='application/json')
    
    return Response(json.dumps(result), status=200, mimetype='application/json')