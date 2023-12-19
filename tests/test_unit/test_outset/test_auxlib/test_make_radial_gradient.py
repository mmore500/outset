from outset._auxlib.make_radial_gradient_ import make_radial_gradient


def test_gradient_shape():
    """Test if the output array has the correct shape."""
    gradient = make_radial_gradient()
    assert len(gradient.shape) == 2, "Gradient should be two dimensional"


def test_gradient_value_range():
    """Test if the gradient values are within the range 0 to 1."""
    gradient = make_radial_gradient()
    assert (
        gradient.min() >= 0
    ), "Minimum value should be greater than or equal to 0"
    assert (
        gradient.max() <= 1
    ), "Maximum value should be less than or equal to 1"
