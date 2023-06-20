from app import app, server
from flask import Response, json
from flask import request
from app.services.master_docking_service import MasterDockingService

@app.route('/master/docking/create', methods=['POST'])
def createDocking():
    """create new dock task
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
        json: json contaning docking_id
    """
    content = request.get_json()
    
    if 'worker_ids' not in content: return Response("worker_ids not present", status=500, mimetype='application/json')

    if 'target' not in content: return Response("target not present", status=500, mimetype='application/json')
    
    if 'ligands' not in content: return Response("ligands file not present", status=500, mimetype='application/json')
    

    try:
        docking_id = MasterDockingService.createDock(content)
        return Response(json.dumps({'docking_id':docking_id}),status=201, mimetype='application/json')
    except Exception as e:
        app.logger.error(e)
        return Response(str(e), status=500, mimetype='application/json')


@app.route('/master/docking/ids', methods = ['GET'])
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

    try:
        result = MasterDockingService.getMasterDockingIds()
        return Response(json.dumps(result), status=200, mimetype='application/json')
    except Exception as e:
        return Response(str(e), status=500, mimetype='application/json')
    

@app.route('/master/docking/compute/ids', methods = ['GET'])
def getAllComputeIds()->Response:
    """function returns all docking_id and state of dockings started by master

    Returns:
        Response: json: 
            [
                "compute_id_1", "compute_id_2", ...
            ]
    """
    content = request.get_json()
    if 'compute_id' not in content: return Response("compute_id not present", status=500, mimetype='application/json')

    try:
        result = MasterDockingService.getAllComputeIds(docking_id= content["docking_id"])
        return Response(json.dumps(result), status=200, mimetype='application/json')
    except Exception as e:
        return Response(str(e), status=500, mimetype='application/json')
    


@app.route('/master/docking/compute/result', methods = ['GET'])
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
        result = MasterDockingService.getComputeResult(compute_id = content["compute_id"])
        return Response(json.dumps(result), status=200, mimetype='application/json')
    except Exception as e:
        return Response(str(e), status=500, mimetype='application/json')
    

@app.route('/master/docking/result/download', methods = ['POST'])
def downloadDockingResult()->Response:
    """returns result pdbqt and ligand_name of given compute_id

        Args(json):
            {
                "docking_id":"id"
                "path": "path of folder to store docking result"
            }

        Raises:
            Exception: _description_
    """

    content = request.get_json()
    if 'docking_id' not in content: return Response("docking_id not present", status=500, mimetype='application/json')
    if 'path' not in content: return Response("path not present", status=500, mimetype='application/json')
    try:
        MasterDockingService.downloadDockingResult(docking_id = content["docking_id"], path=content['path'])
        return Response(status=200, mimetype='application/json')
    except Exception as e:
        return Response(str(e), status=500, mimetype='application/json')