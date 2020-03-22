import pytest
import recipeconverter.utils.parser as parser


@pytest.mark.skip(reason="No way of currently testing this")
def test_convert_ingredient_line():
    assert parser.convert_ingredient_volume_to_mass("1 cup flour") == "120 g flour"


def test_parse_ingredient_line():
    lines = [
        ["1", "cup", "flour"],
        ["1/2", "cup", "flour"],
        ["1⁄2", "cup", "flour"],
        ["½", "cup", "flour"],
        ["1 / 2", "cup", "flour"],
        ["1 1 / 2", "cup", "flour"],
        ["1 1/2", "cup", "flour"],
        ["1 1/2", "cup", "brown sugar"],
        ["1 1/2", "cup", "whole wheat flour"],
    ]

    for line in lines:
        amount, unit, ingredient = parser.parse_line(" ".join(line))
        assert amount == line[0]
        assert unit == line[1]
        assert ingredient == line[2]

def test_fraction_to_float():
    assert parser.fraction_to_float("1/2") == 0.5
    assert parser.fraction_to_float("½") == 0.5
    assert parser.fraction_to_float("1⁄4") == 0.25
    assert parser.fraction_to_float("3⁄4") == 0.75
    assert parser.fraction_to_float("1 1/4") == 1.25
    assert parser.fraction_to_float("2") == 2
