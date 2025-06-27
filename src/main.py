import sys
from collections import Counter
from pathlib import Path
from pprint import pprint

import numpy as np

import pdbline


def read_pdb(pdb: Path):
    models: list[np.ndarray] = []
    res_cnts: list[Counter[str]] = []

    with open(pdb) as f:
        atom_coords: dict[
            tuple[str, int, str, str], tuple[np.ndarray, float]
        ] = {}
        rescnt: Counter[str] = Counter()
        residues_seen: set[tuple[str, int, str]] = set()

        for line in f:
            record = pdbline.record(line)
            if record == "MODEL":
                if atom_coords:
                    models.append(
                        np.stack(
                            [
                                coord_occupancy[0]
                                for coord_occupancy in atom_coords.values()
                            ]
                        )
                    )
                    res_cnts.append(rescnt)
                atom_coords = {}
                rescnt = Counter()
                residues_seen = set()
            elif record == "ATOM" or record == "HETATM":
                resid = (
                    pdbline.chain_id(line),
                    pdbline.res_seq(line),
                    pdbline.ins_code(line),
                )
                if resid not in residues_seen:
                    rescnt[pdbline.res_name(line)] += 1
                    residues_seen.add(resid)

                res_seq = pdbline.res_seq(line)

                if res_seq % 5 == 0:
                    atom_name = pdbline.atom_name(line)
                    atom_id = resid + (atom_name,)

                    atom_coord = pdbline.coordinates(line)
                    atom_occupancy = pdbline.occupancy(line)
                    if atom_id not in atom_coords:
                        atom_coords[atom_id] = (atom_coord, atom_occupancy)
                    else:
                        prev_coord_occupancy = atom_coords[atom_id]
                        if atom_occupancy > prev_coord_occupancy[1]:
                            atom_coords[atom_id] = (atom_coord, atom_occupancy)

        if atom_coords:
            models.append(
                np.stack([coord for coord, _ in atom_coords.values()])
            )
            res_cnts.append(rescnt)

    return models, res_cnts


def main():
    pdb_file = Path(sys.argv[1])
    models, res_cnts = read_pdb(pdb_file)
    for model, (coords, res_cnt) in enumerate(zip(models, res_cnts)):
        com = np.mean(coords, axis=0)
        print(f"{model = }: {com = }")
        pprint(res_cnt, sort_dicts=False)


if __name__ == "__main__":
    main()
