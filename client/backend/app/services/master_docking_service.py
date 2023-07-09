import datetime
from app import db, app, user
from app.http_services.server_http_docking_service import ServerHttpDockingService
from app.utils.pqbqt_utils import PdbqtUtils
import os
from app.utils.file_utils import generateFilePath

class MasterDockingService:
    """MasterDockingService class is used by master to create, view, update, delete dockings
    """
    @staticmethod
    def createDock(docking_details: dict):
        """This method will start a new docking request on server

        Args:
            docking_details (dict): {
            "worker_ids": [id_1, id_2, ...],
            "target": target pdbqt,
            "ligands": [pdbqt_1, pdbqt_2, ...],
            "target_name": name,
            "ligands_name": [ligand_name_1, ligand_name_2, ...],
            vina parameters ...
        }

        Returns:
            dict: {"docking_id": id}
        """
        try:
            # splitting pdbqt
            splitted_ligands = []
            ligands_name = []
            for i in range(len(docking_details['ligands'])):
                ligands = docking_details['ligands'][i]
                try:
                    name, extension = os.path.splitext(docking_details['ligands_name'][i])
                except:
                    name = ""
                    extension = ""
                
                splits = PdbqtUtils.splitIntoLigands(ligands)
                for i in range(1, len(splits)+1):
                    if i == 1:
                        ligands_name.append(name+str(extension))
                    else:
                        ligands_name.append(name+"_"+str(i)+str(extension))
                splitted_ligands += splits

            docking_details['ligands'] = splitted_ligands
            docking_details['ligands_name'] = ligands_name
            docking_id = ServerHttpDockingService.createDocking(docking_details)
        except Exception as e:
            app.logger.error(e)
            raise e
        
        return docking_id
    
    @staticmethod
    def getMasterDockingIds()->list[dict[str, str]]:
        """function returns all docking_id of dockings started by master

        Raises:
            Exception: _description_

        Returns:
            list[dict[str, str]]: list of dict contaning docking_id and state of docking
        """
        return ServerHttpDockingService.getMasterDockingIds()

    @staticmethod
    def getAllComputeIds(docking_id: str)-> list[str]:
        """returns all compute_ids of a docking

        Args:
            docking_id (str): docking id

        Raises:
            Exception: _description_

        Returns:
            list[str]: list contaning compute ids
        """

        return ServerHttpDockingService.getAllComputeIds(docking_id=docking_id)


    @staticmethod
    def getComputeResult(compute_id: str)-> list[str]:
        """returns result pdbqt and ligand_name of given compute_id

        Args:
            compute_id (str): compute id of ligand

        Raises:
            Exception: _description_

        Returns:
            dict[str, str]: {
                "result": "pdbqt",
                "ligand_name": "name"
            }
        """

        return ServerHttpDockingService.getComputeResult(compute_id=compute_id)
    
    def downloadDockingResult(docking_id: str, path: str):
        """Method will download and save(at given location) docking result from server

        Args:
            docking_id (str): docking if
            path (str): path at which file will be saved

        Raises:
            Exception: _description_

        Returns:
            _type_: _description_
        """
        # check if given path exists or not
        if os.path.isdir(path) == False:
            raise Exception("Path do not exists: "+path)
        
        # create folder at that location
        result_folder_path = os.path.join(path, docking_id)
        if os.path.isdir(result_folder_path) == False:
            os.mkdir(result_folder_path)
        

        # get compute_ids from server
        compute_ids = ServerHttpDockingService.getAllComputeIds(docking_id=docking_id)
        
        # storing compute results
        for compute_id in compute_ids:
            result = ServerHttpDockingService.getComputeResult(compute_id=compute_id)
            
            compute_result_file_path = generateFilePath(result_folder_path, result['ligand_name'])
            compute_file = open(compute_result_file_path, 'w')
            compute_file.write(result['result'])
            compute_file.close()
        

