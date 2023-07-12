from vina import Vina
import os
import time

start_time = time.process_time()
vina = Vina()

vina.set_receptor("receptor path")
center = [2, 2, 2]
box = [2, 2, 2]

vina.compute_vina_maps(center=center, box_size=box)

ligands_dir = ""
results_dir = ""

ligands_names = os.listdir()

for name in ligands_names:
    vina.set_ligand_from_file(os.path.join(ligands_dir, name))

    vina.dock(exhaustiveness=8, n_poses=20)

    result = vina.poses(n_poses=20)

    f = open(os.path.join(results_dir, name), "w")
    f.write(result)
    f.close()

print("Total time :" + str(time.process_time()-start_time) + " seconds")