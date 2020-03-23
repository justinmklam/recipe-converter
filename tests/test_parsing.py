import pytest
import recipeconverter as rc


@pytest.fixture
def rc_handler():
    return rc.RecipeConverter()


def test_convert_ingredient_line(rc_handler):
    assert rc_handler.convert_volume_to_mass("1 cup flour") == "142 g flour"
    assert rc_handler.convert_volume_to_mass("2 cups flour") == "284 g flour"
    assert rc_handler.convert_volume_to_mass("1 cup flour", multiplier=2) == "284 g flour"
    assert rc_handler.convert_volume_to_mass("1 CUP FLOUR") == "142 g flour"
    assert rc_handler.convert_volume_to_mass("1 cup sugar") == "198 g sugar"
    assert rc_handler.convert_volume_to_mass("1 tablespoon sugar") == "12.5 g sugar"
    assert rc_handler.convert_volume_to_mass("1 teaspoon sugar") == "4.2 g sugar"
    assert rc_handler.convert_volume_to_mass("1 tbsp sugar") == "12.5 g sugar"
    assert rc_handler.convert_volume_to_mass("1 tsp sugar") == "4.2 g sugar"
    assert rc_handler.convert_volume_to_mass("1 oz sugar") == "28.3 g sugar"
    assert rc_handler.convert_volume_to_mass("1 lb flour") == "453.6 g flour"
    assert rc_handler.convert_volume_to_mass("1 cup foobar") == "1 cup foobar"


def test_parse_ingredient_line(rc_handler):
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
        amount, unit, ingredient = rc_handler.parse_line(" ".join(line))
        assert amount == line[0]
        assert unit == line[1]
        assert ingredient == line[2]


def test_parse_incompatible_ingredient_line(rc_handler):
    lines = [
        ["1", "banana, finely crushed"],
        ["1", "figs (optional)"],
    ]

    for line in lines:
        amount, unit, ingredient = rc_handler.parse_line(" ".join(line))
        assert amount == line[0]
        assert unit == ""
        assert ingredient == line[1]


def test_convert_recipe(rc_handler):
    recipe = """2/3 cup butter
1 cup sugar
3 bananas
1/2 teaspoon salt"""

    recipe_out = rc_handler.convert_recipe(recipe)

    expected_recipe_out = """151.3 g butter
198 g sugar
3 bananas
2.5 g salt"""

    assert recipe_out == expected_recipe_out
