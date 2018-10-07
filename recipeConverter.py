# import win32clipboard
import unicodedata
import csv

class RecipeConverter:
    def __init__(self):
        # Conversion table from volumetric to metric grams
        self.conversions = self.import_conversions('gram-conversions.csv')
                
    def import_conversions(self, filename):
        with open(filename) as csvfile:
            conversion_table = list(csv.reader(csvfile, delimiter=','))

            # Remove header
            conversion_table.pop(0)

            return conversion_table
        
    def parse_line(self, ingredient):
        # From Genius recipes
        ingredient = ingredient.replace('1⁄4', '.25')
        ingredient = ingredient.replace('1⁄3', '.33')
        ingredient = ingredient.replace('1⁄2', '.5')
        ingredient = ingredient.replace('2⁄3', '.66')
        ingredient = ingredient.replace('3⁄4', '.75')

        # Standard float expressions
        ingredient = ingredient.replace('1/8', '.125')
        ingredient = ingredient.replace('1/4', '.25')
        ingredient = ingredient.replace('1/3', '.33')
        ingredient = ingredient.replace('1/2', '.5')
        ingredient = ingredient.replace('2/3', '.66')
        ingredient = ingredient.replace('3/4', '.75')
        
        # Replace abbreviations
        ingredient = ingredient.replace('tbsp','tablespoon')
        ingredient = ingredient.replace('tsp','teaspoon')
        ingredient = ingredient.replace('oz','ounces')

        return ingredient

    def convert_ingredient(self, line, unit, conversion):
        try:
            # Extract number from measurement
            number_string = line.split(unit)[0].replace(' ','')
            number_float = float(number_string)

            # Convert butter cup to grams
            converted = number_float * float(conversion)

            # Construct the output ingredient line with original line
            line_out = '%g g%s'%(converted, line.split(unit)[1].strip('s'))
        except:
            # Return the original line if any error occurred)
            line_out = line

        return line_out

    def parse_recipe(self, text, multiplier):
        output = []

        for recipe_line in text:
            flag_converted = False

            # For each recipe line item, look it up in the conversion table
            for ingredient_gram in self.conversions:
                if ingredient_gram[0] in recipe_line:
                    flag_converted = True

                    # Convert fractions to floats and remove abbreviations
                    line = self.parse_line(recipe_line)

                    if 'cup' in line:
                        output.append(self.convert_ingredient(line, 'cup', float(ingredient_gram[1])*multiplier))
                        break
                    elif 'tablespoon' in line:
                        output.append(self.convert_ingredient(line, 'tablespoon', float(ingredient_gram[2])*multiplier))
                        break
                    elif 'teaspoon' in line:
                        output.append(self.convert_ingredient(line, 'teaspoon', float(ingredient_gram[3])*multiplier))
                        break
                    else:
                        flag_converted = False

            # If nothing was found, then use original line
            if not flag_converted:

                # Scale any numbers in the recipe line
                recipe_line_multiplied = []
                for word in recipe_line.split():
                    try:
                        recipe_line_multiplied.append('%g'%(float(word)*multiplier))
                    # Will fail on float(word) if it's not a number
                    except ValueError:
                        recipe_line_multiplied.append(word)

                output.append(" ".join(recipe_line_multiplied))

        return output

def display_lines(text_list):
    for line in text_list:
        print(line)
        
    print()