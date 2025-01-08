import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from pprint import pprint

import numpy as np

import pdbline


@dataclass(frozen=True)
class ResidueId:
    chain_id: str
    res_seq: int
    icode: str


@dataclass
class Atom:
    res_name: str
    res_id: ResidueId
    coord: np.ndarray


def read_pdb(pdb: Path):
    model_atoms: list[list[Atom]] = []

    with open(pdb) as f:
        atoms: list[Atom] = []

        for line in f:
            record = pdbline.record(line)
            if record == "MODEL":
                if atoms:
                    model_atoms.append(atoms)
                    atoms = []
            elif record == "ATOM" or record == "HETATM":
                atoms.append(
                    Atom(
                        res_name=pdbline.res_name(line),
                        res_id=ResidueId(
                            chain_id=pdbline.chain_id(line),
                            res_seq=pdbline.res_seq(line),
                            icode=pdbline.ins_code(line),
                        ),
                        coord=pdbline.coordinates(line),
                    )
                )

        if atoms:
            model_atoms.append(atoms)

    return model_atoms


def count_model_residues(model_atoms: list[Atom]):
    residue_names: dict[ResidueId, str] = {}
    for atom in model_atoms:
        residue_names.setdefault(atom.res_id, atom.res_name)
    return Counter(residue_names.values())


def main():
    pdb_file = Path(sys.argv[1])
    models = read_pdb(pdb_file)
    for model, atoms in enumerate(models):
        com = np.mean(
            [atom.coord for atom in atoms if atom.res_id.res_seq % 5 == 0],
            axis=0,
        )
        res_cnt = count_model_residues(atoms)

        print(f"{model = }: {com = }")
        pprint(res_cnt, sort_dicts=False)


if __name__ == "__main__":
    main()
