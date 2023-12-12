from matplotlib import markers as mpl_markers


def rotate_marker(marker: str, rotate_angle: float) -> mpl_markers.MarkerStyle:
    """Rotate a matplotlib marker by a specified angle."""
    marker_handle = mpl_markers.MarkerStyle(marker=marker)
    marker_handle._transform = marker_handle.get_transform().rotate_deg(
        rotate_angle,
    )
    return marker_handle
