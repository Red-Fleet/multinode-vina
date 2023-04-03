from app import app, auth
from flask import request
from app.services.docking_service import DockingService
from flask import Response, json, g
import uuid
import os

@app.route('/docking/create', methods = ['POST'])
@auth.login_required
def createDocking() -> Response:
    """Create new docking task, POST request should have  worker_ids, ligands and target in json body

    Returns:
        Response: docking_id
    """
    content = request.get_json()
    master_id = g.user.client_id
    
    if 'worker_ids' not in content: return Response("worker_ids not present", status=500, mimetype='application/json')
    worker_ids = content['worker_ids']

    if 'target' not in content: return Response("target not present", status=500, mimetype='application/json')
    target = content['target']
    
    if 'ligands' not in content: return Response("ligands file not present", status=500, mimetype='application/json')
    ligands = content['ligands']
    
    if 'target_name' not in content: target_name = ""
    else : target_name = content['target_name']

    if 'ligands_name' not in content: ligands_name = ""
    else : ligands_name = content['ligands_name']

    try:
        docking_id = DockingService.createDock(master_id=master_id, worker_ids=worker_ids, ligands=ligands, target=target, target_name=target_name ,ligands_name=ligands_name)
        return Response(json.dumps({'docking_id':docking_id}),status=200, mimetype='application/json')
    except Exception as e:
        app.logger.error(e)
        return Response(str(e), status=500, mimetype='application/json')
    


@app.route('/docking/computes', methods = ['GET'])
@auth.login_required
def getComputes() -> Response:
    
    content = request.get_json()
    master_id = g.user.client_id
    
    if 'docking_id' not in content: return Response("docking_id not present", status=500, mimetype='application/json')
    docking_id = content['docking_id']

    if 'count' not in content: return Response("count not present", status=500, mimetype='application/json')
    count = content['count']

    try:
        result = DockingService.getComputes(docking_id=docking_id, num=count)
        return Response(json.dumps(result),status=200, mimetype='application/json')
    except Exception as e:
        app.logger.error(e)
        return Response(str(e), status=500, mimetype='application/json')
    

@app.route('/docking/target', methods = ['GET'])
@auth.login_required
def getDockingTarget() -> Response:
    content = request.get_json()

    if 'docking_id' not in content: return Response("docking_id not present", status=500, mimetype='application/json')
    docking_id = content['docking_id']

    try:
        target = DockingService.getDockingTarget(docking_id=docking_id)
        result = {"target": target}
        return Response(json.dumps(result), status=200, mimetype='application/json')
    except Exception as e:
        return Response(str(e), status=500, mimetype='application/json')
