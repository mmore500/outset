from outset.util import NamedFrames


def test_NamedFrame_kwarg_initialization():
    assert NamedFrames(foo=(1, 2, 3, 4))["foo"] == (1, 2, 3, 4)


def test_NamedFrame_dict_initialization():
    assert NamedFrames({"foo": (1, 2, 3, 4)})["foo"] == (1, 2, 3, 4)
