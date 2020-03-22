import pytest
import recipeconverter as rc


def test_convert_ingredient_line():
    assert rc.convert_ingredient_volume_to_mass("1 cup flour") == "120.0 g flour"
    assert rc.convert_ingredient_volume_to_mass("1 CUP FLOUR") == "120.0 g flour"
    assert rc.convert_ingredient_volume_to_mass("1 cup sugar") == "201.0 g sugar"
    assert (
        rc.convert_ingredient_volume_to_mass("1 tablespoon sugar") == "12.5 g sugar"
    )
    assert rc.convert_ingredient_volume_to_mass("1 teaspoon sugar") == "4.2 g sugar"
    assert rc.convert_ingredient_volume_to_mass("1 tbsp sugar") == "12.5 g sugar"
    assert rc.convert_ingredient_volume_to_mass("1 tsp sugar") == "4.2 g sugar"


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
        amount, unit, ingredient = rc.parse_line(" ".join(line))
        assert amount == line[0]
        assert unit == line[1]
        assert ingredient == line[2]


def test_parse_incompatible_ingredient_line():
    lines = [
        ["1", "banana, finely crushed"],
        ["1", "figs (optional)"],
    ]

    for line in lines:
        amount, unit, ingredient = rc.parse_line(" ".join(line))
        assert amount == line[0]
        assert unit == ""
        assert ingredient == line[1]


def test_convert_recipe():
    recipe = """2/3 cup butter
1 cup sugar
3 bananas
1/2 teaspoon salt"""

    recipe_out = rc.convert_recipe(recipe)

    expected_recipe_out = """151.3 g butter
201.0 g sugar
3.0 bananas
2.5 g salt"""

    assert recipe_out == expected_recipe_out
