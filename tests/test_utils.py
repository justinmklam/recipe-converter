import pytest
from recipeconverter import utils


def test_fraction_to_float():
    assert utils.fraction_to_float("1/2") == 0.5
    assert utils.fraction_to_float("½") == 0.5
    assert utils.fraction_to_float("1⁄4") == 0.25
    assert utils.fraction_to_float("3⁄4") == 0.75
    assert utils.fraction_to_float("1 1/4") == 1.25
    assert utils.fraction_to_float("2") == 2


def test_string_to_float():
    assert utils.string_to_float("1.5") == 1.5
    assert utils.string_to_float("0.5") == 0.5
    assert utils.string_to_float("1") == 1.0
    assert utils.string_to_float("") is None
    assert utils.string_to_float("foobar") is None
