import sys
from pathlib import Path

import numpy as np

import pdbline


def read_pdb(pdb: Path):
    coords: list[np.ndarray] = []

    with open(pdb) as f:
        for line in f:
            # Fill in here
            pass

    return # What should this return?


def main():
    pdb_file = Path(sys.argv[1])

    # Fill in here


if __name__ == "__main__":
    main()
