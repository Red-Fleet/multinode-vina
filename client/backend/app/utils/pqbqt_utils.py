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
        # splitting pdbqt file in lines
        lines = pdbqt.split("\n")
        ligands = [] # for storing parsed ligand
        curr_ligand = ""
        
        for line in lines:
            if "MODEL" in line:
                # start of new ligand file
                curr_ligand = ""
            elif "ENDMDL" in line:
                # end of current ligand, save it, if not empty
                if curr_ligand != "":
                    ligands.append(curr_ligand)
                    curr_ligand = ""
            elif line != "":
                # save line in current ligand
                curr_ligand += line + "\n"

        # if curr_ligand is not empty then save
        if curr_ligand != "":
            ligands.append(curr_ligand) 

        return ligands
        