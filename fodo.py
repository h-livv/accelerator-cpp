"""One FODO cell as a product of 2×2 transfer matrices.

A transverse ray is the column (x, x'), with x in metres and x' in radians.
The cell is the Xsuite getting-started FODO, in beam order: focusing
quadrupole, drift, defocusing quadrupole, drift. The quad lengths are
equal, the drift lengths are equal, and the normalised gradients are
opposite: 1 m at k1 = +0.12 m^-2, a 2 m drift, 1 m at k1 = -0.12 m^-2,
a 2 m drift.

The element met first stands on the right of the product. Each later
matrix multiplies on the left. That is the product xtrack.Line.get_R_matrix
returns for this cell, and the order Wiedemann uses for a thick half-cell.
The same 2×2 block is used in each plane; the other plane swaps the two
quadrupole matrices.
"""

import numpy as np

# Normalised gradient and element lengths of that Xsuite cell.
k1 = 0.12
quad_length = 1.0
drift_length = 2.0


def quadrupole(k, length):
    """Transfer matrix of one thick quadrupole in one transverse plane.

    k is the normalised gradient k1 in m^-2. Positive k focuses in this
    plane. length is in metres. The phase advance through the magnet is
    length * sqrt(|k|).

    Focusing uses cos and sin. Defocusing uses cosh and sinh of the same
    phase. The lower-left entry is the angle change per unit offset: negative
    when the quadrupole focuses, positive when it defocuses.
    """
    root = np.sqrt(abs(k))
    phase = root * length
    if k > 0.0:
        # Focusing. A positive offset leaves with a negative angle.
        cosine = np.cos(phase)
        sine = np.sin(phase)
        return np.array([[cosine, sine / root], [-root * sine, cosine]])
    # Defocusing. A positive offset leaves with a positive angle.
    cosine = np.cosh(phase)
    sine = np.sinh(phase)
    return np.array([[cosine, sine / root], [root * sine, cosine]])


def drift(length):
    """Transfer matrix of a field-free drift.

    length is in metres. The offset changes by length times the angle.
    The angle is unchanged, so the lower-left entry is zero and the
    upper-right entry is the length.
    """
    return np.array([[1.0, length], [0.0, 1.0]])


# Four factors in beam order. The quadrupoles have opposite k1.
elements = (
    ("focusing quadrupole", quadrupole(+k1, quad_length)),
    ("drift", drift(drift_length)),
    ("defocusing quadrupole", quadrupole(-k1, quad_length)),
    ("drift", drift(drift_length)),
)

np.set_printoptions(precision=8, suppress=True, floatmode="fixed", linewidth=100)

# Map from the cell entrance. The first factor replaces this identity.
# matrix @ cell puts the element just traversed on the left, so it acts
# after every factor already included.
cell = np.eye(2)
for name, matrix in elements:
    cell = matrix @ cell
    print(name)
    print(matrix)
    print("running product")
    print(cell)
    print()

# The product after the fourth factor is the map of one cell.
print("cell")
print(cell)

# One ray through that map: the exit column is the cell matrix times the entrance column.
ray = np.array([1.0e-3, 2.0e-4])
print("ray before")
print(ray)
print("ray after")
print(cell @ ray)
