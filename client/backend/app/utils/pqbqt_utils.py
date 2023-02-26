import re

class PdbqtUtils:
    @staticmethod
    def splitIntoLigands(pdbqt: str) -> list[str]:
        """method is used to get ligands from a single pdbqt

        Args:
            pdbqt (str): string of pdbqt

        Returns:
            list[str]: list of str contaning ligands
        """
        ligands = re.split(r'\n *ENDMDL', pdbqt)
        
        # only add ENDMDL if it was removed
        if bool(re.split(r'\n *ENDMDL', pdbqt)) == True:
            ligands = [ligand+'\nENDMDL' for ligand in ligands]

        return ligands
        