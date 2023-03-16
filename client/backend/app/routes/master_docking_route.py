from app import app, server
from flask import Response, json
from flask import request
from app.services.master_docking_service import MasterDockingService

@app.route('/master/docking/create', methods=['POST'])
def createDocking():
    """create new dock task

    Returns:
        json: json contaning docking_id
    """
    content = request.get_json()
    
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
        docking_id = MasterDockingService.createDock(worker_ids=worker_ids, ligands=ligands, target=target, target_name=target_name ,ligands_name=ligands_name)
        return Response(json.dumps({'docking_id':docking_id}),status=201, mimetype='application/json')
    except Exception as e:
        app.logger.error(e)
        return Response(str(e), status=500, mimetype='application/json')
