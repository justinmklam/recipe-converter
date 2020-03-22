import recipeconverter.utils.parser as parser


def test_convert_ingredient_line():
    assert parser.convert_ingredient_volume_to_mass("1 cup flour") == "120 g flour"


def test_fraction_to_float():
    assert parser.fraction_to_float("1/2") == 0.5
    assert parser.fraction_to_float("1 1/4") == 1.25
    assert parser.fraction_to_float("2") == 2
