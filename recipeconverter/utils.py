import unicodedata
from fractions import Fraction


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
        try:
            # Convert normal fraction (ie. "1/2")
            fraction_out = float(sum(Fraction(s) for s in fraction.split()))
        except ValueError:
            # Convert combined fraction with unicode (ie. "1 ½")
            fraction_split = fraction.split()
            fraction_out = float(fraction_split[0]) + unicodedata.numeric(
                fraction_split[1]
            )

    return fraction_out


def string_to_float(input: str) -> float:
    """Convert string to float, if possible

    Args:
        input (str): Input string (ie. "1.5")

    Returns:
        float: Casted value (ie. 1.5), or None if conversion was not possible
    """
    try:
        output = float(input)
    except ValueError:
        output = None

    return output
