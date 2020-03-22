from fractions import Fraction
import re
import unicodedata

def convert_ingredient_volume_to_mass(line: str) -> str:
    return "foo"

def parse_line(line:str) -> tuple:
    p = re.compile(r"(.+?)(?=[a-zA-z])([a-zA-Z]\w+)")
    m = p.findall(line)

    amount = m[0][0].strip()
    unit = m[0][1].strip()

    # Use all remaining matches as ingredients (ie. "whole wheat flour")
    ingredient = ""
    for match in m[1:]:
        ingredient += "%s " % match[-1]

    ingredient = ingredient.strip()

    return amount, unit, ingredient

def fraction_to_float(fraction: str) -> float:
    """Convert string representation of a fraction to float.

    Also supports unicode characters.

    Args:
        fraction (str): String representation of fraction, ie. "3/4", "1 1/2", etc.

    Returns:
        float: Converted fraction
    """
    # For fractions with weird divider character (ie. "1⁄2")
    fraction = fraction.replace("⁄", "/")

    try:
        # Convert unicode fractions (ie. "½")
        fraction_out = unicodedata.numeric(fraction)
    except TypeError:
        # Convert normal fraction (ie. "1/2")
        fraction_out = float(sum(Fraction(s) for s in fraction.split()))

    return fraction_out
