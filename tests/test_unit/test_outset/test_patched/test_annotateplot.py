import pandas as pd
import matplotlib.pyplot as plt
import pytest

from outset import patched as otst_patched


@pytest.fixture
def sample_data():
    """Provide a small dataset for testing."""
    return pd.DataFrame(
        {"x": [1, 2, 3], "y": [4, 5, 6], "text": ["A", "B", "C"]}
    )


def test_annotateplot(sample_data: pd.DataFrame):
    """Test the annotateplot function with minimal input."""
    fig, ax = plt.subplots()
    result = otst_patched.annotateplot(
        data=sample_data, x="x", y="y", text="text", ax=ax
    )
    assert isinstance(result, plt.Axes)

    outpath = "/tmp/test_annotateplot.png"
    plt.savefig(outpath)
    print(f"saved graphic to {outpath}")
