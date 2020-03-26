import csv
import os
import re
from recipe_scrapers import scrape_me
from recipeconverter import utils


def import_conversions(filename) -> list:
    """Import ingredient conversion table

    Returns:
        list: List of dicts (ingredient, cup, tablespoon, teaspoon)
    """

    with open(filename) as csvfile:
        conversion_table = list(csv.reader(csvfile, delimiter=","))

    # Remove header
    header = conversion_table[0]
    conversion_table.pop(0)

    # Convert list of lists to list of dicts
    out_table = []
    for line in conversion_table:
        d = {
            header[0]: line[0],
            header[1]: utils.string_to_float(line[1]),
            header[2]: utils.string_to_float(line[2]),
            header[3]: utils.string_to_float(line[3]),
        }
        out_table.append(d)

    return out_table


class RecipeConverter:
    """Convert ingredients and recipes from volumetric to mass units. Includes
    commonly used baking ingredients such as flour, sugar, etc.
    """

    OUNCE_TO_GRAM = 28.3495
    POUND_TO_GRAM = 453.592

    def __init__(self):
        # Values from https://www.cooksillustrated.com/how_tos/5490-baking-conversion-chart
        database_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "gram-conversions.csv"
        )

        self._conversion_table = import_conversions(database_path)

    def convert_recipe_from_url(self, url: str, multiplier=1.0) -> tuple:
        """Convert recipe from URL, if supported

        Args:
            url (str): Recipe URL
            multiplier (float, optional): Recipe scale factor. Defaults to 1.0.

        Returns:
            tuple (str): Output recipe
            tuple (recipe_scrapers.allrecipes.AllRecipes): Recipe scraper object
        """

        scraper = scrape_me(url)

        ingredients = "\n".join(scraper.ingredients())

        return self.convert_recipe(ingredients, multiplier), scraper

    def convert_recipe(self, recipe: str, multiplier=1.0) -> str:
        """Convert a multi-line recipe from volumetric units to mass units

        Args:
            recipe (str): Input recipe
            multiplier (float, optional): Recipe scale factor. Defaults to 1.0.

        Returns:
            str: Output recipe
        """
        output = ""
        for line in recipe.split("\n"):
            try:
                output += self.convert_volume_to_mass(line, multiplier) + "\n"
            except Exception as e:
                print(f"Could not convert: '{line}''")
                print(repr(e))
                output += line + "\n"

        return output.strip()

    def convert_volume_to_mass(self, line: str, multiplier=1.0) -> str:
        """Convert ingredient line from volume to mass.

        Also converts imperial weight to metric (ie. ounce or pounds)

        Args:
            line (str): ie. "1 cup flour"
            multiplier (float, optional): Scale factor to multiply ingredient by

        Returns:
            str: Converted line, ie. "120.0 g flour
        """
        amount, unit, ingredient = self.extract_from_line(line.lower())

        amount = utils.fraction_to_float(amount)

        if unit == "ounce":
            conversion = self.OUNCE_TO_GRAM
            unit = "g"
        elif unit == "pound":
            conversion = self.POUND_TO_GRAM
            unit = "g"
        else:
            conversion, unit = self.get_ingredient_conversion(ingredient, unit)

        amount_converted = amount * conversion * multiplier

        if amount_converted.is_integer():
            amount_converted = int(amount_converted)
        else:
            amount_converted = round(amount_converted, 1)

        # Incompatible ingredients won't have an associated unit
        if unit:
            unit_out = f" {unit} "
        else:
            unit_out = " "

        return f"{amount_converted}{unit_out}{ingredient}"

    def get_ingredient_conversion(self, ingredient: str, unit: str) -> float:
        """Get conversion factor for the given ingredient

        Args:
            ingredient (str): ie. Flour, sugar, etc.
            unit (str): Cup, tablespoon, or teaspoon

        Returns:
            float: Conversion factor from unit to grams
        """
        ingredient_found = False

        for conversion_line in self._conversion_table:
            if conversion_line["ingredient"] in ingredient:
                conversion = conversion_line[unit]
                ingredient_found = True
                break

        if not ingredient_found:
            conversion = 1
            unit_out = unit
        else:
            unit_out = "g"

        return conversion, unit_out

    @staticmethod
    def extract_from_line(line: str) -> tuple:
        """Extract components from ingredient line

        Args:
            line (str): Input line, ie. "1 1/2 cup brown sugar"

        Returns:
            tuple (str): Amount (ie. "1 1/2")
            tuple (str): Unit (ie. "cup"), or "" if no units (ie. "1 banana")
            tuple (str): Ingredient (ie. "brown sugar")
        """
        compatible_units = ["cup", "tablespoon", "teaspoon", "ounce", "pound"]
        regex_compatible = r"(.+?)(cup|tablespoon|teaspoon|ounce|pound)(?:s|)(.*)"
        regex_incompatible = r"(.+?)(?=[a-zA-z])(.*)"

        line = line.replace("tbsp", "tablespoon")
        line = line.replace("tsp", "teaspoon")
        line = line.replace("oz", "ounce")
        line = line.replace("lbs", "pound")
        line = line.replace("lb", "pound")

        if any(x in line for x in compatible_units):
            p = re.compile(regex_compatible)
            m = p.findall(line)

            amount = m[0][0].strip()
            unit = m[0][1].strip()
            ingredient = m[0][2].strip()

        else:
            p = re.compile(regex_incompatible)
            m = p.findall(line)

            amount = m[0][0].strip()
            unit = ""
            ingredient = m[0][1].strip()

        return amount, unit, ingredient
