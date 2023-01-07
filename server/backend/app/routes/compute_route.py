from app import app, auth
from flask import request
from app.services.compute_service import ComputeService
from flask import Response, json, g
import uuid
import os

@app.route('/compute/create', methods = ['POST'])
@auth.login_required
def createComputeTask() -> Response:
    """Create new compute task, POST request should have  worker_id, ligands and target in json body

    Returns:
        Response: _description_
    """
    content = request.get_json()
    master_id = g.user.client_id
    
    if 'worker_id' not in content: return Response("worker_id not present", status=500, mimetype='application/json')
    worker_id = content['worker_id']

    if 'target' not in content: return Response("target not present", status=500, mimetype='application/json')
    target = content['target']
    
    if 'ligands' not in content: return Response("ligands file not present", status=500, mimetype='application/json')
    ligands = content['ligands']
    
    try:
        compute_id = ComputeService.createComputeTask(master_id=master_id, worker_id=worker_id, ligands=ligands, target=target)
        return Response(json.dumps({'compute_id':compute_id}),status=200, mimetype='application/json')
    except Exception as e:
        app.logger.error(e)
        return Response(str(e), status=500, mimetype='application/json')


@app.route('/compute/<compute_id>', methods = ['GET'])
@auth.login_required
def getComputeTaskUsingComputeId(compute_id) -> Response:
    try: 
        task = ComputeService.getComputeTaskUsingComputeId(compute_id=compute_id)
    except Exception as e:
        app.logger.error(e)
        return Response(str(e), status=500, mimetype='application/json')

    if task is None:
        return Response("Compute ID does not exists", status=500, mimetype='application/json')
    
    result = {}
    result['compute_id'] = task.compute_id
    result['master_id'] = task.master_id
    result['worker_id'] = task.worker_id
    result['target'] = task.target
    result['ligands'] = task.ligands
    result['result'] = task.result
    result['state'] = task.state.name
    result['error'] = task.error

    return Response(json.dumps(result), status=200, mimetype='application/json')

