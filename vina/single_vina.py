from vina import Vina
import os
import time

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

log_file = open("vina.log", 'w')
total_time = time.process_time()
print("#&% Docking started")
log_file.write("#&% Docking started\n")
vina = Vina(cpu=8)

vina.set_receptor("6cc0_filled.pdbqt")
center = [-64, -16, 13]
box = [20, 20, 20]

vina.compute_vina_maps(center=center, box_size=box)

ligands_dir = "200_4"
results_dir = "result"

ligands_names = os.listdir(ligands_dir)

i = 0
for name in ligands_names:
    f = open(os.path.join(ligands_dir, name))
    ligands = splitIntoLigands(f.read())
    f.close()

    for ligand in ligands:
        start_time = time.time()
        process_start_time = time.process_time()

        vina.set_ligand_from_string(ligand)


        vina.dock(exhaustiveness=8, n_poses=20)

        result = vina.poses(n_poses=20)

        f = open(os.path.join(results_dir, str(i)+".pdbqt"), "w")
        f.write(result)
        f.close()
        i += 1
        print("#&% Time: " + str(time.time()-start_time) + ",  Process Time: " + str(time.process_time()-process_start_time))
        log_file.write("#&% Time: " + str(time.time()-start_time) + ",  Process Time: " + str(time.process_time()-process_start_time) + "\n")

print("#&% Total time :" + str(time.process_time()-total_time) + " seconds")
log_file.write("#&% Total time :" + str(time.process_time()-total_time) + " seconds\n")
log_file.close()
