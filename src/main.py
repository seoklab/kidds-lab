import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from pprint import pprint

import numpy as np

import pdbline


@dataclass(frozen=True)
class ResidueId:
    chain_id: str
    res_seq: int
    icode: str

    @staticmethod
    def from_pdb_line(line: str):
        return ResidueId(
            chain_id=pdbline.chain_id(line),
            res_seq=pdbline.res_seq(line),
            icode=pdbline.ins_code(line),
        )


@dataclass(frozen=True)
class AtomId:
    res_id: ResidueId
    atom_name: str


@dataclass
class AtomSite:
    altloc: str
    coord: np.ndarray
    occupancy: float


@dataclass
class Atom:
    atom_id: AtomId

    res_name: str
    sites: list[AtomSite] = field(default_factory=list)

    def most_occupied_site(self):
        return max(self.sites, key=lambda site: site.occupancy)


def read_pdb(pdb: Path):
    model_atoms: list[dict[AtomId, Atom]] = []

    with open(pdb) as f:
        atoms: dict[AtomId, Atom] = {}

        for line in f:
            record = pdbline.record(line)
            if record == "MODEL":
                if atoms:
                    model_atoms.append(atoms)
                    atoms = {}
            elif record == "ATOM" or record == "HETATM":
                atom_id = AtomId(
                    res_id=ResidueId.from_pdb_line(line),
                    atom_name=pdbline.atom_name(line),
                )
                atom = atoms.setdefault(
                    atom_id,
                    Atom(atom_id=atom_id, res_name=pdbline.res_name(line)),
                )
                atom.sites.append(
                    AtomSite(
                        coord=pdbline.coordinates(line),
                        altloc=pdbline.alt_loc(line),
                        occupancy=pdbline.occupancy(line),
                    )
                )

        if atoms:
            model_atoms.append(atoms)

    return model_atoms


def count_model_residues(model_atoms: dict[AtomId, Atom]):
    residue_names: dict[ResidueId, str] = {}
    for atom in model_atoms.values():
        residue_names.setdefault(atom.atom_id.res_id, atom.res_name)
    return Counter(residue_names.values())


def main():
    pdb_file = Path(sys.argv[1])
    models = read_pdb(pdb_file)
    for model, atoms in enumerate(models):
        com = np.mean(
            [
                atom.most_occupied_site().coord
                for atom in atoms.values()
                if atom.atom_id.res_id.res_seq % 5 == 0
            ],
            axis=0,
        )
        res_cnt = count_model_residues(atoms)

        print(f"{model = }: {com = }")
        pprint(res_cnt, sort_dicts=False)


if __name__ == "__main__":
    main()
