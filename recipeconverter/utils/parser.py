from fractions import Fraction
import re

def convert_ingredient_volume_to_mass(line: str) -> str:
    return "foo"

def parse_line(line:str) -> tuple:
    p = re.compile(r"(.+?)(?=[a-zA-z])([a-zA-Z]\w+)")
    m = p.findall(line)
    print(m)

    amount = m[0][0].strip()
    unit = m[0][1].strip()
    ingredient = m[1][1].strip()

    return amount, unit, ingredient

def fraction_to_float(fraction: str) -> float:
    """Convert string representation of a fraction to float

    Args:
        fraction (str): String representation of fraction, ie. "3/4", "1 1/2", etc.

    Returns:
        float: Converted fraction
    """
    return float(sum(Fraction(s) for s in fraction.split()))

