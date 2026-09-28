# Particle Accelerator from Scratch

### A small accelerator-physics simulation written from scratch in Python + NumPy.

> I'm using this project to learn **accelerator physics, beam optics, and beam dynamics** by implementing the underlying physics myself.

## Current

Two small programs.

### Particle tracking

The tracking program follows a **10 MeV proton** through a simple magnetic beamline:

```text
Dipole → Quadrupole
```

- 0.5 m hard-edge dipole, `By = 0.5 T`
- 0.4 m hard-edge quadrupole, `G = 2 T/m`
- Relativistic **Boris integrator**
- No electric field, so the magnetic field only changes the particle's direction
- Checks that the particle's speed remains constant up to numerical roundoff

### FODO cell

One FODO cell, as a product of 2×2 transfer matrices. The cell is the Xsuite getting-started example, in beam order:

```text
Focusing quadrupole → Drift → Defocusing quadrupole → Drift
```

- Equal quadrupoles, 1 m, opposite gradients `k1 = +0.12` and `k1 = -0.12` m⁻²
- Equal drifts, 2 m
- The first element stands on the right of the product; each later matrix multiplies on the left
- Prints each matrix, the running product, the cell matrix, and one transverse ray before and after

### Files

```text
elements.py       # Dipole, quadrupole, magnetic fields
boris.py          # Constants, relativistic velocity, Boris solver
track.py          # Beamline tracking
accelerator.py    # Example simulation
fodo.py           # One FODO cell as a product of transfer matrices
```

## Run

Requirements:

```bash
pip install numpy
```

Then:

```bash
python accelerator.py
```

The program prints the particle position after each magnet and the relative speed change.

```bash
python fodo.py
```

The program prints the four matrices, the running product, the cell matrix, and the ray.

## Planned

The project will gradually move from single-particle tracking toward beam optics and beam dynamics:

- Phase-space tracking
- Twiss parameters and emittance
- RF cavities and longitudinal dynamics
- Energy-recovery linac

The goal is to learn the physics by building the accelerator model from the ground up.
