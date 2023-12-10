import numpy as np


def make_radial_gradient() -> np.ndarray:
    """Generate a radial gradient intensity map.

    Gradient takes maximum intensity in upper-right corner of array.

    Returns
    -------
    np.ndarray
        A 2D NumPy array of shape (101, 101), containing the normalized radial
        gradient values ranging from 0 to 1.
    """

    x = np.linspace(-5, 0, 101)
    y = np.linspace(0, 5, 101)

    xs, ys = np.meshgrid(x, y)
    zs = -np.sqrt(xs**2 + ys**2)

    z_norm = (zs - np.min(zs.flat)) / (np.max(zs.flat) - np.min(zs.flat))
    # note: must assign to new variable or incorrect behavior occurs
    zs = np.power(z_norm, 2)  # nonlinear gradient rate
    z_norm = (zs - np.min(zs.flat)) / (np.max(zs.flat) - np.min(zs.flat))

    return z_norm
