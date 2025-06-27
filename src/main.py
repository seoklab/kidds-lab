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
        model: list[np.ndarray] = []
        rescnt: Counter[str] = Counter()
        residues_seen: set[tuple[str, int, str]] = set()

        for line in f:
            record = pdbline.record(line)
            if record == "MODEL":
                if model:
                    models.append(np.stack(model))
                    res_cnts.append(rescnt)
                model = []
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

                if pdbline.res_seq(line) % 5 == 0:
                    model.append(pdbline.coordinates(line))

        if model:
            models.append(np.stack(model))
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
