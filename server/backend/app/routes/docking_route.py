from app import app, auth
from flask import request
from app.services.docking_service import DockingService
from flask import Response, json, g
import uuid
import os

@app.route('/docking/create', methods = ['POST'])
@auth.login_required
def createDocking() -> Response:
    """Create new docking task, POST request should have  worker_ids, ligands, target, params in json body
    Args(json):
        {
            "worker_ids": [id_1, id_2, ...],
            "target": target pdbqt,
            "ligands": [pdbqt_1, pdbqt_2, ...],
            "target_name": name,
            "ligands_name": [ligand_name_1, ligand_name_2, ...],
            vina parameters ...
        }
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

    if 'ligands_name' not in content: ligands_name = []
    else : ligands_name = content['ligands_name']

    params = dict()

    if 'scoring_function' in content: params['scoring_function'] = content['scoring_function']
    if 'cpu_num' in content: params['cpu_num'] = content['cpu_num']
    if 'random_seed' in content: params['random_seed'] = content['random_seed']
    if 'exhaustiveness' in content: params['exhaustiveness'] = content['exhaustiveness']
    if 'n_poses' in content: params['n_poses'] = content['n_poses']
    if 'min_rmsd' in content: params['min_rmsd'] = content['min_rmsd']
    if 'max_evals' in content: params['max_evals'] = content['max_evals']
    if 'center_x' in content: params['center_x'] = content['center_x']
    if 'center_y' in content: params['center_y'] = content['center_y']
    if 'center_z' in content: params['center_z'] = content['center_z']
    if 'box_size_x' in content: params['box_size_x'] = content['box_size_x']
    if 'box_size_y' in content: params['box_size_y'] = content['box_size_y']
    if 'box_size_z' in content: params['box_size_z'] = content['box_size_z']
    if 'grid_spacing' in content: params['grid_spacing'] = content['grid_spacing']


    try:
        docking_id = DockingService.createDock(master_id=master_id, worker_ids=worker_ids, ligands=ligands, target=target, target_name=target_name ,ligands_name=ligands_name, params=params)
        return Response(json.dumps({'docking_id':docking_id}),status=200, mimetype='application/json')
    except Exception as e:
        app.logger.error(e)
        return Response(str(e), status=500, mimetype='application/json')
    


@app.route('/docking/computes', methods = ['GET'])
@auth.login_required
def getComputes() -> Response:
    
    content = request.get_json()
    
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


@app.route('/docking/details', methods = ['GET'])
@auth.login_required
def getDockingDetails() -> Response:
    """returns target pdbqt, master_id, params(parameters of vina) using docking_id

        Args:
            docking_id (str): _description_

        Raises:
            Exception: _description_

        Returns:
            json: containing target, master_id, params
    """
    content = request.get_json()

    if 'docking_id' not in content: return Response("docking_id not present", status=500, mimetype='application/json')
    docking_id = content['docking_id']

    try:
        result = DockingService.getDockingDetails(docking_id=docking_id)
        return Response(json.dumps(result), status=200, mimetype='application/json')
    except Exception as e:
        return Response(str(e), status=500, mimetype='application/json')
    
@app.route('/docking/computes/result', methods = ['POST'])
@auth.login_required
def saveComputeResult()->Response:
    content = request.get_json()

    if 'computes' not in content: return Response("computes not present", status=500, mimetype='application/json')
    if 'docking_id' not in content: return Response("docking_id not present", status=500, mimetype='application/json')
    try:
        result = DockingService.saveComputeResult(docking_id=content["docking_id"], computes=content['computes'])
        return Response(status=200, mimetype='application/json')
    except Exception as e:
        return Response(str(e), status=500, mimetype='application/json')
    
@app.route('/docking/computes/error', methods = ['POST'])
@auth.login_required
def saveComputeError()->Response:
    content = request.get_json()

    if 'computes' not in content: return Response("computes not present", status=500, mimetype='application/json')
    if 'docking_id' not in content: return Response("docking_id not present", status=500, mimetype='application/json')
    try:
        result = DockingService.saveComputeError(docking_id=content["docking_id"], computes=content['computes'])
        return Response(status=200, mimetype='application/json')
    except Exception as e:
        return Response(str(e), status=500, mimetype='application/json')

@app.route('/docking/error', methods = ['POST'])
@auth.login_required
def saveDockingError()->Response:
    content = request.get_json()
    worker_id = g.user.client_id
    if 'docking_id' not in content: return Response("docking_id not present", status=500, mimetype='application/json')
    if 'error' not in content: return Response("error not present", status=500, mimetype='application/json')
    try:
        DockingService.saveDockingError(docking_id=content["docking_id"], worker_id=worker_id, error=content["error"])
        return Response(status=200, mimetype='application/json')
    except Exception as e:
        return Response(str(e), status=500, mimetype='application/json')
       
@app.route('/docking/status', methods = ['GET'])
@auth.login_required
def getDockingStatus()->Response:
    content = request.get_json()

    if 'docking_id' not in content: return Response("docking_id not present", status=500, mimetype='application/json')
    try:
        result = DockingService.getDockingStatus(docking_id=content["docking_id"])
        return Response(json.dumps(result), status=200, mimetype='application/json')
    except Exception as e:
        return Response(str(e), status=500, mimetype='application/json')

@app.route('/docking/delete', methods = ['DELETE'])
@auth.login_required
def deleteDocking()->Response:
    content = request.get_json()
    if 'docking_id' not in content: return Response("docking_id not present", status=500, mimetype='application/json')
    try:
        result = DockingService.deleteDocking(docking_id=content["docking_id"])
        return Response(json.dumps(result), status=200, mimetype='application/json')
    except Exception as e:
        return Response(str(e), status=500, mimetype='application/json')
         
@app.route('/docking/finished', methods = ['GET'])
@auth.login_required
def isDockingFinished()->Response:
    """will return 'true'/'false' of str type

    Returns:
        Response: _description_
    """
    content = request.get_json()

    if 'docking_id' not in content: return Response("docking_id not present", status=500, mimetype='application/json')
    try:
        result = DockingService.isDockingFinished(docking_id=content["docking_id"])
        return Response(json.dumps(result), status=200, mimetype='application/json')
    except Exception as e:
        return Response(str(e), status=500, mimetype='application/json')
    
# @app.route('/docking/compute/result', methods = ['GET'])
# @auth.login_required
# def getComputeResult()->Response:
#     content = request.get_json()

#     if 'docking_id' not in content: return Response("docking_id not present", status=500, mimetype='application/json')
#     if 'compute_id' not in content: return Response("compute_id not present", status=500, mimetype='application/json')
#     try:
#         result = DockingService.getComputeResult(docking_id=content["docking_id"], compute_id=content["compute_id"])
#         return Response(json.dumps(result), status=200, mimetype='application/json')
#     except Exception as e:
#         return Response(str(e), status=500, mimetype='application/json')
    

@app.route('/docking/ids', methods = ['GET'])
@auth.login_required
def getMasterDockingIds()->Response:
    """function returns all docking_id and state of dockings started by master

    Returns:
        Response: json: 
            [
                {
                    "docking_id":"val",
                    "state": "val"
                }
                ...
            ]
    """
    master_id = g.user.client_id

    try:
        result = DockingService.getMasterDockingIds(master_id= master_id)
        return Response(json.dumps(result), status=200, mimetype='application/json')
    except Exception as e:
        print(e)
        return Response(str(e), status=500, mimetype='application/json')
    

@app.route('/docking/compute/ids', methods = ['GET'])
@auth.login_required
def getAllComputeIds()->Response:
    """function returns all docking_id and state of dockings started by master

    Returns:
        Response: json: 
            [
                "compute_id_1", "compute_id_2", ...
            ]
    """
    content = request.get_json()
    if 'docking_id' not in content: return Response("docking not present", status=500, mimetype='application/json')

    try:
        result = DockingService.getAllComputeIds(docking_id= content["docking_id"])
        return Response(json.dumps(result), status=200, mimetype='application/json')
    except Exception as e:
        return Response(str(e), status=500, mimetype='application/json')
    

@app.route('/docking/compute/result', methods = ['GET'])
@auth.login_required
def getComputeResult()->Response:
    """returns result pdbqt and ligand_name of given compute_id

        Args(json):
            {
                "compute_id":"id"
            }

        Raises:
            Exception: _description_

        Returns(json):
            {
                "result": "pdbqt",
                "ligand_name": "name"
            }
    """

    content = request.get_json()
    if 'compute_id' not in content: return Response("compute_id not present", status=500, mimetype='application/json')
    
    try:
        result = DockingService.getComputeResult(compute_id = content["compute_id"])
        return Response(json.dumps(result), status=200, mimetype='application/json')
    except Exception as e:
        return Response(str(e), status=500, mimetype='application/json')