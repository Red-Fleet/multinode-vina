from app import app, user, server
from flask import Response, json
from flask import request
from app.services.chembl_service import ChemblService

@app.route('/chembl/save/sdf', methods = ['GET'])
def saveSdfUsingChemblId():
    content = request.get_json()
    if 'chembl-id' not in content: return Response("'chembl-id' not found")
    chembl_id = content['chembl-id']

    if 'dir-path' not in content: return Response("'dir-path' not found")
    dir_path = content["dir-path"]

    try:
        ChemblService.saveSdfUsingChemblId(chembl_id=chembl_id, dir_path=dir_path)
        return Response(status=200, mimetype='application/json')
    except Exception as e:
        return Response(str(e), status=500, mimetype='application/json')


@app.route('/chembl/save/pdbqt', methods = ['GET'])
def savePdbqtUsingChemblId():
    content = request.get_json()
    if 'chembl-id' not in content: return Response("'chembl-id' not found")
    chembl_id = content['chembl-id']

    if 'dir-path' not in content: return Response("'dir-path' not found")
    dir_path = content["dir-path"]

    try:
        ChemblService.savePdbqtUsingChemblId(chembl_id=chembl_id, dir_path=dir_path)
        return Response(status=200, mimetype='application/json')
    except Exception as e:
        return Response(str(e), status=500, mimetype='application/json')