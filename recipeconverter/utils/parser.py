from fractions import Fraction
import os
import csv
import re
import unicodedata

CONVERSION_TABLE_CSV = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "..", "gram-conversions.csv"
)


def import_conversions() -> list:
    """Import ingredient conversion table

    Returns:
        list: List of dicts (ingredient, cup, tablespoon, teaspoon)
    """

    def string_to_float(input: str) -> float:
        try:
            output = float(input)
        except ValueError:
            output = None

        return output

    with open(CONVERSION_TABLE_CSV) as csvfile:
        conversion_table = list(csv.reader(csvfile, delimiter=","))

    # Remove header
    header = conversion_table[0]
    conversion_table.pop(0)

    # Convert list of lists to list of dicts
    out_table = []
    for line in conversion_table:
        d = {
            header[0]: line[0],
            header[1]: string_to_float(line[1]),
            header[2]: string_to_float(line[2]),
            header[3]: string_to_float(line[3]),
        }
        out_table.append(d)

    return out_table


def convert_ingredient_volume_to_mass(line: str) -> str:
    """Convert ingredient line from volume to mass

    Args:
        line (str): ie. "1 cup flour"

    Returns:
        str: Converted line, ie. "120.0 g flour
    """

    def get_ingredient_conversion(ingredient: str, unit: str) -> float:
        """Get conversion factor for the given ingredient

        Args:
            ingredient (str): ie. Flour, sugar, etc.
            unit (str): Cup, tablespoon, or teaspoon

        Returns:
            float: Conversion factor from unit to grams
        """
        conversion_table = import_conversions()

        ingredient_found = False

        for conversion_line in conversion_table:
            if conversion_line["ingredient"] in ingredient:
                conversion = conversion_line[unit]
                ingredient_found = True
                break

        if not ingredient_found:
            conversion = 1

        return conversion

    amount, unit, ingredient = parse_line(line.lower())

    amount = fraction_to_float(amount)

    amount_converted = amount * get_ingredient_conversion(ingredient, unit)

    return f"{amount_converted:.1f} g {ingredient}"


def parse_line(line: str) -> tuple:
    """Exract components from ingredient line

    Args:
        line (str): Input line, ie. "1 1/2 cup brown sugar"

    Returns:
        tuple (str): Amount (ie. "1 1/2")
        tuple (str): Unit (ie. "cup")
        tuple (str): Ingredient (ie. "brown sugar")
    """

    line = line.replace("tbsp", "tablespoon")
    line = line.replace("tsp", "teaspoon")

    p = re.compile(r"(.+?)(cup|tablespoon|teaspoon)(.*)")
    m = p.findall(line)

    amount = m[0][0].strip()
    unit = m[0][1].strip()
    ingredient = m[0][2].strip()

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
