import sys
from pathlib import Path

import numpy as np

import pdbline


def read_pdb(pdb: Path):
    models: list[np.ndarray] = []

    with open(pdb) as f:
        model: list[np.ndarray] = []

        for line in f:
            record = pdbline.record(line)
            if record == "MODEL":
                if model:
                    models.append(np.stack(model))
                model = []
            elif record == "ATOM" or record == "HETATM":
                if pdbline.res_seq(line) % 5 == 0:
                    model.append(pdbline.coordinates(line))

        if model:
            models.append(np.stack(model))

    return models


def main():
    pdb_file = Path(sys.argv[1])
    models = read_pdb(pdb_file)
    for model, coords in enumerate(models):
        com = np.mean(coords, axis=0)
        print(f"{model = }: {com = }")


if __name__ == "__main__":
    main()
