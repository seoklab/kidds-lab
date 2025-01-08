"""
This is a module for parsing PDB lines.
You don't need to change this file.
"""

import numpy as np


def record(line: str) -> str:
    return line[:6].strip()


def atom_serial(line: str) -> int:
    return int(line[6:11])


def atom_name(line: str) -> str:
    return line[12:16].strip()


def alt_loc(line: str) -> str:
    return line[16]


def res_name(line: str) -> str:
    return line[17:20].strip()


def chain_id(line: str) -> str:
    return line[21]


def res_seq(line: str) -> int:
    return int(line[22:26])


def ins_code(line: str) -> str:
    return line[26]


def coordinates(line: str) -> np.ndarray:
    return np.array([line[30:38], line[38:46], line[46:54]], dtype=np.float64)


def occupancy(line: str) -> float:
    return float(line[54:60])


def temp_factor(line: str) -> float:
    return float(line[60:66].strip() or 0)


def atom_element(line: str) -> str:
    return line[76:78].strip()


def atom_charge(line: str) -> int:
    return int(line[78:80].strip() or 0)
