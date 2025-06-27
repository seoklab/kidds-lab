import sys
from pathlib import Path

import numpy as np

import pdbline


def read_pdb(pdb: Path):
    coords: list[np.ndarray] = []

    with open(pdb) as f:
        for line in f:
            record = pdbline.record(line)
            if record == "ATOM" or record == "HETATM":
                coords.append(pdbline.coordinates(line))

    return np.stack(coords)


def main():
    pdb_file = Path(sys.argv[1])
    coords = read_pdb(pdb_file)
    com = np.mean(coords, axis=0)
    print(f"{com = }")


if __name__ == "__main__":
    main()
