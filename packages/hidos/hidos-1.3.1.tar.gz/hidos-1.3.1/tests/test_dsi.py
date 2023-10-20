import pytest

from hidos.dsi import EditionId, Dsi

def test_empty_edition_id():
    empty = EditionId()
    assert len(empty) == 0
    assert str(empty) == ""
    assert empty.listed is True


def test_edition_id_bad_values():
    with pytest.raises(ValueError):
        EditionId("1.-1")
    with pytest.raises(ValueError):
        EditionId("-1")
    with pytest.raises(ValueError):
        EditionId("1.b1")
    with pytest.raises(ValueError):
        EditionId([1, 1.2])


def test_edition_id_compare():
    assert EditionId("1.1") > EditionId("0.3")
    assert EditionId("1.11") > EditionId("1.9")


def test_dsi():
    dsi = Dsi("DZFCt68peNNajZ34WtZni9VYxzo")
    assert len(dsi.edid) == 0
    s = "DZFCt68peNNajZ34WtZni9VYxzo/1"
    dsi = Dsi("DZFCt68peNNajZ34WtZni9VYxzo/1")
    assert dsi.edid == EditionId("1")
    assert str(dsi) == s
    assert dsi == Dsi(s)
