import recipeconverter.utils.parser as parser


def test_fraction_to_float():
    assert parser.fraction_to_float("1/2") == 0.5
    assert parser.fraction_to_float("1 1/4") == 1.25
    assert parser.fraction_to_float("2") == 2
