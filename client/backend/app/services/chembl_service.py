from chembl_webresource_client.new_client import new_client
from app.utils.file_utils import generateFilePath
from openbabel import openbabel as ob
from openbabel import pybel as pb

class ChemblService:

    @staticmethod
    def getSdfUsingChemblId(chembl_id: str) -> str:
        compound = new_client.molecule.get(chembl_id)

        # checking if sdf is present or not
        if "molfile" in compound["molecule_structures"]:
            return str(compound["molecule_structures"]["molfile"])
        else :
            raise Exception(chembl_id + " : sdf not avalable")
        

    def saveSdfUsingChemblId(chembl_id: str, dir_path: str):
        sdf = ChemblService.getSdfUsingChemblId(chembl_id=chembl_id)
        file_path = generateFilePath(file_dir=dir_path, file_name= chembl_id+".sdf")
        
        with open(file_path, 'w+') as f:
            f.write(sdf)

    
    def savePdbqtUsingChemblId(chembl_id: str, dir_path: str):
        sdf = ChemblService.getSdfUsingChemblId(chembl_id=chembl_id)
        file_path = generateFilePath(file_dir=dir_path, file_name= chembl_id+".pdbqt")

        # convert sdf to pdbqt using openbabel
        pymol = pb.readstring(format="sdf", string=sdf)
        pdbqt = pymol.write(format="pdbqt")

        with open(file_path, 'w+') as f:
            f.write(pdbqt)

        