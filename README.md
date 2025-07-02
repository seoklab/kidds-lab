# KIDDS Summer 2025 – Software Engineering Seminar

> :ledger: The slide is available in the `docs/` directory.
> [Download PDF version here](https://raw.githubusercontent.com/seoklab/kidds-lab/refs/heads/main/docs/250702-slide.pdf).

Welcome to the lab session! This hands-on exercise simulates evolving
real-world code through a series of progressive changes.

## Getting Started

1. Clone this repository to your local machine.

   ```bash
   git clone https://github.com/seoklab/kidds-lab
   cd kidds-lab
   ```

2. Edit [`src/main.py`](src/main.py) as you progress through each stage of the
   lab.

   - Each stage introduces a new goal or modification, much like real-world
     software evolution.

   - Updated requirements will be presented live during the seminar.

   - You can test your code by running it with the provided PDB file:

     ```bash
     python src/main.py data/protein.pdb
     ```

     The file [`data/protein.pdb`](data/protein.pdb) is provided for
     testing[^1]. Expected outputs for each stage will be shared during the
     session.

## If You're Stuck

If you miss a stage or want to align with the current one, use the
[`prepare-stage.sh`](prepare-stage.sh) script.

- It applies naive reference solutions for all previous stages and prepares your
  working directory for the stage you specify.

  ```bash
  ./prepare-stage.sh <stage>
  ```

  Replace `<stage>` with a number from 1 to 5. For example:

  ```bash
  ./prepare-stage.sh 3
  ```

  This will apply solutions for stages 0 through 2 and leave stage 3 ready for
  you to implement.

- The script is reentrant, so you can run it again or switch between stages as
  needed.

> ⚠️ **Important:** This script will **overwrite your working files**. To keep
> your current progress, commit your changes first. The git history is
> preserved, so you can always roll back if needed.

---

[^1]: It is PDB entry [3CYE](https://www.rcsb.org/structure/3CYE), a very
unusual file with *both* multiple models and alternate locations, and differing
residue ids across models. It highlights the complexity of real-world PDB data.
